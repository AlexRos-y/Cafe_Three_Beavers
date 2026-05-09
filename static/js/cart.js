document.addEventListener('DOMContentLoaded', function() {
    // Обновление количества в корзине
    document.querySelectorAll('.update-qty').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            
            const itemId = this.dataset.id;
            const action = this.dataset.action;
            const input = document.querySelector(`.qty-input[data-id="${itemId}"]`);
            let quantity = parseInt(input.value);
            
            if (action === 'increase') {
                quantity++;
            } else if (action === 'decrease') {
                quantity--;
            }
            
            if (quantity <= 0) {
                // Если количество 0 — удаляем через форму
                const form = this.closest('.card-body').querySelector('form');
                if (form) form.submit();
                return;
            }
            
            // Отправляем AJAX-запрос
            fetch(`/cart/update/${itemId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ quantity: quantity })
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'ok') {
                    input.value = quantity;
                    document.getElementById('cart-total').textContent = data.total + ' ₽';
                    document.getElementById('cart-grand-total').textContent = data.total + ' ₽';
                }
            })
            .catch(error => console.error('Error:', error));
        });
    });
});