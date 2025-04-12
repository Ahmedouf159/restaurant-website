document.addEventListener("DOMContentLoaded", function () {

    // Mobile Menu Toggle
    const mobileMenuButton = document.getElementById("mobile-menu-button");
    const mobileMenu = document.getElementById("mobile-menu");

    if (mobileMenuButton) {
        mobileMenuButton.addEventListener("click", function () {
            mobileMenu.classList.toggle("show");
        });
    }

    // User Profile Dropdown
    const profileButton = document.querySelector(".profile-icon");
    const dropdownMenu = document.querySelector(".dropdown-menu");

    if (profileButton) {
        profileButton.addEventListener("click", function (event) {
            dropdownMenu.classList.toggle("active");
            event.stopPropagation(); // Prevent closing when clicking inside
        });

        document.addEventListener("click", function (event) {
            if (!profileButton.contains(event.target) && !dropdownMenu.contains(event.target)) {
                dropdownMenu.classList.remove("active");
            }
        });
    }

    // Cart Functionality
    let cart = [];

    function showQuantityPopup(name, price) {
        // Create a popup div
        let popup = document.createElement("div");
        popup.id = "quantityPopup";
        popup.innerHTML = `
            <div class="popup-content">
                <h3>Choose Quantity for ${name}</h3>
                <input type="number" id="quantityInput" min="1" value="1">
                <button onclick="addToCart('${name}', '${price}')">Add to Cart</button>
                <button onclick="closePopup()">Close</button>
            </div>
        `;
        popup.classList.add("popup");
        document.body.appendChild(popup);
    }
    
    function closePopup() {
        let popup = document.getElementById("quantityPopup");
        if (popup) {
            popup.remove();
        }
    }
    
    function addToCart(name, price) {
        let quantity = document.getElementById("quantityInput").value;
        quantity = parseInt(quantity);
    
        // Check if item already exists in the cart
        let existingItem = cart.find(item => item.name === name);
        if (existingItem) {
            existingItem.quantity += quantity;
        } else {
            cart.push({ name, price, quantity });
        }
    
        updateCartCount();
        closePopup();
        saveCartToLocalStorage();
    }
    
    function updateCartCount() {
        let cartCount = document.getElementById("cartCount");
        let totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);
        cartCount.innerText = totalItems;
    }
    
    function saveCartToLocalStorage() {
        localStorage.setItem("cart", JSON.stringify(cart));
    }
    
    function loadCartFromLocalStorage() {
        let storedCart = localStorage.getItem("cart");
        if (storedCart) {
            cart = JSON.parse(storedCart);
            updateCartCount();
        }
    }
    
    window.onload = function() {
        loadCartFromLocalStorage();
    };
    
    document.querySelectorAll(".btn-primary").forEach(button => {
        button.addEventListener("click", function () {
            const name = this.getAttribute("data-name");
            const price = parseFloat(this.getAttribute("data-price"));
            addToCart(name, price);
        });
    });

    document.getElementById("cart-items").addEventListener("click", function (event) {
        if (event.target.classList.contains("remove-btn")) {
            const index = event.target.getAttribute("data-index");
            cart.splice(index, 1);
            updateCartDisplay();
        }
    });

    document.getElementById("checkout-btn").addEventListener("click", function () {
        if (cart.length === 0) {
            alert("Your cart is empty!");
            return;
        }

        let finalTotal = cart.reduce((sum, item) => sum + item.price * item.quantity, 0);
        alert(`Your final total is $${finalTotal.toFixed(2)}`);
        cart = [];
        updateCartDisplay();
    });

});
let cart = JSON.parse(localStorage.getItem("cart")) || [];
document.getElementById("cart-count").innerText = cart.length;

function showQuantityPopup(name, price) {
    document.getElementById("popup-item-name").innerText = name;
    document.getElementById("popup-item-price").innerText = price;
    document.getElementById("quantity-popup").style.display = "block";
}

function closePopup() {
    document.getElementById("quantity-popup").style.display = "none";
}

function addToCart() {
    let name = document.getElementById("popup-item-name").innerText;
    let price = parseFloat(document.getElementById("popup-item-price").innerText);
    let quantity = parseInt(document.getElementById("quantity").value);

    let existingItem = cart.find(item => item.name === name);
    if (existingItem) {
        existingItem.quantity += quantity;
    } else {
        cart.push({ name, price, quantity });
    }

    localStorage.setItem("cart", JSON.stringify(cart));
    document.getElementById("cart-count").innerText = cart.length;
    closePopup();
}

function goToCart() {
    window.location.href = "/cart";
}
