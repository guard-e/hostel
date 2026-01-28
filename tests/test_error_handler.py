"""
Тесты для обработки ошибок
"""

import pytest
from hypothesis import given, strategies as st, settings
from app.utils.error_handler import ErrorHandler


class TestErrorHandler:
    """Тесты для обработчика ошибок"""

    def test_handle_database_connection_error(self):
        """Тест обработки ошибки подключения"""
        error = Exception("Connection refused")
        response, status = ErrorHandler.handle_database_error(error)
        
        assert status == 503
        assert 'error' in response
        assert 'подключения' in response['error'].lower()

    def test_handle_database_timeout_error(self):
        """Тест обработки ошибки таймаута"""
        error = Exception("Connection timeout")
        response, status = ErrorHandler.handle_database_error(error)
        
        assert status == 504
        assert 'error' in response

    def test_handle_database_permission_error(self):
        """Тест обработки ошибки прав доступа"""
        error = Exception("Permission denied")
        response, status = ErrorHandler.handle_database_error(error)
        
        assert status == 403
        assert 'error' in response

    def test_handle_procedure_result_added(self):
        """Тест обработки результата - карта добавлена"""
        response, status = ErrorHandler.handle_procedure_error(0)
        
        assert status == 201
        assert 'message' in response
        assert 'добавлена' in response['message'].lower()

    def test_handle_procedure_result_updated(self):
        """Тест обработки результата - карта обновлена"""
        response, status = ErrorHandler.handle_procedure_error(1)
        
        assert status == 200
        assert 'message' in response
        assert 'обновлена' in response['message'].lower()

    def test_handle_procedure_result_exists(self):
        """Тест обработки результата - карта существует"""
        response, status = ErrorHandler.handle_procedure_error(2)
        
        assert status == 409
        assert 'error' in response
        assert 'существует' in response['error'].lower()

    def test_handle_procedure_result_not_found(self):
        """Тест обработки результата - карта не найдена"""
        response, status = ErrorHandler.handle_procedure_error(3)
        
        assert status == 404
        assert 'error' in response
        assert 'не найдена' in response['error'].lower()

    def test_handle_validation_error(self):
        """Тест обработки ошибки валидации"""
        errors = {
            'room': 'Номер комнаты должен быть больше 0',
            'card_number': 'Номер карты должен быть больше 0'
        }
        
        response, status = ErrorHandler.handle_validation_error(errors)
        
        assert status == 400
        assert 'error' in response
        assert 'details' in response
        assert response['details'] == errors

    def test_handle_authentication_error(self):
        """Тест обработки ошибки аутентификации"""
        response, status = ErrorHandler.handle_authentication_error('Invalid credentials')
        
        assert status == 401
        assert 'error' in response

    def test_handle_authorization_error(self):
        """Тест обработки ошибки авторизации"""
        response, status = ErrorHandler.handle_authorization_error('Access denied')
        
        assert status == 403
        assert 'error' in response

    def test_handle_not_found_error(self):
        """Тест обработки ошибки 'не найдено'"""
        response, status = ErrorHandler.handle_not_found_error('Card')
        
        assert status == 404
        assert 'error' in response
        assert 'Card' in response['error']

    def test_handle_internal_error(self):
        """Тест обработки внутренней ошибки"""
        error = Exception("Something went wrong")
        response, status = ErrorHandler.handle_internal_error(error)
        
        assert status == 500
        assert 'error' in response

    @given(st.integers(min_value=0, max_value=10))
    @settings(max_examples=50)
    def test_handle_procedure_error_property(self, result_code):
        """
        Property 12: Обработка ошибок процедуры
        Validates: Requirements 5.3, 8.2, 8.4
        
        Проверяет, что все коды результата процедуры обрабатываются корректно.
        """
        response, status = ErrorHandler.handle_procedure_error(result_code)
        
        # Проверить, что всегда возвращается корректный статус
        assert status in [200, 201, 400, 404, 409, 500]
        assert isinstance(response, dict)
        assert 'error' in response or 'message' in response
