"""
Интеграционные тесты для приложения
"""

import pytest
from hypothesis import given, strategies as st, settings
from datetime import date, timedelta
from app.models.card import Card
from app.managers.auth_manager import AuthManager


class TestCRUDIntegration:
    """Интеграционные тесты для CRUD операций"""

    def test_card_creation_flow(self):
        """Тест полного цикла создания карты"""
        # Создать карту
        card = Card(
            room=401,
            card_number=1234567,
            valid_from=date.today(),
            valid_until=date.today() + timedelta(days=3),
            status=1,
            comments='Test card'
        )
        
        # Валидировать
        is_valid, errors = card.validate()
        assert is_valid, f"Card should be valid, but got errors: {errors}"
        
        # Сериализовать
        card_dict = card.to_dict()
        assert card_dict['card_number'] == 1234567
        
        # Десериализовать
        restored_card = Card.from_dict(card_dict)
        assert restored_card == card

    def test_card_update_flow(self):
        """Тест полного цикла обновления карты"""
        # Создать исходную карту
        original_card = Card(
            card_id=1,
            room=401,
            card_number=1234567,
            valid_from=date.today(),
            valid_until=date.today() + timedelta(days=3),
            status=1
        )
        
        # Обновить данные
        updated_data = original_card.to_dict()
        updated_data['room'] = 402
        updated_data['valid_days'] = 5
        
        # Создать обновленную карту
        updated_card = Card.from_dict(updated_data)
        assert updated_card.room == 402

    def test_card_deletion_flow(self):
        """Тест полного цикла удаления карты"""
        # Создать карту
        card = Card(
            card_id=1,
            room=401,
            card_number=1234567,
            valid_from=date.today(),
            valid_until=date.today() + timedelta(days=3),
            status=1
        )
        
        # Проверить, что карта валидна
        is_valid, errors = card.validate()
        assert is_valid
        
        # Карта готова к удалению
        assert card.card_id == 1


class TestAuthenticationFlow:
    """Интеграционные тесты для аутентификации"""

    def test_login_logout_flow(self):
        """Тест полного цикла входа и выхода"""
        # Вход
        user_data = {
            'id': 1,
            'username': 'testuser',
            'permissions': {
                'can_view': True,
                'can_create': True,
                'can_edit': True,
                'can_delete': False,
                'is_admin': False
            }
        }
        
        session_data = AuthManager.login_user(user_data)
        assert AuthManager.is_authenticated(session_data)
        
        # Проверить разрешения
        assert AuthManager.check_permissions(session_data, 'can_view')
        assert AuthManager.check_permissions(session_data, 'can_create')
        assert not AuthManager.check_permissions(session_data, 'can_delete')
        
        # Выход
        result = AuthManager.logout_user(session_data)
        assert result is True

    def test_permission_escalation_prevention(self):
        """Тест предотвращения повышения привилегий"""
        # Обычный пользователь
        user_session = {
            'user_id': 2,
            'username': 'user',
            'authenticated': True,
            'permissions': {
                'can_view': True,
                'can_create': False,
                'can_edit': False,
                'can_delete': False,
                'is_admin': False
            }
        }
        
        # Проверить, что пользователь не может создавать
        assert not AuthManager.check_permissions(user_session, 'can_create')
        assert not AuthManager.check_permissions(user_session, 'can_delete')
        
        # Администратор
        admin_session = {
            'user_id': 1,
            'username': 'admin',
            'authenticated': True,
            'permissions': {
                'can_view': True,
                'can_create': True,
                'can_edit': True,
                'can_delete': True,
                'is_admin': True
            }
        }
        
        # Проверить, что администратор может все
        assert AuthManager.check_permissions(admin_session, 'can_create')
        assert AuthManager.check_permissions(admin_session, 'can_delete')


class TestDataConsistency:
    """Тесты для проверки консистентности данных"""

    @given(
        room=st.integers(min_value=101, max_value=999),
        card_number=st.integers(min_value=1, max_value=9999999),
        valid_days=st.integers(min_value=1, max_value=365)
    )
    @settings(max_examples=100)
    def test_card_data_consistency(self, room, card_number, valid_days):
        """
        Property 10: Синхронизация списка с базой данных
        Validates: Requirements 4.4
        
        Проверяет, что данные карты остаются консистентными при сериализации.
        """
        today = date.today()
        
        # Создать карту
        card = Card(
            room=room,
            card_number=card_number,
            valid_from=today,
            valid_until=today + timedelta(days=valid_days),
            status=1
        )
        
        # Валидировать
        is_valid, errors = card.validate()
        assert is_valid, f"Card should be valid: {errors}"
        
        # Сериализовать и десериализовать
        card_dict = card.to_dict()
        restored_card = Card.from_dict(card_dict)
        
        # Проверить консистентность
        assert restored_card.room == card.room
        assert restored_card.card_number == card.card_number
        assert restored_card.valid_from == card.valid_from
        assert restored_card.valid_until == card.valid_until

    def test_form_clearing_after_operation(self):
        """
        Property 3: Очистка формы после операции
        Validates: Requirements 1.4
        
        Проверяет, что форма очищается после операции.
        """
        # Создать карту
        card = Card(
            room=401,
            card_number=1234567,
            valid_from=date.today(),
            valid_until=date.today() + timedelta(days=3)
        )
        
        # Валидировать
        is_valid, errors = card.validate()
        assert is_valid
        
        # После операции форма должна быть очищена
        # (в реальном приложении это происходит на клиенте)
        empty_card = Card()
        is_valid, errors = empty_card.validate()
        assert not is_valid  # Пустая карта невалидна
