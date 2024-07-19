import datetime
from asyncio import sleep

import aiogram
from aiogram import Bot, Dispatcher, executor, types
import asyncio
import logging
from aiogram.dispatcher.filters import Command, Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.webhook import DeleteMessage
from aiogram.types import InputMediaPhoto
import pythonProject.sale_bot.texts.stat
import keyboards
import sqlite3
import pythonProject.sale_bot.texts.admin
import database
import config

from pythonProject import texts
from pythonProject.sale_bot import regular
from pythonProject.sale_bot.texts import stat, db_product
from pythonProject.sale_bot.texts.db_product import path

api = config.API
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())
counter = 0

global connection
global cursor
global custom_basket # корзина покупателя
global buffer_basket
global Flag #убирает все сообщения пользователя. кроме входа в оформление заказа

Flag: bool = False
custom_basket = {}
@dp.message_handler(commands=['start'])
async  def start(message):
    global connection
    global cursor


    connection = sqlite3.connect(path + 'db_product.db', timeout=5)
    cursor = connection.cursor()


    await message.answer(f".                  @{message.from_user.username:*^5}" + stat.start, parse_mode='HTML',
                         reply_markup= keyboards.catalog_kb)




@dp.message_handler(commands=['stop'])
#после тестировани закрыть стоп
async def stop_(message):
    connection.commit()
    cursor.close()
    hideBoard = types.ReplyKeyboardRemove()
    await message.answer(f"Досвидания  @{message.from_user.username:*^5} "
                     "надеемся, что ты хорошо провел(а) время \n\n"
                    , parse_mode='html', reply_markup=hideBoard)

    exit()

@dp.callback_query_handler(text = 'about')
async def about_as(call):
    with open('files/media/about.jpg', "rb") as img:
        await call.message.answer_photo(img, stat.about_as, parse_mode ='HTML',reply_markup=keyboards.ok_kb)
        await call.answer()
        await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
        await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id - 1)
        await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id - 2)

@dp.callback_query_handler(text='ok')
async def ok(call):
    await (call.message.answer(stat.head, parse_mode='HTML', reply_markup=keyboards.catalog_kb))

    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id )
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id - 1)
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id - 2)
    await call.answer()
@dp.callback_query_handler(text='news')
async def news(call):
    await call.message.answer (stat.head, parse_mode='HTML')
    await call.answer()

@dp.callback_query_handler(text='catalog')
async def show_product(call):
    global list_id_product
    global counter
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    record,count, list_id_product = db_product.get_product(1,cursor)
    counter = 1
    cid = call.message.chat.id
    for row in record:
        id = row[0]
        polotno = row[1]
        size = row[2]
        name = row[3]
        photos = row[4]

    await bot.send_photo(chat_id=cid, photo=photos, caption=f'{name.center(100)} \n'
                                                            f'              размер  - {size} \n'
                                                            f'              полотно - {polotno}\n'
                                                            f'Это {id}-й товар из {count}'
                         )
    await call.message.answer('Используйте кнопки меню \n для просмотра каталога',
                              reply_markup=keyboards.serfcatalog_kb)
    


@dp.callback_query_handler(text = 'main')
async def back_to_main(call):
    try:
        await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id - 1)
        await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    except Exception as ex:
        print(' удалять нечего')
    await call.message.answer(stat.head, parse_mode='HTML', reply_markup=keyboards.catalog_kb)
    await call.answer()
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)

@dp.callback_query_handler(text = 'forward_db')
async def forward(call):
    global counter
    global buffer_basket
    counter += 1
    record, count, all_id = db_product.get_product(counter, cursor)

    if counter > count:
        await call.message.answer('Это последний товар в списке \n'
                                  'Используйте кнопку НАЗАД  \n '
                                  'для просмотра каталога или \n'
                                  'В начало - для возврата',
                                  reply_markup=keyboards.serfcatalog_kb)
        counter = count
        await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id-1)
        await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
        await call.answer()
    else:
        cid = call.message.chat.id
        for row in record:
            id = row[0]
            polotno = row[1]
            size = row[2]
            name = row[3]
            photos = row[4]
        buffer_basket = id
        try:
            await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
            await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id-1)
        except Exception as ex:
            print(' удалять нечего')

        await bot.send_photo(chat_id=cid, photo=photos, caption=f'{name.center(100)} \n'
                                                                f'              размер  - {size} \n'
                                                                f'              полотно - {polotno}\n'
                                                                f'Это {id }-й товар из {count}'

                             )
        await call.message.answer('Используйте кнопки меню \n для просмотра каталога',
                                  reply_markup=keyboards.serfcatalog_kb)

        await call.answer()

