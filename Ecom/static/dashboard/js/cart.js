
document.querySelectorAll('.decrease').forEach(button => {
    button.addEventListener('click', function() {
        const id = parseInt(this.getAttribute('data-id'));
        const price = parseInt(this.getAttribute('data-price'));
        productCount = document.getElementById(`product-count-${id}`);
        productCount.value = parseInt(productCount.value) - 1;

        if(productCount.value < 0 )
        {
            productCount.value = 0;
        }
        totalProductPrice = document.getElementById(`product-price-${id}`);
        totalProductPrice.innerHTML =`$ ${ (price * parseFloat(productCount.value)).toFixed(2) }`;
        updateSubtotal();
    });
});

document.querySelectorAll('.increase').forEach(button => {
    button.addEventListener('click', function() {
        const id = parseInt(this.getAttribute('data-id'));
        const price = parseFloat(this.getAttribute('data-price'));
        productCount = document.getElementById(`product-count-${id}`);
        productCount.value = parseInt(productCount.value) + 1;

        if(productCount.value <0 )
        {
            productCount.value = 0;
        }
        totalProductPrice = document.getElementById(`product-price-${id}`);
        totalProductPrice.innerHTML =`$ ${ (price * parseFloat(productCount.value)).toFixed(2) }`;
        updateSubtotal();
    });
});

window.addEventListener('DOMContentLoaded',() => {
    updateSubtotal();
})

function updateSubtotal() {
    let subtotal = 0;
    document.querySelectorAll('.quantity-input').forEach(input => {
        const id = input.getAttribute('id').split('-')[2]; // Extract product ID
        const price = parseFloat(document.querySelector(`.quantity-btn[data-id="${id}"]`).getAttribute('data-price'));
        const quantity = parseInt(input.value);
        subtotal += price * quantity;
        document.getElementById(`product-price-${id}`).innerText = `$${subtotal.toFixed(2)}`;
    });

    let grandTotal = 0;
    document.querySelectorAll('.all-prices').forEach( price => {
        let aprice = price.innerHTML.split('$')[1];
        grandTotal = (parseFloat(grandTotal) + parseFloat(aprice)).toFixed(2);
    })
    document.getElementById('cartSubtotal').innerText = `$${grandTotal}`;
}