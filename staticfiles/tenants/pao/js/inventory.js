var order = {
	"sumTotalAmount": 0.0,
	"products": {}
}

let cardProducts = document.getElementsByClassName("card-body-product")
for (let i=0; i < cardProducts.length; i++){

	var addButton = cardProducts[i].getElementsByClassName('button-add')[0]
	addButton.addEventListener('click', function (){
		var productSize = cardProducts[i].getElementsByClassName("product-size")[0].value
		var productQuantity= cardProducts[i].getElementsByClassName("product-quantity")[0].value

	})


}