@dp.callback_query_handler(text = 'back_db')
async def step_back(call):
    global counter
    counter -= 1
    record, count, all_id = db_product.get_product(counter, cursor)

    if counter <= 0 :
        try:
            await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
            await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id-1)
        except Exception as ex:
            print(' удалять нечего')
        await call.message.answer('Это первый товар в списке \n'
                                  'Используйте кнопку ВПЕРЕД  \n '
                                  'для просмотра каталога или \n'
                                  'В начало - для возврата',
                                  reply_markup=keyboards.serfcatalog_kb)
        counter = 0
        try:
            await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id - 2)
            await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id-1)
            await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
        except Exception as ex:
            print(' удалять нечего')
        await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
        #await call.answer()
    else:
        cid = call.message.chat.id
        for row in record:
            id = row[0]
            polotno = row[1]
            size = row[2]
            name = row[3]
            photos = row[4]
        try:
            await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id-1)
            await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
        except Exception as ex:
            print(' удалять нечего')

        await bot.send_photo(chat_id=cid, photo=photos, caption=f'{name.center(100)} \n'
                                                                f'              размер  - {size} \n'
                                                                f'              полотно - {polotno}\n'
                                                                f'Это {id}-й товар из {count}'
                             )
        await call.message.answer('Используйте кнопки меню \n для просмотра каталога',
                                  reply_markup=keyboards.serfcatalog_kb)

        await call.answer()
        await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)

@dp.callback_query_handler(text ='basket')
async def basket_db(call):
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    await call.message.answer('Корзина', reply_markup=keyboards.basket_kb)
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)

    await call.answer()

@dp.callback_query_handler(text='basket_add')
async def basket_ad(call):
    global  counter
    global custom_basket
    #custom_basket индекс/ключ  это id_товара, значение - это колл-во
    #custom_basket.append([buffer_basket, 1])
    flag = False
    for key in custom_basket:
        if buffer_basket ==  key:
            custom_basket[buffer_basket] = custom_basket[buffer_basket] + 1
            flag = True
            break
    if not flag:
        custom_basket[buffer_basket] = 1

    record, count, all_id = db_product.get_product(counter, cursor)

    if counter <= 0:
        await call.message.answer('Это первый товар в списке \n'
                                  'Используйте кнопку ВПЕРЕД  \n '
                                  'для просмотра каталога или \n'
                                  'В начало - для возврата',
                                  reply_markup=keyboards.serfcatalog_kb)
        counter = 0
        await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
        # await call.answer()
    else:
        cid = call.message.chat.id
        for row in record:
            id = row[0]
            polotno = row[1]
            size = row[2]
            name = row[3]
            photos = row[4]
        await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id - 1)
        await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
        await bot.send_photo(chat_id=cid, photo=photos, caption=f'{name.center(100)} \n'
                                                                f'              размер  - {size} \n'
                                                                f'              полотно - {polotno}\n'
                                                                f'Это {id}-й товар из {count}'
                             )
        await call.message.answer('Используйте кнопки меню \n для просмотра каталога',
                                  reply_markup=keyboards.serfcatalog_kb)

        await call.answer()
        #await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)

@dp.callback_query_handler(text = 'choice_bd')
async def print_basket(call):
    prn_basket = ''
    for key_id in custom_basket:
        prn_basket += (db_product.get_product_from_basket(key_id,cursor) + 'штук: '
                       + str(custom_basket[key_id])) + '\n'
    await call.message.answer(prn_basket, reply_markup=keyboards.ok_basket)
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)

@dp.callback_query_handler(text = 'ok_basket')
async def back_ok(call):
    await call.message.answer('Корзина', reply_markup=keyboards.basket_kb)
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)

@dp.callback_query_handler(text = 'clear_bd')
async def clear_basket(call):
    custom_basket.clear()

@dp.callback_query_handler(text = 'order')
async def order(msg):
    global Flag
    Flag = True
    await msg.answer ('Напишите ниже ФИО, адрес для отправки, телефон \n'
                              
                              'Пример:'
                              'Вассер Иван Петрович, Москва красная площадь д2 , 89622845406',)

@dp.message_handler(content_types='text')
async def txt(message, user_id=None):
    global Flag
    global cursor

    kotakt_usr = (message.text)
    if Flag:
        if regular.check_adress(kotakt_usr) != True:
            cid = message.chat.id
            await bot.send_message(chat_id=cid, text="неверный ввод, должно быть так:\n"
                         "Сидоров иван петрович, г. Москва  кр площадь 2, 8963545406\n",)
        else:
            numbers_list = kotakt_usr.split(",")
            user_id = message.from_user.id
            name = numbers_list[0]
            adress = numbers_list[1]
            phone = numbers_list[2]
            db_product.insert_user(name, user_id, adress, phone, cursor, connection)
            number_order = db_product.get_last_number_order(cursor)
            data_order = datetime.date.today().strftime('%d-%m-%Y')
            db_product.write_order_bd(user_id, custom_basket,number_order, data_order,cursor, connection)
            msg = f'Ваш заказ принят\n номер заказа {number_order}, дата заказа {data_order}'
            db_product.write_order_to_file(number_order, cursor)
            #await bot.send_document(message.chat.id, 'c:\\order.txt')
            await message.answer (msg, reply_markup=keyboards.basket_kb)
            Flag = False
    else:
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)

@dp.callback_query_handler(text =  "my_order")
async def all_order(call):
    id_user_telegram = call.message.chat.id
    rec = db_product.all_order(id_user_telegram,cursor)
    s_out =''
    for i in rec:
        s_out += f'номер заказа: {i[0]} | data заказа {i[1]} | сумма заказа {i[2]} \n'
    await call.message.answer(s_out,reply_markup=keyboards.ok_kb)
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)

if __name__ == "__main__":

    executor.start_polling(dp, skip_updates=True)

