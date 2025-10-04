import uuid
from datetime import datetime
from datetime import date
import time
import pickle
from functools import wraps


class InvalidDateError(Exception):
    """Исключение для невалидных форматов даты"""

    def __init__(self, message="Неверный формат даты"):
        """
        Args:
            message (str): Сообщение об ошибке
        """
        self.message = message
        super().__init__(self.message)


class InvalidHeightError(Exception):
    """Исключение для недопустимых значений высоты скульптуры"""

    def __init__(self, height, message="Неверная высота скульптуры"):
        """
        Args:
            height: Некорректное значение высоты
            message: Сообщение об ошибке
        """
        self.height = height
        self.message = f"{message}: {height}"
        super().__init__(self.message)


def timing_decorator(func):
    """Декоратор для замера времени выполнения метода."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Время выполнения метода {func.__name__}: {end_time - start_time:.4f} секунд")
        return result
    return wrapper

def count_calls_decorator(func):
    """Декоратор для подсчета количества вызовов метода."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not hasattr(wrapper, 'call_count'):
            wrapper.call_count = 0
        wrapper.call_count += 1
        print(f"Вызов метода {func.__name__}: {wrapper.call_count}")
        return func(*args, **kwargs)
    return wrapper


class Author:
    """Класс для представления автора музейного предмета"""

    def __init__(self, full_name="", birth_date="", country=""):
        """
        Args:
            full_name (str): Полное имя автора
            birth_date (str): Дата рождения в формате ДД.ММ.ГГГГ
            country (str): Страна происхождения
        """
        self.id = uuid.uuid4()
        self.__full_name = full_name
        self.__birth_date = birth_date
        self.__country = country

    def __del__(self):
        """Деструктор - выводит информацию об авторе при удалении"""
        print(f'ФИО {self.__full_name} : Дата рождения {self.__birth_date} : Страна {self.__country}  \n')

    @property
    def full_name(self):
        """str: Полное имя автора"""
        return self.__full_name

    @full_name.setter
    def full_name(self, value):
        """Устанавливает полное имя автора"""
        self.__full_name = value

    @property
    def birth_date(self):
        """date: Дата рождения автора"""
        return self.__birth_date

    @birth_date.setter
    def birth_date(self, value):
        """
        Устанавливает дату рождения с валидацией формата

        Raises:
            InvalidDateError: Если формат даты не соответствует ДД.ММ.ГГГГ
        """
        self.__birth_date = value
        try:
            self.__birth_date = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise InvalidDateError(f"Неверный формат даты: {value}.")

    @property
    def country(self):
        """str: Страна происхождения """
        return self.__country

    @country.setter
    def country(self, value):
        """Устанавливает страну происхождения"""
        self.__country = value

    @timing_decorator
    @count_calls_decorator
    def __str__(self):
        """Возвращает строковое представление автора"""
        return f'ФИО: {self.__full_name}, Дата рождения: {self.__birth_date}, Страна: {self.__country}'


class PersistenceAuthor:
    """Класс для сериализации и десериализации объектов Author"""

    @staticmethod
    def serialize(author):
        """
        Сериализует объект Author в файл

        Args:
            author (Author): Объект для сериализации
        """
        with open('author.pkl', 'wb') as f:
            pickle.dump(author, pickle.load(f))

    @staticmethod
    def deserialize():
        """
        Десериализует объект Author из файла

        Returns:
            Author: Десериализованный объект
        """
        with open('author.pkl', 'rb') as f:
            author = pickle.load(f)
        return author


