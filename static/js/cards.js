/**
 * Функции для управления картами
 */

let currentCardId = null;

/**
 * Загрузить список всех карт
 */
async function loadCards() {
    showLoading();
    try {
        const cards = await makeRequest('/cards', 'GET');
        displayCards(cards);
        hideLoading();
    } catch (error) {
        showMessage('Ошибка при загрузке карт: ' + error.message, 'danger');
        hideLoading();
    }
}

/**
 * Отобразить карты в таблице
 * @param {array} cards - Массив карт
 */
function displayCards(cards) {
    const tbody = document.getElementById('cardsBody');
    if (!tbody) return;

    tbody.innerHTML = '';

    if (!Array.isArray(cards) || cards.length === 0) {
        tbody.innerHTML = '<tr><td colspan="7" class="text-center text-muted">Карты не найдены</td></tr>';
        return;
    }

    cards.forEach(card => {
        const row = document.createElement('tr');
        const status = card.status === 1 ? 'Активна' : 'Неактивна';
        const statusBadge = card.status === 1 ? 'badge-active' : 'badge-inactive';

        row.innerHTML = `
            <td>${card.card_id || '-'}</td>
            <td>${card.card_number || '-'}</td>
            <td>${card.room || '-'}</td>
            <td>${card.valid_from || '-'}</td>
            <td>${card.valid_until || '-'}</td>
            <td><span class="badge ${statusBadge}">${status}</span></td>
            <td>
                <div class="action-buttons">
                    <button class="btn btn-sm btn-warning" onclick="showEditCardForm(${card.card_id})">
                        Редактировать
                    </button>
                    <button class="btn btn-sm btn-danger" onclick="showDeleteConfirm(${card.card_id})">
                        Удалить
                    </button>
                </div>
            </td>
        `;
        tbody.appendChild(row);
    });
}

/**
 * Показать форму добавления карты
 */
function showAddCardForm() {
    clearValidationErrors();
    document.getElementById('cardForm').reset();
    document.getElementById('cardModalTitle').textContent = 'Добавить карту';
    currentCardId = null;

    // Установить дату на сегодня
    const today = new Date().toISOString().split('T')[0];
    document.getElementById('valid_from').value = today;

    const modal = new bootstrap.Modal(document.getElementById('cardModal'));
    modal.show();
}

/**
 * Показать форму редактирования карты
 * @param {number} cardId - ID карты
 */
async function showEditCardForm(cardId) {
    showLoading();
    try {
        const card = await makeRequest(`/cards/${cardId}`, 'GET');
        
        document.getElementById('room').value = card.room || '';
        document.getElementById('card_number').value = card.card_number || '';
        document.getElementById('valid_from').value = card.valid_from || '';
        document.getElementById('valid_days').value = card.valid_days || '';
        document.getElementById('comments').value = card.comments || '';
        document.getElementById('dep').value = card.dep || 'ХОСТЕЛ';

        document.getElementById('cardModalTitle').textContent = 'Редактировать карту';
        currentCardId = cardId;

        clearValidationErrors();
        const modal = new bootstrap.Modal(document.getElementById('cardModal'));
        modal.show();
        hideLoading();
    } catch (error) {
        showMessage('Ошибка при загрузке данных карты: ' + error.message, 'danger');
        hideLoading();
    }
}

/**
 * Сохранить карту
 */
async function saveCard() {
    const validation = validateCardForm();
    if (!validation.isValid) {
        showValidationErrors(validation.errors);
        return;
    }

    clearValidationErrors();
    showLoading();

    const data = {
        room: parseInt(document.getElementById('room').value),
        card_number: parseInt(document.getElementById('card_number').value),
        valid_from: document.getElementById('valid_from').value,
        valid_days: parseInt(document.getElementById('valid_days').value),
        comments: document.getElementById('comments').value,
        dep: document.getElementById('dep').value
    };

    try {
        let result;
        if (currentCardId) {
            result = await makeRequest(`/cards/${currentCardId}`, 'PUT', data);
        } else {
            result = await makeRequest('/cards', 'POST', data);
        }

        if (result.error) {
            showMessage('Ошибка: ' + result.error, 'danger');
        } else {
            showMessage(
                currentCardId ? 'Карта успешно обновлена' : 'Карта успешно добавлена',
                'success'
            );
            
            // Закрыть модальное окно
            bootstrap.Modal.getInstance(document.getElementById('cardModal')).hide();
            
            // Перезагрузить список карт
            loadCards();
        }
        hideLoading();
    } catch (error) {
        showMessage('Ошибка при сохранении карты: ' + error.message, 'danger');
        hideLoading();
    }
}

/**
 * Показать диалог подтверждения удаления
 * @param {number} cardId - ID карты
 */
function showDeleteConfirm(cardId) {
    currentCardId = cardId;
    const modal = new bootstrap.Modal(document.getElementById('deleteModal'));
    modal.show();
}

/**
 * Подтвердить удаление карты
 */
async function confirmDelete() {
    if (!currentCardId) return;

    showLoading();
    try {
        const result = await makeRequest(`/cards/${currentCardId}`, 'DELETE');

        if (result.error) {
            showMessage('Ошибка: ' + result.error, 'danger');
        } else {
            showMessage('Карта успешно удалена', 'success');
            
            // Закрыть модальное окно
            bootstrap.Modal.getInstance(document.getElementById('deleteModal')).hide();
            
            // Перезагрузить список карт
            loadCards();
        }
        hideLoading();
    } catch (error) {
        showMessage('Ошибка при удалении карты: ' + error.message, 'danger');
        hideLoading();
    }
}
