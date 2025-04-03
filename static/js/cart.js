// Почему везде let а не const используется? Для поддержки совместимости? Тогда уж лучше var использовать

function removeCartDuplicate() {
    const cartItems = JSON.parse(localStorage.getItem("cartItems")) || [];
    const newCartItems = [];
    cartItems.forEach((item) => {
        const isDuplicate = newCartItems.some(
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
        return paymentType.value === "delivery" && cartDataParameters.dataset.deliveryPriceOffline;

    }

    function minusQuantity(index) {
        let cartItems = JSON.parse(localStorage.getItem("cartItems")) || [];
        if (cartItems[index].quantity > 1) cartItems[index].quantity--; // Сложно читается. Лучше декремент не использовать, а писать привычный синтаксис.
        if (cartItems[index].quantity > 1) {
            cartItems[index].quantity += 1
        }
        localStorage.setItem("cartItems", JSON.stringify(cartItems));
    }

    function plusQuantity(index) {
        let cartItems = JSON.parse(localStorage.getItem("cartItems")) || [];
        cartItems[index].quantity += 1; // Опять декремент
        localStorage.setItem("cartItems", JSON.stringify(cartItems));
    }

    function removeFromCart(index) {
        let cartItems = JSON.parse(localStorage.getItem("cartItems"));
        cartItems.splice(index, 1);
        localStorage.setItem("cartItems", JSON.stringify(cartItems));
    }

    function displayCartItems() {
        let cartItems = JSON.parse(localStorage.getItem("cartItems"));
        const productsAtCart = document.querySelector(".productsAtCart"); // А тут уже решили константы использовать, хотя до этого везде let был. Почему?

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

        // Лучше с guard-expression, чтобы избежать сильную вложенность. Так проще читать.
        if (cartItems.length < 0) {
            return
        }

        // Опять let. Цикл for ... in лучше не использовать, может свойства прототипов захватить. Хоть они здесь не используются, но не рекомендуется использовать данный цикл
        // В целом, можно даже деструктуризацию использовать: const [i, {image, name, color, и т.д.}] of cartItems.entries()
        for (const [i, item] of cartItems.entries()) {
            const cartItemsImage = item.image ? item.image : "/static/img/other/no_image.png"

            itemsHtml += `
            <div class="productCart">
            <button data-index="${i}" class="removeItem">
                <img src="/static/img/other/close.svg" alt="close">
            </button>
            <div class="leftSide">
            <img src="${cartItemsImage}" alt="product">
            </div>
            <div class="rightSide">

            <div>
            <div class="productCartName">
                ${item.name}
            </div>
            <div class="productCartParameter">
                ${item.parameter_string}
            </div>
            `;
            if (item.color) {
                itemsHtml += `
            <div class="productCartColorBlock">
                <div class="productCartColor">Цвет: </div>
                <div class="cart-product-parameter-color" style="background-color: ${item.color};"></div>
            </div>`;
            }
            itemsHtml += `
            <div class="productCartPrice">
                <span>${
                    item.price * item.quantity
                } ₽</span>`;
            if (item.oldPrice) {
                itemsHtml += `&nbsp;<span class="productCartOldPrice">${
                    item.oldPrice * item.quantity
                } ₽</span>`;
            }
            itemsHtml += `
            </div>
            </div>

            <div class="productCartCount">
                <button data-index="${i}" class="minusItem">-</button>
                <span class="countNumber">${item.quantity}</span>
                <button data-index="${i}" class="plusItem">+</button>
            </div>
            </div>
            </div>`;
        }

        productsAtCart.innerHTML = itemsHtml;

        // Можно уменьшить нагрузку на UI. Ранее на каждый item добавляется отдельный обработчик на .removeItem
        document.querySelector(".cartContainer").addEventListener("click", (event) => {
            if (event.target.closest(".removeItem")) {
                const index = event.target.closest(".removeItem").dataset.index;
                removeFromCart(index);
                displayCartItems();
                updateSummaryBlock();
            }
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

        // Лучше деструктуризировать и использовать "синтаксический сахар". Давно это слово не произносил)
        const dataToSend = cartItems.map(({product_id, parameter_id, quantity}) => ({
            product_id,
            parameter_id,
            quantity,
        }));
        document.getElementById("productsData").value =
            JSON.stringify(dataToSend);

    }

    function updateSummaryBlock() {
        // Вот тут понравилось. Хорошее разделение переменных, адекватно используются const и let
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

        // Зачем if? Если массив пустой - итераций и так не будет. Сюда же деструктуризацию можно добавить.
        cartItems.forEach(({quantity, price}) => {
            totalItems += quantity;
            totalSum += price * quantity;
        });

        if (cartDataParameters.dataset.actionsP23) {
            const [num1, num2] =
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
        clearCartButton = document.querySelector("#cart-clear-button"); // Тут вообще забыли декларацию переменной сделать
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

        // Опять непонятные комментарии. Почему оставили? Забыли убрать? Так и будет этот бедный участок кода на протяжении всей жизни проекта висеть.
        // const initialSelectedType = document
        //     .querySelector(".cartPaymentBlocksType .payType.active")
        //     ?.innerText.trim();
    }
});
