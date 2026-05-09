// Обновление счётчика корзины в навбаре
function updateCartCount(count) {
    var badge = document.getElementById('cart-count');
    if (badge) {
        badge.textContent = count;
        if (count > 0) {
            badge.classList.remove('d-none');
        } else {
            badge.classList.add('d-none');
        }
    }
}

// Функция для AJAX-добавления в корзину
function addToCart(itemId, button) {
    fetch('/cart/add/' + itemId, {
        method: 'POST',
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/json'
        }
    })
    .then(function(response) { return response.json(); })
    .then(function(data) {
        if (data.status === 'ok') {
            updateCartCount(data.cart_count);
            
            // Визуальный фидбек на кнопке
            var originalHTML = button.innerHTML;
            button.innerHTML = '<i class="bi bi-check"></i> Добавлено!';
            button.classList.add('btn-success');
            button.classList.remove('btn-outline-primary');
            
            setTimeout(function() {
                button.innerHTML = originalHTML;
                button.classList.remove('btn-success');
                button.classList.add('btn-outline-primary');
            }, 1500);
        }
    })
    .catch(function(error) {
        console.error('Ошибка:', error);
    });
}

document.addEventListener('DOMContentLoaded', function() {
    // Обработчики для кнопок "В корзину" в меню (AJAX)
    document.querySelectorAll('.add-to-cart-ajax').forEach(function(button) {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            var itemId = this.dataset.id;
            addToCart(itemId, this);
        });
    });

    // Обновление количества в корзине (на странице cart.html)
    document.querySelectorAll('.update-qty').forEach(function(button) {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            
            var itemId = this.dataset.id;
            var action = this.dataset.action;
            var input = document.querySelector('.qty-input[data-id="' + itemId + '"]');
            var quantity = parseInt(input.value);
            
            if (action === 'increase') {
                quantity++;
            } else if (action === 'decrease') {
                quantity--;
            }
            
            if (quantity <= 0) {
                var form = this.closest('form');
                if (form) {
                    var formData = new FormData(form);
                    fetch(form.action, {
                        method: 'POST',
                        body: formData
                    }).then(function() {
                        window.location.reload();
                    });
                }
                return;
            }
            
            fetch('/cart/update/' + itemId, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ quantity: quantity })
            })
            .then(function(response) { return response.json(); })
            .then(function(data) {
                if (data.status === 'ok') {
                    input.value = quantity;
                    document.getElementById('cart-total').textContent = data.total + ' ₽';
                    document.getElementById('cart-grand-total').textContent = data.total + ' ₽';
                    updateCartCount(data.cart_count);
                }
            })
            .catch(function(error) {
                console.error('Ошибка:', error);
            });
        });
    });
});