class Fund:
    """Класс для представления музейного фонда"""

    def __init__(self, name="", curator=""):
        """
        Args:
            name (str): Название фонда
            curator (str): ФИО хранителя фонда
        """
        self.id = uuid.uuid4()
        self.__name = name
        self.__curator = curator
        self.__items: list[MuseumItem | Collection] = []

    def __del__(self):
        """Деструктор - выводит информацию о фонде при удалении"""
        print(f'Название {self.__name} : Хранитель {self.__curator} \n')

    @property
    def name(self):
        """str: Название фонда """
        return self.__name

    @name.setter
    def name(self, value):
        """Устанавливает название фонда"""
        self.__name = value

    @property
    def curator(self):
        """str: ФИО хранителя фонда """
        return self.__curator

    @curator.setter
    def curator(self, value):
        """Устанавливает ФИО хранителя фонда"""
        self.__curator = value

    @property
    def items(self):
        """list: Список предметов/коллекций в фонде"""
        return self.__items

    @items.setter
    def items(self, value):
        """Устанавливает список предметов/коллекций"""
        self.__items = value

    @timing_decorator
    @count_calls_decorator
    def __str__(self):
        """Возвращает строковое представление фонда"""
        return f'Название: {self.__name}, Хранитель: {self.__curator}'

    def add_item(self, item):
        """
        Добавляет предмет/коллекцию в фонд

        Args:
            item: Объект MuseumItem или Collection для добавления
        """
        self.__items.append(item)


class MuseumItem:
    """Базовый класс для музейных предметов"""

    def __init__(self, number=0, name="", date_of_creation=None, is_exactly=False, author=None, fund=None):
        """
        Args:
            number: Инвентарный номер
            name: Название предмета
            date_of_creation: Дата создания
            is_exactly: Точность датировки
            author: Автор (объект Author)
            fund: Фонд хранения (объект Fund)
        """
        self.id = uuid.uuid4()
        self.__number = number
        self.__name = name
        self.__date_of_creation = date_of_creation
        self.__is_exactly = is_exactly
        self.__author = author or Author()
        self.__fund = fund
        self.__collection = None
        self.__exhibitions = []

    @property
    def number(self):
        """int: Инвентарный номер"""
        return self.__number

    @number.setter
    def number(self, value):
        """Устанавливает инвентарный номер"""
        self.__number = value

    @property
    def name(self):
        """str: Название предмета"""
        return self.__name

    @name.setter
    def name(self, value):
        """Устанавливает название предмета"""
        self.__name = value

    @property
    def date_of_creation(self):
        """date: Дата создания """
        return self.__date_of_creation

    @date_of_creation.setter
    def date_of_creation(self, value):
        """
        Устанавливает дату создания с валидацией

        Raises:
            InvalidDateError: Если формат даты неверный или дата в будущем
        """
        try:
            self.__date_of_creation = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise InvalidDateError(f"Неверный формат даты: {value}.")
        if self.date_of_creation > date.today():
            raise InvalidDateError("Дата создания не может быть в будущем")

    @property
    def is_exactly(self):
        """bool: Точность датировки"""
        return self.__is_exactly

    @is_exactly.setter
    def is_exactly(self, value):
        """Устанавливает точность датировки"""
        self.__is_exactly = value

    @property
    def author(self):
        """Author: Автор предмета """
        return self.__author

    @author.setter
    def author(self, value):
        """Устанавливает автора предмета"""
        self.__author = value

    @property
    def fund(self):
        """Fund: Фонд хранения """
        return self.__fund

    @fund.setter
    def fund(self, value):
        """Устанавливает фонд хранения"""
        self.__fund = value

    @property
    def collection(self):
        """Collection: Коллекция """
        return self.__collection

    @collection.setter
    def collection(self, value):
        """Устанавливает коллекцию"""
        self.__collection = value

    @property
    def exhibitions(self):
        """list: Список выставок """
        return self.__exhibitions

    @exhibitions.setter
    def exhibitions(self, value):
        """Устанавливает список выставок"""
        self.__exhibitions = value

    @timing_decorator
    @count_calls_decorator
    def __str__(self):
        """Возвращает строковое представление предмета"""
        return (f'Номер: {self.number}, '
                f'Название: {self.name}, '
                f'Дата создания: {self.date_of_creation}, '
                f'Точная ли дата: {self.is_exactly}, '
                f'Автор: {self.author()}, '
                f'Фонд: {self.fund()}')


