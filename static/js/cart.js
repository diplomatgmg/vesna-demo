function removeCartDuplicate() {
    let cartItems = JSON.parse(localStorage.getItem("cartItems")) || [];
    let newCartItems = [];
    cartItems.forEach((item) => {
        let isDuplicate = newCartItems.some(
            (newItem) =>
                newItem.product_id === item.product_id &&
                newItem.parameter_id === item.parameter_id
        );
        if (!isDuplicate) {
            newCartItems.push(item);
        }
    });
    localStorage.setItem("cartItems", JSON.stringify(newCartItems));
}

function checkIfProductExistsInCart(productID, parameterID) {
    let cartItems = JSON.parse(localStorage.getItem("cartItems")) || [];
    return cartItems.some(
        (item) =>
            item.product_id === productID && item.parameter_id === parameterID
    );
}

function addToCart(
    productId,
    parameterId,
    productName,
    parameterName,
    parameterString,
    colorName,
    productPrice,
    oldPrice,
    productImage
) {
    let cartItems = JSON.parse(localStorage.getItem("cartItems")) || [];
    cartItems.push({
        product_id: productId,
        parameter_id: parameterId,
        name: productName,
        parameter_name: parameterName,
        parameter_string: parameterString,
        color: colorName,
        price: productPrice,
        oldPrice: oldPrice,
        image: productImage,
        quantity: 1,
    });
    localStorage.setItem("cartItems", JSON.stringify(cartItems));
    removeCartDuplicate();
}
window.addToCart = addToCart;
window.checkIfProductExistsInCart = checkIfProductExistsInCart;

