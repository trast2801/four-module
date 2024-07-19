from aiogram.types import ReplyKeyboardMarkup,KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
'''
start_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Стоимость"),
            KeyboardButton(text="О нас")
        ]
    ], resize_keyboard=True
)
'''

catalog_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Каталог', callback_data="catalog")],
        [InlineKeyboardButton(text= "Корзина", callback_data= "basket")],
        [InlineKeyboardButton(text= "Мои заказы", callback_data= "my_order")],
        [InlineKeyboardButton(text = "Новости", callback_data= "news", url="https://t.me/tshirtsok")],
        [InlineKeyboardButton(text = "Информация о нас", callback_data= "about")]
    ]
)

buy_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Купить!", url = "http://ya.ru")],
        [InlineKeyboardButton(text="Назад", callback_data="back_to_catalog")]
    ]
)

ok_kb = InlineKeyboardMarkup(
    inline_keyboard =[[InlineKeyboardButton(text="Ок", callback_data='ok')]]
)

ok_basket = InlineKeyboardMarkup(
    inline_keyboard =[[InlineKeyboardButton(text="Ок", callback_data='ok_basket')]]
)

serfcatalog_kb = InlineKeyboardMarkup(
    inline_keyboard =[
        [InlineKeyboardButton (text = 'Вперед', callback_data='forward_db')],
        [InlineKeyboardButton (text = 'Назад', callback_data='back_db')],
        [InlineKeyboardButton(text= 'В Корзину', callback_data='basket_add')],
        [InlineKeyboardButton(text = 'В начало', callback_data ='main')]
    ]
)

basket_kb = InlineKeyboardMarkup(
    inline_keyboard = [
        [InlineKeyboardButton (text =' Ваша корзина', callback_data='choice_bd')],
        [InlineKeyboardButton (text =' Очистить Корзину', callback_data= 'clear_bd' )],
        [InlineKeyboardButton (text =' Оформить заказ', callback_data= 'order')],
        [InlineKeyboardButton (text= 'Вернуться в начало', callback_data='main')]
    ]
)

admin_panel = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Пользователи", callback_data="users")],
        [InlineKeyboardButton(text="Статистика", callback_data="stat")],
        [
        InlineKeyboardButton(text="Блокировка", callback_data="block"),
        InlineKeyboardButton(text="Разблокировка", callback_data="unblock")
        ]
    ]
)