class Painting(MuseumItem):
    """Класс для картин (наследуется от MuseumItem)"""

    def __init__(self, number=0, name="", date_of_creation="", is_exactly=False,
                 author=None, fund=None, material="", style=""):
        """
        Args:
            material: Материал (масло, акварель и т.д.)
            style: Стиль (реализм, импрессионизм и т.д.)
        """
        super().__init__(number, name, date_of_creation, is_exactly, author, fund)
        self.__material = material
        self.__style = style

    @property
    def material(self):
        """str: Материал"""
        return self.__material

    @material.setter
    def material(self, value):
        """Устанавливает материал"""
        self.__material = value

    @property
    def style(self):
        """str: Стиль"""
        return self.__style

    @style.setter
    def style(self, value):
        """Устанавливает стиль"""
        self.__style = value

    @timing_decorator
    @count_calls_decorator
    def __str__(self):
        """Возвращает строковое представление картины"""
        return (f'Номер: {self.number},'
                f' Название: {self.name},'
                f' Дата создания: {self.date_of_creation},'
                f' Точная ли дата: {self.is_exactly},'
                f' Автор: {self.author},'
                f' Фонд: {self.fund},'
                f' Материал: {self.material},'
                f' Стиль: {self.style}')


class Sculpture(MuseumItem):
    """Класс для скульптур (наследуется от MuseumItem)"""

    def __init__(self, number=0, name="", date_of_creation="", is_exactly=False,
                 author=None, fund=None, material="", height=0.0):
        """
        Args:
            material: Материал (мрамор, бронза и т.д.)
            height: Высота в метрах
        """
        super().__init__(number, name, date_of_creation, is_exactly, author, fund)
        self.__material = material
        self.__height = height

    @property
    def material(self):
        """str: Материал """
        return self.__material

    @material.setter
    def material(self, value):
        """Устанавливает материал"""
        self.__material = value

    @property
    def height(self):
        """float: Высота в метрах"""
        return self.__height

    @height.setter
    def height(self, value):
        """
        Устанавливает высоту скульптуры

        Raises:
            InvalidHeightError: Если высота отрицательная
        """
        if value < 0:
            raise InvalidHeightError(value)
        self.__height = value

    @timing_decorator
    @count_calls_decorator
    def __str__(self):
        """Возвращает строковое представление скульптуры"""
        return (f'Номер: {self.number}, '
                f'Название: {self.name}, '
                f'Дата создания: {self.date_of_creation}, '
                f'Точная ли дата: {self.is_exactly},'
                f' Автор: {self.author}, '
                f'Фонд: {self.fund}, '
                f'Материал: {self.material}, '
                f'Высота: {self.height}')


class Collection:
    """Класс для представления коллекции музейных предметов"""

    def __init__(self, name="", annotation=""):
        """
        Args:
            name: Название коллекции
            annotation: Аннотация/описание
        """
        self.id = uuid.uuid4()
        self.__name = name
        self.__annotation = annotation
        self.__items: list[MuseumItem] = []

    def __del__(self):
        """Деструктор - выводит информацию о коллекции при удалении"""
        print(f'Название {self.__name} : Аннотация {self.__annotation} \n')

    @property
    def name(self):
        """str: Название коллекции"""
        return self.__name

    @name.setter
    def name(self, value):
        """Устанавливает название коллекции"""
        self.__name = value

    @property
    def annotation(self):
        """str: Аннотация """
        return self.__annotation

    @annotation.setter
    def annotation(self, value):
        """Устанавливает аннотацию"""
        self.__annotation = value

    @property
    def items(self):
        """list: Список предметов в коллекции"""
        return self.__items

    @items.setter
    def items(self, value):
        """Устанавливает список предметов"""
        self.__items = value

    def add_item(self, item: MuseumItem):
        """
        Добавляет предмет в коллекцию

        Args:
            item: Объект MuseumItem для добавления
        """
        self.__items.append(item)
        item.collection = self

    def __add__(self, other):
        self.__items.append(other)
        return self

    @timing_decorator
    @count_calls_decorator
    def __str__(self):
        """Возвращает строковое представление коллекции"""
        return f'Название: {self.__name} Аннотация: {self.__annotation} Предметы: {[item.__str__() for item in self.__items]}'


