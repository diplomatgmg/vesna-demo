document.addEventListener("DOMContentLoaded", () => {

    const productsContainer = document.querySelector(".index-product-cards-container");
    const urlParams = new URLSearchParams(window.location.search);

    if (document.querySelector('[data-page="index"]')) {
        if (urlParams.get("afterbuy") === "1") {
            localStorage.removeItem('cartItems');
            document.querySelector('.order-confirmation').classList.remove('hidden');
            console.log("afterbuy");
        }

        const closeIcon = document.querySelector(
            ".order-confirmation .close-icon"
        );
        const popup = document.querySelector(".order-confirmation");
        if (closeIcon) {
            closeIcon.addEventListener("click", () => {
                popup.classList.add("hidden");
            });
        }
    }

});
