document.body.addEventListener('click', (event) => {
    const productCard = event.target.closest('.cart-item');
    if (event.target.classList.contains('bi-trash')) {
        if (window.confirm("Are you sure you want to remove this item from the cart?")) {
            const id = parseInt(productCard.getAttribute('data-id'));

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
        }
    }

    else if (productCard) {
        const id = parseInt(productCard.getAttribute('data-id'));
        window.location.href = `${window.location.origin}/products/${id}`;
    }
});

function getCSRFToken() {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]');
    return csrfToken ? csrfToken.value : '';
}


document.querySelectorAll('.decrease').forEach(button => {
    button.addEventListener('click', function() {
        const id = parseInt(this.getAttribute('data-id'));
        const price = parseFloat(this.getAttribute('data-price'));
        let productCount = document.getElementById(`product-count-${id}`);
        productCount.value = parseInt(productCount.value) - 1;

        if (productCount.value <= 0) {
            productCount.value = 1;
        }

        let totalProductPrice = document.getElementById(`product-price-${id}`);
        totalProductPrice.innerHTML = `$${(price * parseFloat(productCount.value)).toFixed(2)}`;
        updateGrandTotal(); // Update the grand total after modifying the product count
    });
});

document.querySelectorAll('.increase').forEach(button => {
    button.addEventListener('click', function() {
        const id = parseInt(this.getAttribute('data-id'));
        const price = parseFloat(this.getAttribute('data-price'));
        let productCount = document.getElementById(`product-count-${id}`);
        productCount.value = parseInt(productCount.value) + 1;

        let totalProductPrice = document.getElementById(`product-price-${id}`);
        totalProductPrice.innerHTML = `$${(price * parseFloat(productCount.value)).toFixed(2)}`;
        updateGrandTotal(); // Update the grand total after modifying the product count
    });
});

function updateGrandTotal() {
    let grandTotal = 0;
    document.querySelectorAll('.all-prices').forEach(price => {
        let aprice = price.innerHTML.split('$')[1];
        grandTotal += parseFloat(aprice);
    });
    document.getElementById('cartSubtotal').innerText = `$${grandTotal.toFixed(2)}`;
}

window.addEventListener('DOMContentLoaded', () => {
    updateGrandTotal();
    document.getElementById('checkout-btn').addEventListener('click',()=>{
        document.getElementById('overlay-payment').style.display = 'flex';
        document.getElementById('cartPage').style.color = 'flex';

    });
    document.getElementById('close-btn').addEventListener('click',()=>{
        document.getElementById('overlay-payment').style.display = 'none';
    });
    
    document.body.addEventListener('click', (event) => {
        if (event.target.classList.contains('cart-item')) {
            document.getElementById('overlay-payment').style.display = 'none';
        }
    });
});