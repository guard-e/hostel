/**
 * Основные функции JavaScript для приложения управления картами
 */

/**
 * Показать сообщение пользователю
 * @param {string} message - Текст сообщения
 * @param {string} type - Тип сообщения (success, error, warning, info)
 */
function showMessage(message, type = 'info') {
    const messageDiv = document.getElementById('message');
    if (!messageDiv) return;

    messageDiv.className = `alert alert-${type} alert-dismissible fade show`;
    messageDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    messageDiv.style.display = 'block';

    // Автоматически скрыть через 5 секунд
    setTimeout(() => {
        messageDiv.style.display = 'none';
    }, 5000);
}

/**
 * Показать индикатор загрузки
 */
function showLoading() {
    const loading = document.getElementById('loading');
    if (loading) {
        loading.style.display = 'block';
    }
}

/**
 * Скрыть индикатор загрузки
 */
function hideLoading() {
    const loading = document.getElementById('loading');
    if (loading) {
        loading.style.display = 'none';
    }
}

/**
 * Выполнить AJAX запрос
 * @param {string} url - URL для запроса
 * @param {string} method - HTTP метод (GET, POST, PUT, DELETE)
 * @param {object} data - Данные для отправки
 * @returns {Promise}
 */
async function makeRequest(url, method = 'GET', data = null) {
    const options = {
        method: method,
        headers: {
            'Content-Type': 'application/json',
        }
    };

    if (data) {
        options.body = JSON.stringify(data);
    }

    try {
        const response = await fetch(url, options);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error('Request error:', error);
        throw error;
    }
}

/**
 * Валидировать форму карты
 * @returns {object} - Объект с результатом валидации и ошибками
 */
function validateCardForm() {
    const errors = {};
    const room = document.getElementById('room').value;
    const cardNumber = document.getElementById('card_number').value;
    const validFrom = document.getElementById('valid_from').value;
    const validDays = document.getElementById('valid_days').value;

    if (!room || room <= 0) {
        errors.room = 'Номер комнаты должен быть больше 0';
    }

    if (!cardNumber || cardNumber <= 0) {
        errors.card_number = 'Номер карты должен быть больше 0';
    }

    if (!validFrom) {
        errors.valid_from = 'Дата начала действия обязательна';
    }

    if (!validDays || validDays <= 0) {
        errors.valid_days = 'Количество дней должно быть больше 0';
    }

    return {
        isValid: Object.keys(errors).length === 0,
        errors: errors
    };
}

/**
 * Показать ошибки валидации
 * @param {object} errors - Объект с ошибками
 */
function showValidationErrors(errors) {
    // Очистить предыдущие ошибки
    document.querySelectorAll('.invalid-feedback').forEach(el => {
        el.style.display = 'none';
    });

    // Показать новые ошибки
    for (const [field, message] of Object.entries(errors)) {
        const input = document.getElementById(field);
        if (input) {
            input.classList.add('is-invalid');
            const feedback = input.nextElementSibling;
            if (feedback && feedback.classList.contains('invalid-feedback')) {
                feedback.textContent = message;
                feedback.style.display = 'block';
            }
        }
    }
}

/**
 * Очистить ошибки валидации
 */
function clearValidationErrors() {
    document.querySelectorAll('.form-control').forEach(input => {
        input.classList.remove('is-invalid');
    });
    document.querySelectorAll('.invalid-feedback').forEach(el => {
        el.style.display = 'none';
    });
}
