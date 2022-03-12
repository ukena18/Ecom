import json
from .models import *


# for cookie cart 
def cookieCart(request):
    try:
        #get te cart cookies using request.COOKIES
        cart = json.loads(request.COOKIES["cart"])
    except:
        #we puttry except block because we dont want to throw error
        cart = {}

    # print("Cartme", cart)
    # item is goona used for grabing product from database and send it to front end as a context
    items = []
    #those are default to send frontend if there is problem with database or back end
    # and for loop below we want to define vaariables
    order = {"get_cart_total": 0, "get_cart_items": 0, "shipping": False}
    cartItems = order["get_cart_items"]

    # loop for everyitem in the cart cookie
    for i in cart:
        #try-except is for prevent if cart item removed from database that prevent those mistakes
        # it is gonna loop thorough cart if item is not in the database
        # it is just gonna skip it
        try:
            #get total quantity
            cartItems += cart[i]["quantity"]
            # get the product
            product = Product.objects.get(id=i)
            # get the total of specific item
            total = (product.price * cart[i]["quantity"])
            #get the full total of order
            order["get_cart_total"] += total
            #get total quantity
            order["get_cart_items"] += cart[i]["quantity"]
            #create database clone to use same front end
            # so we dont need to change anything in the front end sinve data look similar
            item = {
                "product": {
                    "id": product.id,
                    "name": product.name,
                    "price": product.price,
                    "imageURL": product.imageURL,
                },
                "quantity": cart[i]["quantity"],
                "get_total": total
            }
            #add item to items array
            items.append(item)
            #if there is one physical item then shipping is true
            if product.digital == False:
                order["shipping"] = True
        except:
            pass
        #send json to frontend
    return {"cartItems":cartItems,"order":order,"items":items}

#get the data from cart either derived from cookie or database
def cartData(request):
    #if user is authenticated
    if request.user.is_authenticated:
        #find the customer
        customer = request.user.customer
        # print(customer)
        # get or create if order exist for customer , if not just create order with current customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        # get all the order items from order
        items = order.orderitem_set.all()
        # get the number of item from orde
        cartItems = order.get_cart_items
    # if user is not logged in,.... means just a guest
    else:
        #get data from cookie
        #the func is above
        cookieData = cookieCart(request)
        # get the number of item from orde
        cartItems = cookieData["cartItems"]
        #order info
        order = cookieData["order"]
        #items 
        items = cookieData["items"]

    return {"cartItems":cartItems,"order":order,"items":items}

#to create guest database even if he is guest
def guestOrder(request,data):

    # print("user is not legged in")
    # print("COOKIES:",request.COOKIES)
    #get the name and email from form
    name = data["form"]["name"]
    email = data["form"]["email"]

    #get the order detailfrom cookies
    cookieData = cookieCart(request)
    #get the item from cookies
    items = cookieData["items"]

    #create or get the customer 
    #this is guest we are trying to add database
    customer, created = Customer.objects.get_or_create(
        email=email,
    )
    #add name to customer
    customer.name = name
    #save to database
    customer.save()

    #add all those orders to new created guest database
    order = Order.objects.create(
        customer = customer,
        complete = False
    )

    #get all the items from dtabase and add it to order items
    for item in items:
        product = Product.objects.get(id=item["product"]["id"])

        orderItem = OrderItem.objects.create(
            product = product,
            order = order,
            quantity = item["quantity"]
        )
        return customer, order