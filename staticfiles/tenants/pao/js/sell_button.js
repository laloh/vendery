var increaseTotal = document.getElementsByClassName('increase-total')
var decreaseTotal = document.getElementsByClassName('decrease-total')
var totalAmount = document.getElementById("total-amount")



for (i = 0; i < increaseTotal.length; i++) {
	increaseTotal[i].addEventListener('click', function (){
		var productPrice = this.dataset.product['price']

		console.log('increaseTotal button %s', id)
		console.log(id)
	})
}

for (i = 0; i < decreaseTotal.length; i++) {
	decreaseTotal[i].addEventListener('click', function (){
		var id = this.dataset.product
		console.log('decrease button %s', id)
		console.log(id)
	})
}