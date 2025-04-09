
// Initialize the page with some items in the cart for demo
window.addEventListener('DOMContentLoaded', function() {

        //Mobile functionality

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
                        <button class="add-to-cart-btn" data-id="${product.id}" data-name="${product.name}" data-price="${product.price}" data-image="${product.image}" >Add to Cart</button>
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

    loadMoreProducts();


});
