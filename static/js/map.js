ymaps.ready(function () {
    var myMap = new ymaps.Map('map', {
        center: [55.751574, 37.573856], // Москва (позже поменяем на адрес кафе)
        zoom: 15,
        controls: ['zoomControl', 'searchControl', 'typeSelector']
    });

    // Метка, которую можно перетаскивать
    var placemark = new ymaps.Placemark([55.751574, 37.573856], {
        hintContent: 'Перетащите метку на нужный адрес',
        balloonContent: 'Адрес доставки'
    }, {
        draggable: true
    });

    myMap.geoObjects.add(placemark);

    // При перетаскивании метки получаем адрес
    placemark.events.add('dragend', function (e) {
        var coords = placemark.geometry.getCoordinates();
        
        ymaps.geocode(coords).then(function (res) {
            var firstGeoObject = res.geoObjects.get(0);
            var address = firstGeoObject.getAddressLine();
            document.getElementById('address').value = address;
        });
    });

    // Поиск адреса при вводе
    document.getElementById('address').addEventListener('change', function (e) {
        var address = e.target.value;
        
        ymaps.geocode(address).then(function (res) {
            var firstGeoObject = res.geoObjects.get(0);
            if (firstGeoObject) {
                var coords = firstGeoObject.geometry.getCoordinates();
                placemark.geometry.setCoordinates(coords);
                myMap.setCenter(coords);
            }
        });
    });
});