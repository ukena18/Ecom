// get all the button which has update cart class
var updateBtns = document.getElementsByClassName("update-cart")

// for loop all of them and add click event to the
for (var i = 0;i<updateBtns.length; i++){
    // that is how you are add click event to a element
    updateBtns[i].addEventListener("click",function(){
        // productid and action come from datasets
        // html has custom attribute if you do data-product
        // data-product="{{item.product.id}}" data-action="add"
        var productId = this.dataset.product
        var action = this.dataset.action
        
        
        // console.log("productId:",productId,"action: ",action)
        // console.log("USer:",user)
        // if it is anonymoususer instead of database use cookies 
        // so you can still keep cart even after you refresh page
        if(user==="AnonymousUser"){
            // send product and action to cart cookie
            addCookieItem(productId,action)
        }else{
            // if user is already logged in update database 
            updateUserOrder(productId,action)
        }
    })

}

// if it is anonymoususer instead of database use cookies 
// so you can still keep cart even after you refresh page
function addCookieItem(productId,action){
    // if action is add check if it is already exist if not create quantity
    
    if(action=="add"){
        if (cart[productId] == undefined){
            cart[productId]={"quantity":1}
        }
        else{
            // if it is exist just add +1
            cart[productId]["quantity"] += 1
        }
    }
    // if action is remove start to reduce if it is zero just delete it 
    if(action=="remove"){
        cart[productId]["quantity"] -= 1
        if (cart[productId]["quantity"] <= 0){
            // that is how you delete key,value pair from a dict
            delete cart[productId]
        }
       
    }

    // console.log("cartjs:",cart)
    // add that cart data to cookie 
    // ";domain=;path=/" means even after you reload or redirect diff pafe it still keeo the cookie
    document.cookie = "cart="+JSON.stringify(cart)+ ";domain=;path=/"
    // reload page 
    location.reload();
}

// if user register run updateuser func
// send post request to backend
function updateUserOrder(productId,action){
    // console.log("user logged in sending data..")
    // url 
    var url = "/update_item/"
    // fetch api
    fetch(url,{
        method:"POST",
        headers:{
            "Content-Type": "application/json",
            'X-CSRFToken': csrftoken
        },
        // you gotta stringfy all the time and parse it back
        body:JSON.stringify({"productId":productId,"action":action})
    })
    // get the stringfy json respnse
    // turn into javascript dict
    .then((response)=>{
            return response.json()
    })
    // refresh page
    .then((data)=>{
        // console.log("data",data)
        location.reload()
    })

}