class Organization:
    """Класс для представления организации"""

    def __init__(self, name="", address="", telephone_number="", contact_name=""):
        """
        Args:
            name: Название организации
            address: Адрес
            telephone_number: Номер телефона
            contact_name: ФИО контактного лица
        """
        self.id = uuid.uuid4()
        self.__name = name
        self.__address = address
        self.__telephone_number = telephone_number
        self.__contact_name = contact_name

    @property
    def name(self):
        """str: Название организации"""
        return self.__name

    @name.setter
    def name(self, value):
        """Устанавливает название организации"""
        self.__name = value

    @property
    def address(self):
        """str: Адрес """
        return self.__address

    @address.setter
    def address(self, value):
        """Устанавливает адрес"""
        self.__address = value

    @property
    def telephone_number(self):
        """str: Номер телефона"""
        return self.__telephone_number

    @telephone_number.setter
    def telephone_number(self, value):
        """Устанавливает номер телефона"""
        self.__telephone_number = value

    @property
    def contact_name(self):
        """str: ФИО контактного лица"""
        return self.__contact_name

    @contact_name.setter
    def contact_name(self, value):
        """Устанавливает ФИО контактного лица"""
        self.__contact_name = value

    @timing_decorator
    @count_calls_decorator
    def __str__(self):
        """Возвращает строковое представление организации"""
        return (f'Название[{self.id}]: {self.__name}, '
                f'Адрес: {self.__address}, '
                f'Номер телефона: {self.__telephone_number}, '
                f'ФИО контактного лица: {self.__contact_name}')


class Exhibition:
    """Класс для представления выставки"""

    def __init__(self, organisation=None, place="", name="", beginning_date="", ending_date=""):
        """
        Args:
            organisation: Организатор (объект Organization)
            place: Место проведения
            name: Название выставки
            beginning_date: Дата начала (ДД.ММ.ГГГГ)
            ending_date: Дата окончания (ДД.ММ.ГГГГ)
        """
        self.id = uuid.uuid4()
        self.__organisation = organisation
        self.__place = place
        self.__name = name
        self.__beginning_date = beginning_date
        self.__ending_date = ending_date
        self.__items = []

    @property
    def organisation(self):
        """Organization: Организатор"""
        return self.__organisation

    @organisation.setter
    def organisation(self, value):
        """Устанавливает организатора"""
        self.__organisation = value

    @property
    def place(self):
        """str: Место проведения"""
        return self.__place

    @place.setter
    def place(self, value):
        """Устанавливает место проведения"""
        self.__place = value

    @property
    def name(self):
        """str: Название выставки"""
        return self.__name

    @name.setter
    def name(self, value):
        """Устанавливает название выставки"""
        self.__name = value

    @property
    def beginning_date(self):
        """date: Дата начала"""
        return self.__beginning_date

    @beginning_date.setter
    def beginning_date(self, value):
        """
        Устанавливает дату начала с валидацией

        Raises:
            InvalidDateError: Если формат даты неверный
        """
        try:
            self.__beginning_date = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise InvalidDateError(f"Неверный формат даты: {value}.")

    @property
    def ending_date(self):
        """date: Дата окончания"""
        return self.__ending_date

    @ending_date.setter
    def ending_date(self, value):
        """
        Устанавливает дату окончания с валидацией

        Raises:
            InvalidDateError: Если формат даты неверный
        """
        try:
            self.__ending_date = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise InvalidDateError(f"Неверный формат даты: {value}.")

    @property
    def items(self):
        """list: Список предметов/коллекций"""
        return self.__items

    @items.setter
    def items(self, value):
        """Устанавливает список предметов/коллекций"""
        self.__items = value

    def add_item(self, item):
        """
        Добавляет предмет/коллекцию на выставку

        Args:
            item: Объект MuseumItem или Collection
        """
        self.__items.append(item)
        item.exhibitions = [self]

    def __add__(self, other):
        self.__items.append(other)
        return self.__items

    @timing_decorator
    @count_calls_decorator
    def __str__(self):
        """Возвращает строковое представление выставки"""
        return (f'Организация: {self.__organisation.get_name()}, '
                f'Местонахождение: {self.__place}, '
                f'Название[{self.id}]: {self.__name}, '
                f'Дата начала: {self.__beginning_date}, '
                f'Дата окончания: {self.__ending_date}')


