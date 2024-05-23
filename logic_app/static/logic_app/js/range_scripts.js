document.addEventListener('DOMContentLoaded', (event) => {
    const rangeInput = document.getElementById('customRange3');
    const rangeValue = document.getElementById('rangeValue');
    const sendButton = document.getElementById('sendButton');
    const numberWords = {
        1: 'один человек',
        2: 'двое человек',
        3: 'трое человек',
        4: 'четверо человек',
        5: 'пятеро человек',
        6: 'шестеро человек',
        7: 'семеро человек',
        8: 'восемеро человек',
        9: 'девятеро человек',
        10: 'десятеро человек',
        11: 'более десяти человек'
    };

    // Инициализация отображаемого значения
    rangeValue.textContent = numberWords[rangeInput.value];

    // Обновление значения отображаемого элемента при изменении ползунка
    rangeInput.addEventListener('input', () => {
        rangeValue.textContent = numberWords[rangeInput.value];
    });

    // Отправка данных на сервер при нажатии на кнопку
    sendButton.addEventListener('click', () => {
        const value = rangeInput.value;

        // Создание POST-запроса для отправки данных на сервер
        fetch('/submit-range-value/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken') // Убедитесь, что передается CSRF-токен
            },
            body: JSON.stringify({ 'range_value': value })
        })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    });

    // Функция для получения CSRF-токена из cookie
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Проверяем, соответствует ли эта cookie необходимому имени
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
