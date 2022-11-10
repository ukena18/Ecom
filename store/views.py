
from django.shortcuts import render
from .models import *
# for api view
from django.http import JsonResponse
import json
import datetime

# dry(don't repeat yourself) functions
from .utils import cookieCart, cartData ,guestOrder


# #main page where you can see all product
# def store(request):
#     #get the cart data for looeged user or guest user
#     data = cartData(request)
#     #it isshow us how many item we do have in the frontend and keep refresh 
#     # every time we click add button
#     cartItems = data["cartItems"]

    #get all the produt
    products = Product.objects.all()
    #create context for frontend
    context = {"products": products, "cartItems": cartItems}
    #return to front end
#     return render(request, "store/store.html", context)  # Create your views here.


def cart(request):
    #get the cart data for looeged user or guest use
    data = cartData(request)
    #it isshow us how many item we do have in the frontend and keep refresh 
    # every time we click add button
    cartItems = data["cartItems"]
    #  get the order from cartData
    order = data["order"]
    # get the item from carDAta
    items = data["items"]
    #create context for frontend
    context = {"items": items, "order": order, "cartItems": cartItems}
    return render(request, "store/cart.html", context)  # Create your views here.


def checkout(request):
    #get the cart data for looeged user or guest use
    data = cartData(request)
    #it isshow us how many item we do have in the frontend and keep refresh 
    # every time we click add button
    cartItems = data["cartItems"]
     # get the order from cartData
    order = data["order"]
    # get the item from carDAta
    items = data["items"]
    #create context for frontend
    context = {"items": items, "order": order, "cartItems": cartItems}
    return render(request, "store/checkout.html", context)  # Create your views here.

# json return api end point
def updateItem(request):
    # load json request it has product id add action 
    #in the front end below every item 
    data = json.loads(request.body)
    productId = data["productId"]
    action = data["action"]
    # print(productId, action)

    #get the customer
    customer = request.user.customer
    # find the product
    product = Product.objects.get(id=productId)
    # either create or get the order based on which customer it is 
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    # either create or get the orderitem  based on which order it is 
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    # if action is add plus the quantity of order item
    if action == "add":
        orderItem.quantity = (orderItem.quantity + 1)
    # decrease the quantity of order item
    elif action == "remove":
        orderItem.quantity = (orderItem.quantity - 1)
    # and saave it to thedatabase
    orderItem.save()

    # if orderitem below zero just delete it  
    if orderItem.quantity <= 0:
        orderItem.delete()
    # retun confirmation( you didnt console anywhere)
    return JsonResponse("item was added", safe=False)


# json return api end point
# for check out order we created and shipping
def processOrder(request):
    #create unique transaction id
    transaction_id = datetime.datetime.now().timestamp()
    #get the data from form that include user info, total and shipping info
    data = json.loads(request.body)
    # print("data:", request.body)
    # if user logged in
    if request.user.is_authenticated:
        # get the current user info
        customer = request.user.customer
        # get the current order or create it
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    # if it is guest customer
    else:
        # create customer and order 
        customer,order = guestOrder(request,data)
    # get the toal of order from form 
    total = float(data["form"]['total'])
    # get the transaction id
    order.transaction_id = transaction_id
    # if total and cart_total match then complete order
    # that prevent malicuos attack from frontend
    #because you can change total with alittle bit javascript knowledge
    if total == order.get_cart_total:
        order.complete = True
    # save the order
    order.save()
    # if there is physical item get the shipping info
    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data["shipping"]["address"],
            city=data["shipping"]["city"],
            state=data["shipping"]["state"],
            zipcode=data["shipping"]["zipcode"],

        )
     # retun confirmation( you didnt console anywhere)
    return JsonResponse("PAyment Comlete", safe=False)
