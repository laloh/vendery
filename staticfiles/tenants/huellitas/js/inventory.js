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
        var sumTotal = 0
        for (let key in sumTotalAmount) {
            sumTotal += Object.values(sumTotalAmount[key]).reduce((a, b) => a + b, 0)
        }

        order.sumTotalAmount = sumTotal
        totalAmount.innerText = "Total: $"+ order.sumTotalAmount +".00"
    });
}

$("#product-cart").click(function (e){
    var table_rows = []
    var productModalID = 0
    for (let productID in order['products']) {
        for (let productSize in order['products'][productID]) {
            const productName = order['products'][productID][productSize].name;
            const productPrice = order['products'][productID][productSize].price;
            const productQuantity = order['products'][productID][productSize].quantity;
            const productSubtotal = order['products'][productID][productSize].subtotal;

            table_rows.push(`
                <tr id="product-${productModalID}">
                    <td class="tg-1pky">${productID}</td>
                    <td class="tg-1pky">${productName}</td>
                    <td class="tg-1pky">$ ${productPrice}.00 MXN</td>
                    <td class="tg-1pky">${productSize}</td>
                    <td class="tg-1pky">${productQuantity}</td>
                    <td class="tg-1lax">$ ${productSubtotal}.00 MXN</td>
                    <td class="tg-1lax">
                        <button type="button" 
                                class="btn btn-danger delete-product" 
                                id="${productModalID}-${productID}-${productSize}">
                        Borrar
                        </button>
                    </td>
                </tr>`
            )

            productModalID++;
        }
    }

    $(".cart-modal-table-body").html(table_rows.join(''))
    $("#cart-modal").modal('show');

    // Delete button event handler
    $('.delete-product').each(function (){
        var deleteButton = this;
        deleteButton.addEventListener("click", function (){
            // Delete product from order json i.e. productID-ProductSize
            let productIDSize = deleteButton.id.split("-")
            let productModalID = productIDSize[0]
            let productID = productIDSize[1]
            let productSize = productIDSize[2]

            $(`#product-${productModalID}`).remove()

            // Test when all sizes from products are deleted
            delete order['products'][productID][productSize]
            delete sumTotalAmount[productID][productSize]

            // TODO: Create function for do the sum (above there are the same code)
            var sumTotal = 0
            for (let key in sumTotalAmount) {
                sumTotal += Object.values(sumTotalAmount[key]).reduce((a, b) => a + b, 0)
            }

            order.sumTotalAmount = sumTotal
            totalAmount.innerText = "Total: $"+ order.sumTotalAmount +".00"
        });
    });
});


$("#continue-button").click(function (){
   $("#cart-modal").modal('hide');
});

$("#send-note-button").click(function (e){
    let pdf_url = $(this).attr('data-pdf')
    let client_id = $(this).attr('data-client')
    console.log(client_id)
    let body = {"pdf_url": pdf_url, "client_id": client_id}
    if(!confirm('Esta seguro de enviar nota por SMS?')) {
        return
    }

    $.ajax({
        type: 'POST',
        url: '/inventory/send-note/',
        data: JSON.stringify(body),
        success: function (data){
            if (data.status == 200) {
                alert("Nota enviado al cliente con éxito!")
                window.location = '/inventory/mis-ventas/'
            }
        }
    });
});

$("#sell-button").click(function (e){
    e.preventDefault()
    const clientID = $("#select-client option:selected").val()
    if (clientID == "Cliente a vender") {
        alert("Seleciona cliente a vender productos")
        return
    }
    order['clientID'] = clientID

    $.ajax({
        type: 'POST',
        url: '/inventory/nota-remision/',
        data: JSON.stringify(order),
        success: function (data){
            if (data.status == 200) {
                alert("La venta se ha realizado con exito!")
                window.location = '/inventory/mis-ventas/'
            }
        }
    });
});