class MovementAct:
    """Класс для учета перемещений музейных предметов"""

    def __init__(self, movement_type, movement_date, item: MuseumItem):
        """
        Args:
            movement_type: Тип перемещения
            movement_date: Дата перемещения (ДД.ММ.ГГГГ)
            item: Перемещаемый предмет
        """
        self.__movement_type = movement_type
        self.__movement_date = movement_date
        self.__item = item
        self.__from_fund = item.fund
        self.__to_fund = None
        self.__organization = None
        self.__exhibition = None

    @property
    def movement_type(self):
        """str: Тип перемещения"""
        return self.__movement_type

    @movement_type.setter
    def movement_type(self, value):
        """Устанавливает тип перемещения"""
        self.__movement_type = value

    @property
    def movement_date(self):
        """date: Дата перемещения"""
        return self.__movement_date

    @movement_date.setter
    def movement_date(self, value):
        """
        Устанавливает дату перемещения с валидацией

        Raises:
            InvalidDateError: Если формат даты неверный
        """
        try:
            self.__movement_date = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise InvalidDateError(f"Неверный формат даты: {value}.")
        self.__movement_date = value

    @property
    def item(self):
        """MuseumItem: Перемещаемый предмет"""
        return self.__item

    @item.setter
    def item(self, value):
        """Устанавливает перемещаемый предмет"""
        self.__item = value

    @property
    def from_fund(self):
        """Fund: Исходный фонд"""
        return self.__from_fund

    @from_fund.setter
    def from_fund(self, value):
        """Устанавливает исходный фонд"""
        self.__from_fund = value

    @property
    def to_fund(self):
        """Fund: Целевой фонд """
        return self.__to_fund

    @to_fund.setter
    def to_fund(self, value):
        """Устанавливает целевой фонд и обновляет предмет"""
        self.item.fund = value
        self.__to_fund = value

    @property
    def organization(self):
        """Organization: Организация"""
        return self.__organization

    @organization.setter
    def organization(self, value):
        """Устанавливает организацию"""
        self.__organization = value

    @property
    def exhibition(self):
        """Exhibition: Выставка"""
        return self.__exhibition

    @exhibition.setter
    def exhibition(self, value):
        """Устанавливает выставку"""
        self.__exhibition = value

    def internal_movement(self):
        """Осуществляет внутреннее перемещение между фондами"""
        self.__from_fund.items.remove(self.__item)
        self.__to_fund.add_item(self.__item)

    def exhibition_transfer(self):
        """Оформляет передачу предмета на выставку"""
        self.__exhibition.add_item(self.__item)

    def exhibition_return(self):
        """Оформляет возврат предмета с выставки"""
        self.__exhibition.items.remove(self.__item)

    def write_off(self):
        """Оформляет списание предмета"""
        self.__item.fund.items.remove(self.__item)
        self.__item.fund = None

    @timing_decorator
    @count_calls_decorator
    def get_movement_info(self) -> str:
        """
        Возвращает информацию о перемещении

        Returns:
            str: Форматированная строка с информацией
        """
        info = [
            f'Тип перемещения: {self.__movement_type}'
            f'Дата: {self.__movement_date.strftime('%d.%m.%Y')}'
            f"Предмет: {self.__item.name} (Номер {self.__item.number})",
            f"Из фонда: {self.__from_fund.name}",
        ]
        if self.__to_fund:
            info.append(f"В фонд: {self.__to_fund.name}")
        if self.__exhibition:
            info.append(f"На выставку: {self.__exhibition.name}")

        return "\n".join(info)

