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

    let currentPage = 1;
    const baseUrl = window.location.origin;
    const productContainer = this.document.getElementById('product-grid')
    
    // Fetches products using fetch and loads 20 per page/request
    function loadMoreProducts(){
        const spinner = document.getElementById('spinner')
        spinner.style.display = 'block';
        
        fetch(`${baseUrl}/products/?page=${currentPage}`)

        .then(response => response.json())
        .then(data => {
            data.products.forEach(product =>{
                const productCard = `
                <div class="product-card">
                    <div class="product-image">
                        <img src="${baseUrl}/media/${product.image}" alt="${product.name}">
                    </div>
                    <div class="product-info">
                        <h3 class="product-title">${product.name}</h3>
                        <p class="product-price">$${product.price}</p>
                        <button class="add-to-cart-btn" data-id="1" data-name="Product Name" data-price="49.00" data-image="/api/placeholder/150/150">Add to Cart</button>
                    </div>
                </div>
                `;
                productContainer.insertAdjacentHTML('beforeend',productCard);
            })
            spinner.style.display = 'none';
        })
        .catch(error => {
            console.error('Error fetching products:', error);
            // spinner.style.display = 'none';
        });
            currentPage++;
        }

    function loadCartProducts(){
        fetch(`${baseUrl}/cart_products`)
        .then(response => response.json)
        .then(data => {
            data.products.forEach(product => {
                const productCard = `
                <div class="product-card">
                    <div class="product-image">
                        <img src="${baseUrl}/media/${product.image}" alt="${product.name}">
                    </div>
                    <div class="product-info">
                        <h3 class="product-title">${product.name}</h3>
                        <p class="product-price">$${product.price}</p>
                        <button class="add-to-cart-btn" data-id="1" data-name="Product Name" data-price="49.00" data-image="/api/placeholder/150/150">Add to Cart</button>
                    </div>
                </div>
                `;
            })
        })
    }

    loadMoreProducts();
    
    // Add some sample items to cart
    // use fetchapi to fetch products in cart if necessary
    cart = [
        {id: 1, name: 'Product Name', price: 49.00, image: '/api/placeholder/150/150', quantity: 1},
        {id: 2, name: 'Product Name', price: 19.00, image: '/api/placeholder/150/150', quantity: 1},
        {id: 2, name: 'Product Name', price: 19.00, image: '/api/placeholder/150/150', quantity: 1},
        {id: 3, name: 'Product Name', price: 59.00, image: '/api/placeholder/150/150', quantity: 1}
    ];
});

//Mobile functionality

document.addEventListener('DOMContentLoaded', function() {
    const mobileMenuBtn = document.getElementById('mobileMenuBtn');
    const mainNav = document.getElementById('mainNav');
    
    if (mobileMenuBtn) {
        mobileMenuBtn.addEventListener('click', function() {
            mainNav.classList.toggle('active');
        });
    }
    
    // Close mobile menu when clicking on a nav link
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        link.addEventListener('click', function() {
            if (window.innerWidth <= 768) {
                mainNav.classList.remove('active');
            }
        });
    });
});