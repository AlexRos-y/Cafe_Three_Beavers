ymaps.ready(function () {
    // Убедимся, что API загрузился
    if (typeof ymaps === 'undefined') {
        console.error('Яндекс.Карты не загрузились');
        document.getElementById('map').innerHTML = '<p style="padding: 20px; text-align: center;">❌ Ошибка загрузки карты. Проверьте ключ API.</p>';
        return;
    }

    // Стартовые координаты (Москва)
    var startCoords = [55.751574, 37.573856];

    var myMap = new ymaps.Map('map', {
        center: startCoords,
        zoom: 13,
        controls: ['zoomControl', 'searchControl', 'typeSelector']
    });

    // Создаём перетаскиваемую метку
    var placemark = new ymaps.Placemark(startCoords, {
        hintContent: '🏠 Адрес доставки',
        balloonContent: 'Перетащите метку на нужный адрес'
    }, {
        draggable: true,
        preset: 'islands#redHomeIcon'
    });
    myMap.geoObjects.add(placemark);

    // Функция: координаты → адрес
    function updateAddressFromCoords(coords) {
        var addressField = document.getElementById('address');
        addressField.value = 'Определяем адрес...';
        
        document.getElementById('latitude').value = coords[0];
        document.getElementById('longitude').value = coords[1];

        ymaps.geocode(coords, { results: 1 }).then(
            function (res) {
                var obj = res.geoObjects.get(0);
                if (obj) {
                    addressField.value = obj.getAddressLine();
                } else {
                    addressField.value = 'Адрес не найден';
                }
            },
            function (err) {
                console.error('Ошибка геокодирования:', err);
                addressField.value = 'Ошибка определения адреса';
            }
        );
    }

    // Функция: адрес → координаты (переместить метку)
    function updateMapFromAddress(address) {
        ymaps.geocode(address, { results: 1 }).then(
            function (res) {
                var obj = res.geoObjects.get(0);
                if (obj) {
                    var coords = obj.geometry.getCoordinates();
                    placemark.geometry.setCoordinates(coords);
                    myMap.setCenter(coords, 16);
                    document.getElementById('latitude').value = coords[0];
                    document.getElementById('longitude').value = coords[1];
                }
            },
            function (err) {
                console.error('Ошибка поиска адреса:', err);
            }
        );
    }

    // --- События ---

    // Клик по карте → ставим метку и получаем адрес
    myMap.events.add('click', function (e) {
        var coords = e.get('coords');
        placemark.geometry.setCoordinates(coords);
        updateAddressFromCoords(coords);
    });

    // Перетащили метку → получаем адрес
    placemark.events.add('dragend', function () {
        var coords = placemark.geometry.getCoordinates();
        updateAddressFromCoords(coords);
    });

    // Ввод адреса вручную (с задержкой)
    var timeout;
    var addressField = document.getElementById('address');
    
    addressField.addEventListener('input', function () {
        clearTimeout(timeout);
        var val = addressField.value.trim();
        if (val.length > 5 && val !== 'Определяем адрес...') {
            timeout = setTimeout(function () {
                updateMapFromAddress(val);
            }, 1000);
        }
    });

    addressField.addEventListener('blur', function () {
        clearTimeout(timeout);
        var val = addressField.value.trim();
        if (val.length > 5 && val !== 'Определяем адрес...') {
            updateMapFromAddress(val);
        }
    });

    // Инициализация: заполняем адрес для стартовой точки
    updateAddressFromCoords(startCoords);
});