let increaseTotal = document.getElementsByClassName('increase-total')
var decreaseTotal = document.getElementsByClassName('decrease-total')
var totalAmount = document.getElementById("total-amount")
var sellButton = document.getElementById('sell-button')
var clientID = document.getElementById("select-client")


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
	})
}


sellButton.onclick = function () {
	var url = '/inventory/nota-remision/'

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
