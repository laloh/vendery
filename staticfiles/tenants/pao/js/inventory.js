const cardProducts = document.getElementsByClassName("card-body-product")
const clientID = document.getElementById("select-client")
const sellButton = document.getElementById('sell-button')

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
        }

        console.log(clientID.options[1].getAttribute('id'))
    })
}

// TODO: Send all the data to DJANGO
sellButton.onclick = function () {
    // var token = document.getElementById("token").value;
    // var url = "/inventory/nota-remision/" + token + "/"

    // Selects the id value of client selected
    order['clientID'] = parseInt(clientID.options[1].getAttribute('id'))
    if (order['clientID'] === null) {
        alert("Seleciona cliente a vender productos")
        return
    }


    console.log(order)

    // fetch(url, {
    //     method: 'POST',
    //     headers: {
    //         'Content-Type': 'application/json'
    //         // 'X-CSRFToken': csrftoken,
    //     },
    //     body: JSON.stringify(order)
    // })
    //     .then((response) => {
    //         return response.json();
    //     })
    //     .then((data) => {
    //         location.reload()
    //     });

}