const cardProducts = document.getElementsByClassName("card-body-product")
var totalAmount = document.getElementById('total-amount')


var order = {
    "sumTotalAmount": null,
    "products": {}
}

var sumTotalAmount = {}

for (let i = 0; i < cardProducts.length; i++) {
    const addButton = cardProducts[i].getElementsByClassName('button-add')[0];
    addButton.addEventListener('click', function () {
        const productSize = cardProducts[i].getElementsByClassName("product-size")[0].value;
        const productQuantity = parseInt(cardProducts[i].getElementsByClassName("product-quantity")[0].value);
        const productPrice = parseFloat(this.dataset.price);
        const productID = parseInt(this.dataset.productid);
        const productName = this.dataset.productname;

        if (!order.products.hasOwnProperty(productID)) {
            order.products[productID] = {}
            sumTotalAmount[productID] = {}
        }

        if (!order.products[productID].hasOwnProperty(productSize)) {
            order.products[productID][productSize] = {
                "name": productName,
                "quantity": 0,
                "subtotal": 0,
                "price": productPrice
            }
        }

        order.products[productID][productSize].quantity = productQuantity
        order.products[productID][productSize].subtotal = productQuantity * productPrice
        sumTotalAmount[productID][productSize] = order.products[productID][productSize].subtotal

        // Sum all subtotals of every product
        for (let key in sumTotalAmount) {
            order.sumTotalAmount = Object.values(sumTotalAmount[key]).reduce((a, b) => a + b, 0)
            totalAmount.innerText = "Total: $"+ order.sumTotalAmount +".00"
        }
    })
}

$("#sell-button").click(function (e){
    e.preventDefault()
    const clientID = $("#select-client option:selected").val()
    if (clientID == "Cliente a vender") {
        alert("Seleciona cliente a vender productos")
        return
    }
    order['clientID'] = clientID
    console.log(JSON.stringify(order))

    $.ajax({
        type: 'POST',
        url: '/inventory/nota-remision/',
        data: JSON.stringify(order),
        success: function (data){
            if (data.status == 200) {
                console.log("Redirecting to the mis-ventas man")
                // window.location = '/inventory/mis-ventas/'
            }
    }
    });
});