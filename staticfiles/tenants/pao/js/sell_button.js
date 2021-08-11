let increaseTotal = document.getElementsByClassName('increase-total')
var decreaseTotal = document.getElementsByClassName('decrease-total')
var totalAmount = document.getElementById("total-amount")
var sellButton = document.getElementById('sell-button')
var clientID = document.getElementById("select-client")
var quantity = document.getElementsByClassName("quantity")
var allProducts = document.getElementsByClassName("all-products")
var searchInput = document.getElementById("search-product")
var divToRenderProducts = document.getElementById("div-to-render-products")

var order = {
	"sumTotalAmount": 0.0,
	"products": {}
}

// ------------------------
//	Search input handlers
// ------------------------

var allProductsName = []
var productCardBody = []
for (let i = 0; i < allProducts.length; i++) {
	productCardBody[i] = allProducts[i]
	allProductsName[i] = allProducts[i].getElementsByClassName("product-name")[0].innerHTML
}

/*
* Some ideas i have in mind:
* 	1. Write a function to save the state of card product
* 	2. It need to be modified and save by `sell button handler`
* 	3. This function need to pass the element to be modified
* 	4. When the match is made, it need to call the object
* */

var filteredArray = []
searchInput.addEventListener('keyup', (e)=>{
    divToRenderProducts.innerHTML = ""
	filteredArray = allProductsName.filter(info => info.includes(e.target.value))
	if (filteredArray.length > 0) {
		divToRenderProducts.innerHTML += productCardBody[0].innerHTML
	} else {
		divToRenderProducts.innerHTML = "No existe el producto que buscas! :("
	}
})

// ------------------------
//	Sell button handlers
// ------------------------


function setTextTotalAmount(element){
	order.sumTotalAmount = parseFloat(order.sumTotalAmount.toFixed(2))
	if (order.sumTotalAmount <= 0) {
		order.sumTotalAmount = 0
	}
	element.innerHTML = "Total: $" + order.sumTotalAmount + " MX"
}


for (let i = 0; i < increaseTotal.length; i++) {
	increaseTotal[i].addEventListener('click', function (){
		var productID = this.dataset.id
		var productPrice = parseFloat(this.dataset.price)
		var productName = this.dataset.name

		order.sumTotalAmount += productPrice
		setTextTotalAmount(totalAmount)

		if (!order.products.hasOwnProperty(productID)) {
			order.products[productID] = {
				"name": productName,
				"quantity":0,
				"subtotal":0,
				"price": productPrice
			}
			console.log(order)
		}

		order.products[productID].quantity += 1
		order.products[productID].subtotal += productPrice

		// Not permit zero values
		if (order.products[productID].quantity <= 0) {
			order.products[productID].quantity = 0
			order.products[productID].subtotal = 0
		}

		quantity[i].innerText = order.products[productID].quantity

	})
}

for (let i = 0; i < decreaseTotal.length; i++) {
	decreaseTotal[i].addEventListener('click', function (){
		var productID = this.dataset.id
		var productPrice = parseFloat(this.dataset.price)
		var productName = this.dataset.name

		order.sumTotalAmount -= productPrice
		setTextTotalAmount(totalAmount)

		if (!order.products.hasOwnProperty(productID)) {
			order.products[productID] = {
				"name": productName,
				"quantity":0,
				"subtotal":0,
				"price": productPrice
			}
			console.log(order)
		}

		order.products[productID].quantity -= 1
		order.products[productID].subtotal -= productPrice

		// Not permit zero values
		if (order.products[productID].quantity <= 0) {
			order.products[productID].quantity = 0
			order.products[productID].subtotal = 0
		}

		quantity[i].innerText = order.products[productID].quantity

	})
}


sellButton.onclick = function () {
	var token=document.getElementById("token").value;
	var url = "/inventory/nota-remision/" + token +"/"

	order['clientID'] = clientID
						.options[clientID.selectedIndex]
						.getAttribute('value')

	fetch(url, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json'
			// 'X-CSRFToken': csrftoken,
		},
		body: JSON.stringify(order)
	})
		.then((response) => {
			return response.json();
		})
		.then((data) => {
			location.reload()
		});
}
