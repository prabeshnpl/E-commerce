// Cart functionality
let cart = [];
        
// Navigation
document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', function(e) {
        e.preventDefault();
        const page = this.getAttribute('data-page');
        
        if (page === 'home') {
            document.getElementById('homepage').classList.remove('hidden');
            document.getElementById('cartPage').classList.remove('active');
        } else {
            // In a real implementation, we'd handle other pages too
        }
    });
});

// Add "View Cart" functionality
document.querySelector('.shop-now-btn').addEventListener('click', function() {
    document.getElementById('homepage').classList.add('hidden');
    document.getElementById('cartPage').classList.add('active');
    renderCart();
});

document.querySelector('.my-cart-btn').addEventListener('click', function() {
    document.getElementById('homepage').classList.add('hidden');
    document.getElementById('cartPage').classList.add('active');
    renderCart();
});

// Add to Cart functionality
document.querySelectorAll('.add-to-cart-btn').forEach(button => {
    button.addEventListener('click', function() {
        const id = parseInt(this.getAttribute('data-id'));
        const name = this.getAttribute('data-name');
        const price = parseFloat(this.getAttribute('data-price'));
        const image = this.getAttribute('data-image');
        
        // Check if product is already in cart
        const existingItem = cart.find(item => item.id === id);
        
        if (existingItem) {
            existingItem.quantity += 1;
        } else {
            cart.push({
                id: id,
                name: name,
                price: price,
                image: image,
                quantity: 1
            });
        }
        
        alert('Product added to cart!');
    });
});

// Render cart function
function renderCart() {
    const cartItemsContainer = document.getElementById('cartItems');
    cartItemsContainer.innerHTML = '';
    
    let subtotal = 0;
    
    if (cart.length === 0) {
        cartItemsContainer.innerHTML = '<tr><td colspan="4">Your cart is empty</td></tr>';
    } else {
        cart.forEach(item => {
            const total = item.price * item.quantity;
            subtotal += total;
            
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>
                    <div class="cart-product">
                        <div class="cart-product-image">
                            <img src="${item.image}" alt="${item.name}">
                        </div>
                        <div>
                            <h3>${item.name}</h3>
                        </div>
                    </div>
                </td>
                <td>$${item.price.toFixed(2)}</td>
                <td>
                    <div class="quantity-control">
                        <button class="quantity-btn decrease" data-id="${item.id}">-</button>
                        <input type="text" class="quantity-input" value="${item.quantity}" readonly>
                        <button class="quantity-btn increase" data-id="${item.id}">+</button>
                    </div>
                </td>
                <td>$${total.toFixed(2)}</td>
            `;
            
            cartItemsContainer.appendChild(tr);
        });
    }
    
    document.getElementById('cartSubtotal').textContent = `$${subtotal.toFixed(2)}`;
    
    // Add event listeners to quantity buttons
    document.querySelectorAll('.decrease').forEach(button => {
        button.addEventListener('click', function() {
            const id = parseInt(this.getAttribute('data-id'));
            updateQuantity(id, -1);
        });
    });
    
    document.querySelectorAll('.increase').forEach(button => {
        button.addEventListener('click', function() {
            const id = parseInt(this.getAttribute('data-id'));
            updateQuantity(id, 1);
        });
    });
}

// Update quantity function
function updateQuantity(id, change) {
    const item = cart.find(item => item.id === id);
    
    if (item) {
        item.quantity += change;
        
        if (item.quantity <= 0) {
            // Remove item from cart
            cart = cart.filter(item => item.id !== id);
        }
        
        renderCart();
    }
}

// Initialize the page with some items in the cart for demo
window.addEventListener('DOMContentLoaded', function() {
    // Add some sample items to cart
    cart = [
        {id: 1, name: 'Product Name', price: 49.00, image: '/api/placeholder/150/150', quantity: 1},
        {id: 2, name: 'Product Name', price: 19.00, image: '/api/placeholder/150/150', quantity: 1},
        {id: 3, name: 'Product Name', price: 59.00, image: '/api/placeholder/150/150', quantity: 1}
    ];
});