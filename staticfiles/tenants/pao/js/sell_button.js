var increaseTotalOne = document.getElementsByClassName('increase-total-1')
var decreaseTotalOne = document.getElementsByClassName('decrease-total-1')
var increaseTotalSix = document.getElementsByClassName('increase-total-6')
var decreaseTotalSix = document.getElementsByClassName('decrease-total-6')
var increaseTotalTwelve = document.getElementsByClassName('increase-total-12')
var decreaseTotalTwelve = document.getElementsByClassName('decrease-total-12')


var totalAmount = document.getElementById("total-amount")
var sellButton = document.getElementById('sell-button')
var clientID = document.getElementById("select-client")
var quantity = document.getElementsByClassName("quantity")


var order = {
	"sumTotalAmount": 0.0,
	"products": {}
}

function setTextTotalAmount(element){
	order.sumTotalAmount = parseFloat(order.sumTotalAmount.toFixed(2))
	if (order.sumTotalAmount <= 0) {
		order.sumTotalAmount = 0
	}
	element.innerHTML = "Total: $" + order.sumTotalAmount + " MX"
}

function increaseHandler(i, id, price, name, increment){
    var productID = id
	var productPrice = parseFloat(price)
	var productName = name

	order.sumTotalAmount += productPrice * increment
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

	order.products[productID].quantity += increment
	order.products[productID].subtotal += productPrice * increment

	// Not permit zero values
	if (order.products[productID].quantity <= 0) {
		order.products[productID].quantity = 0
		order.products[productID].subtotal = 0
	}

	quantity[i].innerText = order.products[productID].quantity + " Uds"
}

function decreaseHandler(i, id, price, name, increment){
	var productID = id
	var productPrice = parseFloat(price)
	var productName = name

	order.sumTotalAmount -= productPrice * increment
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

	order.products[productID].quantity -= increment
	order.products[productID].subtotal -= productPrice * increment

	// Not permit zero values
	if (order.products[productID].quantity <= 0) {
		order.products[productID].quantity = 0
		order.products[productID].subtotal = 0
	}

	quantity[i].innerText = order.products[productID].quantity + " uds"
}


for (let i = 0; i < increaseTotalOne.length; i++) {
	increaseTotalOne[i].addEventListener('click', function (){
		increaseHandler(i, this.dataset.id, this.dataset.price, this.dataset.name, 1)
	})

	increaseTotalSix[i].addEventListener('click', function (){
		increaseHandler(i, this.dataset.id, this.dataset.price, this.dataset.name, 6)
	})

	increaseTotalTwelve[i].addEventListener('click', function (){
		increaseHandler(i, this.dataset.id, this.dataset.price, this.dataset.name, 12)
	})
}

for (let i = 0; i < decreaseTotalOne.length; i++) {
	decreaseTotalOne[i].addEventListener('click', function (){
		decreaseHandler(i, this.dataset.id, this.dataset.price, this.dataset.name, 1)
	})

	decreaseTotalSix[i].addEventListener('click', function (){
		decreaseHandler(i, this.dataset.id, this.dataset.price, this.dataset.name, 6)
	})

	decreaseTotalTwelve[i].addEventListener('click', function (){
		decreaseHandler(i, this.dataset.id, this.dataset.price, this.dataset.name, 12)
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
