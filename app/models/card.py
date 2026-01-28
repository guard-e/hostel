"""
Модель данных Card для представления карты (пропуска).
"""

from datetime import datetime, date
from typing import Dict, Tuple, Optional
import logging

logger = logging.getLogger(__name__)


class Card:
    """Модель карты (пропуска)"""

    def __init__(self, people_id: int = None, card_id: int = None, room: int = None,
                 card_number: int = None, valid_from: date = None, valid_until: date = None,
                 status: int = 1, comments: str = None, profile_id: int = None):
        """
        Инициализация карты
        
        Args:
            people_id: ID человека
            card_id: ID карты
            room: Номер комнаты
            card_number: Номер карты
            valid_from: Дата начала действия
            valid_until: Дата окончания действия
            status: Статус карты (1=активна, 0=неактивна)
            comments: Комментарий
            profile_id: ID профиля
        """
        self.people_id = people_id
        self.card_id = card_id
        self.room = room
        self.card_number = card_number
        self.valid_from = valid_from
        self.valid_until = valid_until
        self.status = status
        self.comments = comments
        self.profile_id = profile_id

    def validate(self) -> Tuple[bool, Dict[str, str]]:
        """
        Валидировать данные карты
        
        Returns:
            Tuple[bool, Dict]: (is_valid, errors)
        """
        errors = {}

        # Проверка номера комнаты
        if self.room is None or self.room <= 0:
            errors['room'] = 'Номер комнаты должен быть больше 0'

        # Проверка номера карты
        if self.card_number is None or self.card_number <= 0:
            errors['card_number'] = 'Номер карты должен быть больше 0'

        # Проверка дат
        if self.valid_from is None:
            errors['valid_from'] = 'Дата начала действия обязательна'

        if self.valid_until is None:
            errors['valid_until'] = 'Дата окончания действия обязательна'

        if self.valid_from and self.valid_until:
            if self.valid_from >= self.valid_until:
                errors['valid_until'] = 'Дата окончания должна быть позже даты начала'

        # Проверка статуса
        if self.status not in [0, 1]:
            errors['status'] = 'Статус должен быть 0 или 1'

        return len(errors) == 0, errors

    def to_dict(self) -> Dict:
        """
        Преобразовать карту в словарь
        
        Returns:
            Dict с данными карты
        """
        return {
            'people_id': self.people_id,
            'card_id': self.card_id,
            'room': self.room,
            'card_number': self.card_number,
            'valid_from': self.valid_from.isoformat() if self.valid_from else None,
            'valid_until': self.valid_until.isoformat() if self.valid_until else None,
            'status': self.status,
            'comments': self.comments,
            'profile_id': self.profile_id
        }

    @staticmethod
    def from_dict(data: Dict) -> 'Card':
        """
        Создать карту из словаря
        
        Args:
            data: Словарь с данными карты
            
        Returns:
            Card: Объект карты
        """
        valid_from = data.get('valid_from')
        valid_until = data.get('valid_until')

        # Преобразовать строки в даты
        if isinstance(valid_from, str):
            valid_from = datetime.fromisoformat(valid_from).date()
        if isinstance(valid_until, str):
            valid_until = datetime.fromisoformat(valid_until).date()

        return Card(
            people_id=data.get('people_id'),
            card_id=data.get('card_id'),
            room=data.get('room'),
            card_number=data.get('card_number'),
            valid_from=valid_from,
            valid_until=valid_until,
            status=data.get('status', 1),
            comments=data.get('comments'),
            profile_id=data.get('profile_id')
        )

    @staticmethod
    def parse_room(room_number: int) -> Tuple[int, int]:
        """
        Разобрать номер комнаты в формате (X)XYY
        
        Args:
            room_number: Номер комнаты (например, 401 = этаж 4, комната 01)
            
        Returns:
            Tuple[int, int]: (floor, room_number)
        """
        if room_number is None or room_number <= 0:
            raise ValueError('Номер комнаты должен быть больше 0')

        floor = room_number // 100
        room = room_number % 100

        if floor <= 0 or room <= 0:
            raise ValueError('Некорректный формат номера комнаты')

        return floor, room

    def __repr__(self) -> str:
        """Строковое представление карты"""
        return (f"Card(card_id={self.card_id}, card_number={self.card_number}, "
                f"room={self.room}, status={self.status})")

    def __eq__(self, other) -> bool:
        """Сравнение карт"""
        if not isinstance(other, Card):
            return False
        return (self.card_id == other.card_id and
                self.card_number == other.card_number and
                self.room == other.room)
