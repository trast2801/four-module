import sqlite3
from asyncio import sleep
from typing import Tuple, Any

path = "C:\\Users\\Konst\\PycharmProjects\\telebot2\\pythonProject\\sale_bot\\files\\"
path_media = "C:\\Users\\Konst\\PycharmProjects\\telebot2\\pythonProject\\sale_bot\\files\\media\\"
def init_db():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            id_telegram INTEGER NOT NULL,
            adress  TEXT NOT NULL
        );
    ''')
    cursor.execute("""
         CREATE TABLE IF NOT EXISTS product(
             id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
             product_name TEXT NOT NULL,
             polotno TEXT NOT NULL,
             size TEXT NOT NULL,
             photo BLOB
    
         );
     """)

    cursor.execute("""
         CREATE TABLE IF NOT EXISTS price(
             id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
             id_product  INTEGER,
             price INTEGER NOT NULL
         );
     """)

    cursor.execute("""
         CREATE TABLE IF NOT EXISTS order_customer(
             id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
             id_user INTEGER,
             id_product INTEGER,
             id_price INTEGER,
             id_size INTEGER,
             data_order DATE NOT NULL,
             number_order TEXT NOT NULL,
             quantity INTEGER NOT NULL        
         );
     """)

def convert_to_binary_data(filename):
    with open(filename, 'rb') as file:
        blob_data = file.read()
    return blob_data

def insert_blob(name, photo, size, polotno):

        insert_blob_query = """INSERT INTO product
                                  (name, photo, size, polotno) VALUES (?, ?, ?, ?)"""
        emp_photo = convert_to_binary_data(photo)
        # Преобразование данных в формат кортежа
        data_tuple = (name, emp_photo, size, polotno)
        cursor.execute(insert_blob_query, data_tuple)
        connection.commit()
        #"Изображение и файл успешно вставлены как BLOB в таблиу"
        cursor.close()

def get_id_product():
    result = ()
    #conn = sqlite3.connect(path +' db_product.db')
    conn = sqlite3.connect(path + ' db_product.db')
    cur = conn.cursor()
    print("Подключен к SQLite")
    query =  """SELECT id FROM product"""
    cur.execute(query)
    result = cur.fetchall()
    return result

def get_product_from_basket(id, cursor):

    sql_fetch_blob_query = """SELECT  product.name, product.polotno,	product.size, price.pric 
                            FROM product, price
                            WHERE
                            product.id = price.id_product and product.id = ?"""
    cursor.execute(sql_fetch_blob_query, (id,))
    record = cursor.fetchall()

    for row in record:
        size    = row[2]
        name    = row[0]
        polotno = row[1]
        price   = row[3]

    #sql_get_price = """SELECT price from price where id = ? """
    #cursor.execute(sql_get_price, 2)
    #record = cursor.fetchone()

    rezult = f'{name}  из {polotno}  размер {size} цена за штуку {price} '
    return rezult

def get_product(id, cursor):

    global all_id
    #try:
    #conn = sqlite3.connect(path +'db_product.db')
    #cursor = conn.cursor()
    print("Подключен к SQLite")

    sql_fetch_blob_query = """SELECT * from product where id = ?"""
    cursor.execute(sql_fetch_blob_query, (id,))
    record = cursor.fetchall()
    query = """SELECT Count(*) FROM product"""
    cursor.execute(query)
    vsego_zapisei = cursor.fetchone()[0]
    query = """SELECT id FROM product"""
    cursor.execute(query)
    all_id = cursor.fetchall()
    print(all_id)
    return record, vsego_zapisei, all_id
'''        #for row in record:
         #   id      = row[0]
         #   name    = row[1]
         #   photo   = row[2]
         #   size    = row[3]
         #   polotno = row[4]
         # 
         #   print( id, name, photo, count)
        #cursor.close()
    #except sqlite3.Error as error:
    #    print("Ошибка при работе с SQLite", error)
    #finally:
    #    if conn:
    #       conn.close()
    #        print("Соединение с SQLite закрыто")