class Museum:
    def __init__(self, name):
        self.name = name
        self.authors = []
        self.funds = []
        self.items = []
        self.collections = []
        self.exhibitions = []
        self.organizations = []
        self.movement_acts = []

    def add_author(self, author):
        """Добавляет автора в музей"""
        self.authors.append(author)

    def add_fund(self, fund):
        """Добавляет фонд в музей"""
        self.funds.append(fund)

    def add_item(self, item):
        """Добавляет музейный предмет"""
        self.items.append(item)

    def add_collection(self, collection):
        """Добавляет коллекцию"""
        self.collections.append(collection)

    def add_exhibition(self, exhibition):
        """Добавляет выставку"""
        self.exhibitions.append(exhibition)

    def add_organization(self, organization):
        """Добавляет организацию"""
        self.organizations.append(organization)

    def add_movement_act(self, movement_act):
        """Добавляет акт перемещения"""
        self.movement_acts.append(movement_act)

    def save_to_file(self, filename="museum_data.pkl"):
        """Сериализует все данные музея в файл"""
        data = {
            'name': self.name,
            'authors': self.authors,
            'funds': self.funds,
            'items': self.items,
            'collections': self.collections,
            'exhibitions': self.exhibitions,
            'organizations': self.organizations,
            'movement_acts': self.movement_acts
        }
        with open(filename, 'wb') as f:
            pickle.dump(data, f)

    def load_from_file(self, filename="museum_data.pkl"):
        """Десериализует данные музея из файла"""
        try:
            with open(filename, 'rb') as f:
                data = pickle.load(f)
                self.name = data['name']
                self.authors = data['authors']
                self.funds = data['funds']
                self.items = data['items']
                self.collections = data['collections']
                self.exhibitions = data['exhibitions']
                self.organizations = data['organizations']
                self.movement_acts = data['movement_acts']
            return True
        except (FileNotFoundError, pickle.PickleError):
            return False

    @timing_decorator
    @count_calls_decorator
    def __str__(self):
        """Возвращает строковое представление музея"""
        info = [
            f"Музей: {self.name}",
            f"Авторов: {len(self.authors)}",
            f"Фондов: {len(self.funds)}",
            f"Предметов: {len(self.items)}",
            f"Коллекций: {len(self.collections)}",
            f"Выставок: {len(self.exhibitions)}",
            f"Организаций: {len(self.organizations)}",
            f"Актов перемещения: {len(self.movement_acts)}"
        ]
        return "\n".join(info)


