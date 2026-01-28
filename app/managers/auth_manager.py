"""
AuthManager для управления аутентификацией и сессиями пользователей.
"""

import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)


class AuthManager:
    """Менеджер для управления аутентификацией пользователей"""

    @staticmethod
    def login_user(user_data: Dict) -> Dict:
        """
        Создать сессию пользователя при успешной аутентификации
        
        Args:
            user_data: Данные пользователя (id, username, permissions)
            
        Returns:
            Dict с информацией о сессии
        """
        try:
            session_data = {
                'user_id': user_data.get('id'),
                'username': user_data.get('username'),
                'permissions': user_data.get('permissions', {}),
                'authenticated': True
            }
            logger.info(f"Пользователь {user_data.get('username')} вошел в систему")
            return session_data
        except Exception as e:
            logger.error(f"Ошибка при создании сессии: {str(e)}")
            return {'error': str(e)}

    @staticmethod
    def logout_user(session: Dict) -> bool:
        """
        Завершить сессию пользователя
        
        Args:
            session: Данные сессии
            
        Returns:
            bool: True если успешно
        """
        try:
            username = session.get('username', 'Unknown')
            logger.info(f"Пользователь {username} вышел из системы")
            return True
        except Exception as e:
            logger.error(f"Ошибка при завершении сессии: {str(e)}")
            return False

    @staticmethod
    def is_authenticated(session: Dict) -> bool:
        """
        Проверить, аутентифицирован ли пользователь
        
        Args:
            session: Данные сессии
            
        Returns:
            bool: True если пользователь аутентифицирован
        """
        return session.get('authenticated', False) and 'user_id' in session

    @staticmethod
    def check_permissions(session: Dict, required_permission: str) -> bool:
        """
        Проверить наличие требуемого разрешения
        
        Args:
            session: Данные сессии
            required_permission: Требуемое разрешение (can_view, can_create, can_edit, can_delete, is_admin)
            
        Returns:
            bool: True если пользователь имеет требуемое разрешение
        """
        if not AuthManager.is_authenticated(session):
            return False

        permissions = session.get('permissions', {})
        
        # Администраторы имеют все разрешения
        if permissions.get('is_admin', False):
            return True

        return permissions.get(required_permission, False)

    @staticmethod
    def get_user_permissions(session: Dict) -> Dict[str, bool]:
        """
        Получить все разрешения пользователя
        
        Args:
            session: Данные сессии
            
        Returns:
            Dict с разрешениями
        """
        if not AuthManager.is_authenticated(session):
            return {
                'can_view': False,
                'can_create': False,
                'can_edit': False,
                'can_delete': False,
                'is_admin': False
            }

        return session.get('permissions', {})

    @staticmethod
    def require_permission(permission: str):
        """
        Декоратор для проверки разрешения на выполнение функции
        
        Args:
            permission: Требуемое разрешение
            
        Returns:
            Функция-декоратор
        """
        def decorator(func):
            def wrapper(*args, **kwargs):
                from flask import session, abort
                
                if not AuthManager.check_permissions(session, permission):
                    logger.warning(f"Доступ запрещен для пользователя {session.get('username')}")
                    abort(403)
                
                return func(*args, **kwargs)
            
            wrapper.__name__ = func.__name__
            return wrapper
        
        return decorator
