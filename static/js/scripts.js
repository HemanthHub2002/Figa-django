// Cart handling

// Add to cart

const products_container = document.getElementById('products-container');

const cart_count = document.getElementById("cart-count");

const csrfToken = document.querySelector("[name = csrfmiddlewaretoken]").value

// Load current Value
async function loadCartCount() {
    const countUrl = cart_count.dataset.countUrl;
    try {
        const result = await fetch(countUrl);
        const data = await result.json();
        cart_count.innerText = data.cart_count;

    }
    catch (error) {
        console.error(`Cart count fetch error: ${error}`)
    }
}
if (cart_count) {
    loadCartCount();
}

// add to cart url 
if (products_container) {
    const addUrl = products_container.dataset.addUrl;
    // adding event listener onto product cards through their parent container

    products_container.addEventListener('click', async function (event) {

        if (!event.target.classList.contains('add-to-cart')) {
            return;
        }

        const btn = event.target;
        const product_card = btn.closest(".product-card");
        const productId = product_card.dataset.productId;

        // Include size if selected
        let bodyContent = `product_id=${productId}`;
        const sizeInput = product_card.querySelector('input[name="size"]:checked');
        if (sizeInput) {
            bodyContent += `&size=${sizeInput.value}`;
        }

        btn.disabled = true;
        btn.innerText = "Adding...";

        // try to make a POST request
        try {
            const response = await fetch(addUrl, {
                method: "POST",
                headers: {
                    'X-CSRFToken': csrfToken,
                    "Content-Type": "application/x-www-form-urlencoded"
                },
                body: bodyContent
            })
            const data = await response.json();

            // if the backend returns 401 status,
            if (response.status === 401 && data.redirect_url) {
                window.location.href = data.redirect_url;
                return;
            }

            if (data.cart_count !== undefined) {
                cart_count.innerText = data.cart_count;
            }
        }
        catch (error) {
            console.error("Cart error:", error);
        }
        finally {
            btn.disabled = false;
            btn.innerText = "Add to Cart";
        }
    });
}




// Increase and Decrease Functions
const cartContainer = document.querySelector('.cart-container');

if (cartContainer) {
    cartContainer.addEventListener('click', async function (e) {
        // Handle clicks on buttons or elements inside buttons (like icons)
        const target = e.target.closest('button') || e.target;

        const productId = target.dataset.productId;
        const size = target.dataset.size;

        if (!productId) return;

        let url = '';

        if (target.classList.contains('increase')) {
            url = '/cart/increase/';
        } else if (target.classList.contains('decrease')) {
            url = '/cart/decrease/';
        } else if (target.classList.contains('remove-btn')) {
            url = '/cart/remove/';
        } else {
            return;
        }

        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: `product_id=${productId}&size=${size || ''}`
        });

        if (response.ok) {
            location.reload();
        }
    });
}








// Add to cart Notification
(() => {
    const count = document.getElementById("cart-count");
    const toast = document.getElementById("cart-toast");
    if (!count || !toast) return;

    let prev = parseInt(count.innerText) || 0;
    let added = false;

    document.addEventListener("click", e => {
        if (e.target.classList.contains("add-to-cart")) added = true;
    });

    new MutationObserver(() => {
        const curr = parseInt(count.innerText) || 0;

        if (added && curr > prev) {
            toast.classList.add("show");
            setTimeout(() => toast.classList.remove("show"), 1800);
            added = false;
        }

        prev = curr;
    }).observe(count, { childList: true });
})();