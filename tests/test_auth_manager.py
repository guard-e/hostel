"""
Тесты для AuthManager
"""

import pytest
from hypothesis import given, strategies as st, settings
from app.managers.auth_manager import AuthManager


class TestAuthManager:
    """Тесты для менеджера аутентификации"""

    def test_login_user(self):
        """Тест входа пользователя"""
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
        
        assert session_data['user_id'] == 1
        assert session_data['username'] == 'testuser'
        assert session_data['authenticated'] is True
        assert session_data['permissions']['can_view'] is True

    def test_logout_user(self):
        """Тест выхода пользователя"""
        session = {
            'user_id': 1,
            'username': 'testuser',
            'authenticated': True
        }
        
        result = AuthManager.logout_user(session)
        assert result is True

    def test_is_authenticated_true(self):
        """Тест проверки аутентификации - положительный случай"""
        session = {
            'user_id': 1,
            'username': 'testuser',
            'authenticated': True
        }
        
        assert AuthManager.is_authenticated(session) is True

    def test_is_authenticated_false(self):
        """Тест проверки аутентификации - отрицательный случай"""
        session = {}
        assert AuthManager.is_authenticated(session) is False
        
        session = {'authenticated': True}
        assert AuthManager.is_authenticated(session) is False

    def test_check_permissions_admin(self):
        """Тест проверки разрешений - администратор"""
        session = {
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
        
        # Администратор имеет все разрешения
        assert AuthManager.check_permissions(session, 'can_view') is True
        assert AuthManager.check_permissions(session, 'can_create') is True
        assert AuthManager.check_permissions(session, 'can_edit') is True
        assert AuthManager.check_permissions(session, 'can_delete') is True

    def test_check_permissions_user(self):
        """Тест проверки разрешений - обычный пользователь"""
        session = {
            'user_id': 2,
            'username': 'user',
            'authenticated': True,
            'permissions': {
                'can_view': True,
                'can_create': True,
                'can_edit': False,
                'can_delete': False,
                'is_admin': False
            }
        }
        
        assert AuthManager.check_permissions(session, 'can_view') is True
        assert AuthManager.check_permissions(session, 'can_create') is True
        assert AuthManager.check_permissions(session, 'can_edit') is False
        assert AuthManager.check_permissions(session, 'can_delete') is False

    def test_check_permissions_not_authenticated(self):
        """Тест проверки разрешений - не аутентифицирован"""
        session = {}
        
        assert AuthManager.check_permissions(session, 'can_view') is False
        assert AuthManager.check_permissions(session, 'can_create') is False

    def test_get_user_permissions_authenticated(self):
        """Тест получения разрешений - аутентифицирован"""
        session = {
            'user_id': 1,
            'username': 'testuser',
            'authenticated': True,
            'permissions': {
                'can_view': True,
                'can_create': True,
                'can_edit': False,
                'can_delete': False,
                'is_admin': False
            }
        }
        
        permissions = AuthManager.get_user_permissions(session)
        assert permissions['can_view'] is True
        assert permissions['can_create'] is True
        assert permissions['can_edit'] is False

    def test_get_user_permissions_not_authenticated(self):
        """Тест получения разрешений - не аутентифицирован"""
        session = {}
        
        permissions = AuthManager.get_user_permissions(session)
        assert permissions['can_view'] is False
        assert permissions['can_create'] is False
        assert permissions['can_edit'] is False
        assert permissions['can_delete'] is False
        assert permissions['is_admin'] is False

    @given(
        user_id=st.integers(min_value=1, max_value=1000),
        username=st.text(min_size=1, max_size=50)
    )
    @settings(max_examples=100)
    def test_login_user_property(self, user_id, username):
        """
        Property 19: Создание сессии при успешной аутентификации
        Validates: Requirements 9.6
        
        Проверяет, что при успешной аутентификации создается корректная сессия.
        """
        user_data = {
            'id': user_id,
            'username': username,
            'permissions': {
                'can_view': True,
                'can_create': True,
                'can_edit': True,
                'can_delete': False,
                'is_admin': False
            }
        }
        
        session_data = AuthManager.login_user(user_data)
        
        assert session_data['user_id'] == user_id
        assert session_data['username'] == username
        assert session_data['authenticated'] is True
        assert 'permissions' in session_data

    def test_login_user_property_failed(self):
        """
        Property 20: Отказ в доступе при неудачной аутентификации
        Validates: Requirements 9.7
        
        Проверяет, что при неудачной аутентификации доступ отклоняется.
        """
        session = {}
        
        # Пустая сессия означает неудачную аутентификацию
        assert AuthManager.is_authenticated(session) is False
        assert AuthManager.check_permissions(session, 'can_view') is False
