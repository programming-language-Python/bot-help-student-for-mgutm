from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from utils.db_api.db_commands import count_items, get_items, get_categories

# Создаем CallbackData-объекты, которые будут нужны для работы с менюшкой
menu_cd = CallbackData("show_menu", "level", "category", "item_id", "photo")
buy_item = CallbackData("buy", "item_id")


# С помощью этой функции будем формировать коллбек дату для каждого элемента меню, в зависимости от
# переданных параметров. Если Подкатегория, или айди товара не выбраны - они по умолчанию равны нулю
def make_callback_data(level, category="0", item_id="0", photo="0"):
    return menu_cd.new(level=level, category=category, item_id=item_id, photo=photo)


# Создаем функцию, которая отдает клавиатуру с доступными категориями
async def categories_keyboard():
    # Указываем, что текущий уровень меню - 0
    CURRENT_LEVEL = 0

    # Создаем Клавиатуру
    markup = InlineKeyboardMarkup()

    # Забираем список товаров из базы данных с РАЗНЫМИ категориями и проходим по нему
    categories = await get_categories()
    for category in categories:
        # Чекаем в базе сколько товаров существует под данной категорией
        number_of_items = await count_items(category.category_code)

        # Сформируем текст, который будет на кнопке
        button_text = f"{category.category_name} ({number_of_items} шт)"

        # Сформируем колбек дату, которая будет на кнопке. Следующий уровень - текущий + 1, и перечисляем категории
        callback_data = make_callback_data(level=CURRENT_LEVEL + 1, category=category.category_code,
                                           photo=category.photo)

        # Вставляем кнопку в клавиатуру
        markup.row(
            InlineKeyboardButton(text=button_text, callback_data=callback_data)
        )

    # Возвращаем созданную клавиатуру в хендлер
    return markup


# Создаем функцию, которая отдает клавиатуру с доступными товарами, исходя из выбранной категории и подкатегории
async def items_keyboard(category):
    CURRENT_LEVEL = 1

    # Устанавливаю row_width = 1, чтобы показывалась одна кнопка в строке на товар
    markup = InlineKeyboardMarkup(row_width=1)

    # Забираем список товаров из базы данных с выбранной категорией и подкатегорией, и проходим по нему
    items = await get_items(category)
    for item in items:
        # Сформируем текст, который будет на кнопке
        button_text = f"{item.name}"

        # Сформируем колбек дату, которая будет на кнопке
        callback_data = make_callback_data(level=CURRENT_LEVEL + 1,
                                           category=category,
                                           item_id=item.id, photo=item.photo)
        markup.insert(
            InlineKeyboardButton(
                text=button_text, callback_data=callback_data)
        )

    # Создаем Кнопку "Назад", в которой прописываем колбек дату такую, которая возвращает
    # пользователя на уровень назад - на уровень 1 - на выбор подкатегории
    markup.row(
        InlineKeyboardButton(
            text="Назад",
            callback_data=make_callback_data(level=CURRENT_LEVEL - 1,
                                             category=category))
    )
    return markup


# Создаем функцию, которая отдает клавиатуру с кнопками "купить" и "назад" для выбранного товара
def item_keyboard(category, item_id):
    CURRENT_LEVEL = 2
    markup = InlineKeyboardMarkup()

    btn_cancel = InlineKeyboardButton(
        text="Назад",
        callback_data=make_callback_data(level=CURRENT_LEVEL - 1,
                                         category=category))
    markup.insert(btn_cancel)

    btn_to_the_begining = InlineKeyboardButton(
        text="В начало",
        callback_data=make_callback_data(level=0,
                                         category=category))
    markup.insert(btn_to_the_begining)

    return markup
