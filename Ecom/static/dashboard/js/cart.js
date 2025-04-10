

document.querySelectorAll('.remove-cart').forEach(button => {
    button.addEventListener('click',function(){
        if (window.confirm("Are you sure you want to remove this item from the cart?")) {
            const id = parseInt(this.getAttribute('data-id'));

            fetch(`${window.location.origin}/remove_cart/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken':getCSRFToken()
                },
                body: JSON.stringify({
                    id:id,
                })
            })
            .then(response => response.json())
            .then( data => {
                console.log(`Message: ${data}`)
                const successMessageContainer = document.createElement('div');
                const successMessage = document.createElement('div');
                successMessage.textContent = 'Item removed from cart !';
                successMessage.className = 'message-success';
                successMessageContainer.className = 'message-container';
                successMessageContainer.prepend(successMessage);
                document.body.prepend(successMessageContainer);

                setTimeout(() => {
                    successMessage.remove();
                    window.location.href = window.location;
                }, 1500);
            })
            .catch(error => {
                console.error('Error adding item to cart:', error);
            });

            updateSubtotal();

            
        } })
})

function getCSRFToken() {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]');
    return csrfToken ? csrfToken.value : '';
}


document.querySelectorAll('.decrease').forEach(button => {
    button.addEventListener('click', function() {
        const id = parseInt(this.getAttribute('data-id'));
        const price = parseInt(this.getAttribute('data-price'));
        let productCount = document.getElementById(`product-count-${id}`);
        productCount.value = parseInt(productCount.value) - 1;

        if(productCount.value <= 0 )
        {
            productCount.value = 1;
        }
        let totalProductPrice = document.getElementById(`product-price-${id}`);
        totalProductPrice.innerHTML =`$ ${ (price * parseFloat(productCount.value)).toFixed(2) }`;
        updateSubtotal();
    });
});

document.querySelectorAll('.increase').forEach(button => {
    button.addEventListener('click', function() {
        const id = parseInt(this.getAttribute('data-id'));
        const price = parseFloat(this.getAttribute('data-price'));
        let productCount = document.getElementById(`product-count-${id}`);
        productCount.value = parseInt(productCount.value) + 1;

        if(productCount.value < 1 )
        {
            productCount.value = 1;
        }
        let totalProductPrice = document.getElementById(`product-price-${id}`);
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