document.addEventListener("DOMContentLoaded", () => {
    const cartDataParameters = document.getElementById("cart-data-parameters");
    const paymentType = document.getElementById("payment_type");

    function getDeliveryPrice() {
        if (
            paymentType.value === "delivery" &&
            cartDataParameters.dataset.deliveryPriceOffline
        ) {
            return cartDataParameters.dataset.deliveryPriceOffline;
        } else {
            return cartDataParameters.dataset.deliveryPrice;
        }
    }
    function getPayOnDelivery() {
        if (
            paymentType.value === "delivery" &&
            cartDataParameters.dataset.deliveryPriceOffline
        )
            return true;
        return false;
    }

    function minusQuantity(index) {
        let cartItems = JSON.parse(localStorage.getItem("cartItems")) || [];
        if (cartItems[index].quantity > 1) cartItems[index].quantity--;
        localStorage.setItem("cartItems", JSON.stringify(cartItems));
    }

    function plusQuantity(index) {
        let cartItems = JSON.parse(localStorage.getItem("cartItems")) || [];
        cartItems[index].quantity++;
        localStorage.setItem("cartItems", JSON.stringify(cartItems));
    }

    function removeFromCart(index) {
        let cartItems = JSON.parse(localStorage.getItem("cartItems"));
        cartItems.splice(index, 1);
        localStorage.setItem("cartItems", JSON.stringify(cartItems));
    }

    function displayCartItems() {
        let cartItems = JSON.parse(localStorage.getItem("cartItems"));
        const productsAtCart = document.querySelector(".productsAtCart");

        if (!cartItems || cartItems.length < 1) {
            const cartHeaderEmptyBlock = document.querySelectorAll(
                ".cart-header-empty-block"
            );
            if (productsAtCart && cartHeaderEmptyBlock) {
                const cartRecomendBlock = document.querySelector(
                    "#cart-recomend-block"
                );
                const cartEmptyBlock =
                    document.getElementById("cart-empty-block");
                cartEmptyBlock.style.display = "block";
                productsAtCart.innerHTML = "";
                cartHeaderEmptyBlock.forEach((block) => {
                    block.style.display = "none";
                });
                cartRecomendBlock.style.display = "block";
            }
            return;
        }

        let itemsHtml = "";
        if (cartItems.length > 0) {
            for (let i in cartItems) {
                itemsHtml += `
                <div class="productCart">
                <button data-index="${i}" class="removeItem">
                    <img src="/static/img/other/close.svg" alt="close">
                </button>
                <div class="leftSide">
                <img src="${
                    cartItems[i].image
                        ? cartItems[i].image
                        : "/static/img/other/no_image.png"
                }" alt="product">
                </div>
                <div class="rightSide">

                <div>
                <div class="productCartName">
                    ${cartItems[i].name}
                </div>
                <div class="productCartParameter">
                    ${cartItems[i].parameter_string}
                </div>
                `;
                if (cartItems[i].color) {
                    itemsHtml += `
                <div class="productCartColorBlock">
                    <div class="productCartColor">Цвет: </div>
                    <div class="cart-product-parameter-color" style="background-color: ${cartItems[i].color};"></div>
                </div>`;
                }
                itemsHtml += `
                <div class="productCartPrice">
                    <span>${
                        cartItems[i].price * cartItems[i].quantity
                    } ₽</span>`;
                if (cartItems[i].oldPrice) {
                    itemsHtml += `&nbsp;<span class="productCartOldPrice">${
                        cartItems[i].oldPrice * cartItems[i].quantity
                    } ₽</span>`;
                }
                itemsHtml += `
                </div>
                </div>

                <div class="productCartCount">
                    <button data-index="${i}" class="minusItem">-</button>
                    <span class="countNumber">${cartItems[i].quantity}</span>
                    <button data-index="${i}" class="plusItem">+</button>
                </div>
                </div>
                </div>`;
            }

            productsAtCart.innerHTML = itemsHtml;

            document.querySelectorAll(".removeItem").forEach((e) => {
                e.addEventListener("click", (el) => {
                    removeFromCart(e.dataset.index);
                    displayCartItems();
                    updateSummaryBlock();
                });
            });
            document.querySelectorAll(".minusItem").forEach((e) => {
                e.addEventListener("click", (el) => {
                    minusQuantity(el.target.dataset.index);
                    displayCartItems();
                    updateSummaryBlock();
                });
            });
            document.querySelectorAll(".plusItem").forEach((e) => {
                e.addEventListener("click", (el) => {
                    plusQuantity(el.target.dataset.index);
                    displayCartItems();
                    updateSummaryBlock();
                });
            });
            const dataToSend = cartItems.map((item) => ({
                product_id: item.product_id,
                parameter_id: item.parameter_id,
                quantity: item.quantity,
            }));
            document.getElementById("productsData").value =
                JSON.stringify(dataToSend);
        }
    }

    function updateSummaryBlock() {
        const cartItems = JSON.parse(localStorage.getItem("cartItems"));

        const sumWithDiscount = document.querySelector(".withDiscount");
        const sumOfDiscount = document.querySelector(".discount");
        const discountBlock = document.querySelector("#cart-dicount-block");
        const finalPriceElement = document.querySelector(".finalPriceSpan");

        const deliveryPriceElement = document.querySelector(".delivery");
        const itemsCountField = document.querySelector(".summaryCount");
        const deliveryPrice = getDeliveryPrice();

        let totalSum = 0;
        let totalItems = 0;
        let discount = 0;

        if (cartItems) {
            cartItems.forEach((item) => {
                totalItems += item.quantity;
                totalSum += item.price * item.quantity;
            });
        }

        if (cartDataParameters.dataset.actionsP23) {
            const [num1, num2, ...rest] =
                cartDataParameters.dataset.actionsP23.split(":");
            const d1 = parseInt(num1);
            const d2 = parseInt(num2);
            if (!isNaN(d1) && d1 > 0 && !isNaN(d2) && d2 > 0) {
                if (totalItems > 2) {
                    discount = Math.round((totalSum / 100) * d2);
                } else if (totalItems === 2) {
                    discount = Math.round((totalSum / 100) * d1);
                }
            }
        }

        if (discount === 0) {
            discountBlock.style.display = "none";
        } else {
            discountBlock.style.display = "flex";
        }
        deliveryPriceElement.innerHTML = deliveryPrice + " ₽";
        sumOfDiscount.innerHTML = discount + " ₽";
        sumWithDiscount.innerHTML = Math.round(totalSum - discount) + " ₽";

        if (getPayOnDelivery()) {
            finalPriceElement.innerHTML = deliveryPrice + " ₽";
        } else {
            finalPriceElement.innerHTML =
                totalSum - discount + Number(deliveryPrice) + " ₽";
        }
        itemsCountField.innerHTML = "Всего товара: " + totalItems + " шт.";
    }

    if (document.querySelector('[data-page="cart"]') && cartDataParameters) {
        const sendOrderButton = document.querySelector(".showMoreButton");
        const orderForm = document.getElementById("contact-form");
        clearCartButton = document.querySelector("#cart-clear-button");
        clearCartButton?.addEventListener("click", clearCart);

        function clearCart() {
            localStorage.removeItem("cartItems");
            location.reload();
        }

        displayCartItems();
        updateSummaryBlock();

        const payType = document.querySelectorAll(".payType");
        payType.forEach((method) => {
            method.addEventListener("click", (e) => {
                payType.forEach((slot) => {
                    slot.classList.remove("active");
                });
                e.currentTarget.classList.add("active");
                const hiddenField = document.querySelector(
                    'input[name="payment_type"]'
                );
                hiddenField.value = method.dataset.payType;
                updateSummaryBlock();
            });
        });

        const phoneInput = document.querySelector('input[name="phone"]');
        const maskOptions = {
            mask: "+{7}(000)000-00-00",
            lazy: false,
        };
        let phoneMask = undefined;
        if (phoneInput) {
            phoneMask = new IMask(phoneInput, maskOptions);
        }

        const payTypeButtons = document.querySelectorAll(
            ".cartPaymentBlocksType .payType"
        );
        payTypeButtons.forEach((button) => {
            button.addEventListener("click", function () {
                payTypeButtons.forEach((btn) => btn.classList.remove("active"));
                this.classList.add("active");
                const selectedType = this.innerText.trim();
            });
        });

        sendOrderButton.addEventListener("click", function (e) {
            e.preventDefault();
            if (orderForm.checkValidity()) {
                if (phoneMask.masked.isComplete) {
                    sendOrderButton.disabled = true;
                    sendOrderButton.innerText =
                        "Подождите, идет формирование заказа...";
                    orderForm.submit();
                } else {
                    alert("ВВедите пожалуйста телефон!");
                }
            } else {
                orderForm.reportValidity();
            }
        });

        // const initialSelectedType = document
        //     .querySelector(".cartPaymentBlocksType .payType.active")
        //     ?.innerText.trim();
    }
});