'''


def insert_user(name, id_teleg, adress, phone,cursor, connection):

    ss = """ SELECT id_telegram  FROM users WHERE id_telegram = ?"""
    data_tuple = (id_teleg,)
    cursor.execute(ss, data_tuple)
    record = cursor.fetchone()
    if record == None:
        try:
            insert_blob_query = """INSERT INTO users
                                               (name, id_telegram, adress, phone) VALUES (?, ?, ?, ?)"""
            data_tuple = (name, id_teleg, adress, phone)
            cursor.execute(insert_blob_query, data_tuple)
        except sqlite3.Error as err:
            print(err)
        finally:
            connection.commit()

def write_order_bd(id_user, custom_basket, number_order, data_order, cursor, connection):
    if custom_basket == {}:
        return
    else:
        for key in custom_basket:
            product = key
            quantity = custom_basket[key]
            sql_get = """ SELECT size FROM product WHERE id = ?"""
            data_tuple: tuple[Any] = (product,)
            cursor.execute(sql_get, data_tuple)
            size = cursor.fetchone()[0]
            sql_get = """ SELECT id FROM price WHERE id = ?"""
            data_tuple0 = (product,)
            cursor.execute(sql_get,data_tuple0)
            price = cursor.fetchone()[0]
            sql_write = """ INSERT INTO order_customer 
                            (id_user, id_product, id_price, id_size, data_order, number_order, quantity)
                            VALUES (?,?,?,?,?,?,?)"""
            data_tuple1 = (id_user, product, price, size, data_order, number_order, quantity)
            cursor.execute(sql_write,data_tuple1)
            connection.commit()
def get_last_number_order(cursor):
    sql_get = """ SELECT MAX(number_order) FROM order_customer"""
    cursor.execute(sql_get)
    rez = int(cursor.fetchone()[0])
    rez += 1
    return rez

def get_blank_of_order(number_order, cursor):

    sql_get = """SELECT number_order, data_order, users.name, users.phone, users.adress
                 FROM order_customer, users
                 WHERE order_customer.number_order = ? AND users.id_telegram = order_customer.id_user """
    data_tuple = (number_order,)

    cursor.execute(sql_get, data_tuple)
    rec_head = cursor.fetchone()
    # number_order = rec[0]
    # data_order = rec[1]
    # customer_name = rec[2]
    # customer_adress = rec[3]
    # customer_phone = rec[4]
    sql_get1 = """ select quantity, pric, product.name, id_size
                 FROM order_customer, price, product
                 WHERE
                 order_customer.number_order = ? AND order_customer.id_price = price.id
                 AND order_customer.id_product = product.id """
    cursor.execute(sql_get1, data_tuple)
    # rec_specification[0] - кол-во
    # rec_specification[1] - цена
    # rec_specification[2] - наименование
    # rec_specification[3] - размер
    rec_specification = cursor.fetchall()

    return rec_specification, rec_head

def all_order(id_user_telegram, cursor):
    sql_get = """ SELECT number_order, data_order,sum(pric)  from order_customer, price 
                    WHERE 
                    order_customer.id_price = price.id and order_customer.id_user = ?
                    GROUP by number_order """
    data_tuple = (id_user_telegram,)
    cursor.execute(sql_get, data_tuple)
    rec = cursor.fetchall()
    return rec

def write_order_to_file(number_order, cursor):
    specification, head = get_blank_of_order(number_order,cursor)
    str_specification = ''
    stroka = (f'заказ номер {head[0]} дата заказа {head[1]} \n'
              f'Покупатель: {head[2]}\n'
              f'Адрес покупателя {head[3]}\n'
              f'телефон покупателя {head[4]}\n'
              f'====================================================================== \n'
              f'Наименование        |Размер | Цена    |  кол-во |\n')

    for i in specification:
        str_specification += f'{i[2].ljust(18)}  |   {i[3]}  | {str(i[1]).ljust(6)}  |   {str(i[0]).ljust(4)}  |\n'
    stroka  += str_specification
    with open("order.txt", "w", encoding="utf8") as file:
        file.write(stroka)
    return


'''
select number_order, data_order, quantity, pric, product.name, id_size, users.name, users.phone, users.adress

FROM order_customer, price, product, users

WHERE
order_customer.number_order = 3 AND order_customer.id_price = price.id
AND order_customer.id_product = product.id AND users.id_telegram = order_customer.id_user

'''

'''
    ss = """ SELECT id_telegram  FROM users WHERE id_telegram = ?"""
    
    data_tuple = (id_teleg,)
    cursor.execute(ss,data_tuple)
    record = cursor.fetchone()
    #if record != None:
'''


'''
#convert_to_binary_data('C:\\Users\\Konst\\PycharmProjects\\telebot2
# \\pythonProject\\sale_bot\\files\\media\\2.jpg')

ss='C:\\Users\\Konst\\PycharmProjects\\telebot2\\pythonProject\\sale_bot\\files\\media\\4.jpg'
connection = sqlite3.connect(path +'db_product.db')
cursor = conn.cursor()
init_db()
connection.commit()
cursor.close()
#insert_blob('4 футболка', ss, 40, 'красивое')
rr = get_product(3)
insert_user('Иванов', 19292929, 'Москва, красная площадь, дом 1')
'''