def console_app():
    museum = Museum("Мой музей")
    while True:
        print("\n=== МУЗЕЙНОЕ УПРАВЛЕНИЕ ===")
        print("1. Добавить предмет")
        print("2. Информация о предмете")
        print("3. Переместить предмет из фонда в фонд")
        print("4. Передать предмет на выставку")
        print("5. Вернуть предмет с выставки")
        print("6. Списать предмет")

        print("0. Выйти")

        choice = input("Выберите действие (0-6): ")
        
        match choice:
            case "1":
                number = int(input("Введите номер предмета: "))
                name = input("Введите название предмета: ")
                date_of_creation = input("Введите дату создания предмета: ")
                is_exactly = bool(input("Точно ли определена дата создания? (True/False): "))
                full_name = input("Введите ФИО автора: ")
                birth_date = input("Введите дату рождения автора: ")
                country = input("Введите страну автора: ")
                author = Author(full_name, birth_date, country)
                fund_name = input("Введите название фонда: ")
                annotation = input("Введите описание фонда: ")
                fund = Fund(fund_name, annotation)
                item = MuseumItem(number, name, date_of_creation, is_exactly, author, fund)
                museum.add_item(item)
            case "2":
                number = input("Введите номер предмета: ")
                found_items = [item for item in museum.items if str(item.number) == number]
                if found_items:
                    item = found_items[0]
                    print(f"Номер: {item.number}")
                    print(f"Название: {item.name}")
                    print(f"Дата создания: {item.date_of_creation}")
                    print(f"Автор: {item.author.full_name}")
                    print(f"Фонд: {item.fund.name if item.fund else 'Не указан'}")
                else:
                    print("Предмет с таким номером не найден")
            case "3":
                number = input("Введите номер предмета: ")
                found_items = [item for item in museum.items if str(item.number) == number]
                if found_items:
                    item = found_items[0]
                    name = input("Введите название нового фонда: ")
                    found_funds = [fund for fund in museum.funds if str(fund.name) ==name]
                    if found_funds:
                        to_fund = found_funds[0]
                        movement_date = input("Введите дату перемещения (ДД.ММ.ГГГГ): ")
                        movement = MovementAct(
                            movement_type="Внутреннее перемещение",
                            movement_date=movement_date,
                            item=item
                        )
                        movement.to_fund = to_fund
                        movement.internal_movement()
                        museum.movement_acts.append(movement)

                        print(f"Предмет '{item.name}' перемещен в фонд '{to_fund.name}'")
                else:
                    print("Предмет с таким номером не найден")
            case "4":
                number = input("Введите номер предмета: ")
                found_items = [item for item in museum.items if str(item.number) == number]
                if found_items:
                    item = found_items[0]
                    name = input("Введите название новой выставки: ")
                    found_exhibitions = [exhibition for exhibition in museum.exhibitions if str(exhibition.name) == name]
                    if found_exhibitions:
                        exhibition = found_exhibitions[0]
                        movement_date = input("Введите дату перемещения (ДД.ММ.ГГГГ): ")
                        movement = MovementAct(
                            movement_type="Передача на выставку",
                            movement_date=movement_date,
                            item=item
                            )
                        movement.exhibition = exhibition
                        movement.exhibition_transfer()
                        museum.movement_acts.append(movement)
                else:
                    print("Предмет с таким номером не найден")
            case "5":
                number = input("Введите номер предмета: ")
                found_items = [item for item in museum.items if str(item.number) == number]
                if found_items:
                    item = found_items[0]
                    name = input("Введите название выставки: ")
                    found_exhibitions = [exhibition for exhibition in museum.exhibitions if
                                         str(exhibition.name) == name]
                    if found_exhibitions:
                        exhibition = found_exhibitions[0]
                        movement_date = input("Введите дату перемещения (ДД.ММ.ГГГГ): ")
                        movement = MovementAct(
                            movement_type="Возвращение с выставки",
                            movement_date=movement_date,
                            item=item
                        )
                        movement.exhibition = exhibition
                        movement.exhibition_return()
                        museum.movement_acts.append(movement)
                else:
                    print("Предмет с таким номером не найден")
            case "6":
                number = input("Введите номер предмета: ")
                found_items = [item for item in museum.items if str(item.number) == number]
                if found_items:
                    item = found_items[0]
                    movement_date = input("Введите дату перемещения (ДД.ММ.ГГГГ): ")
                    movement = MovementAct(
                        movement_type="Списание",
                        movement_date=movement_date,
                        item=item
                        )
                    movement.write_off()
                    museum.movement_acts.append(movement)
                else:
                    print("Предмет с таким номером не найден")
            case "0":
                print("Выход из программы")
                break
            case _:
                print("Неверный выбор. Пожалуйста, попробуйте снова.")

if __name__ == '__main__':
    console_app()