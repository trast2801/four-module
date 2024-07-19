import sqlite3

from pythonProject.sale_bot.config import path


def get_blank_of_order(number_order, cursor):

    sql_get = """SELECT number_order, data_order, users.name, users.phone, users.adress
                 FROM order_customer, users WHERE order_customer.number_order = ? AND users.id_telegram = order_customer.id_user """
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


def all_order(cursor, id_user_telegram):
    sql_get = """ SELECT number_order, data_order,sum(pric)  from order_customer, price 
                    WHERE 
                    order_customer.id_price = price.id and order_customer.id_user = ?
                    GROUP by number_order """
    data_tuple = (id_user_telegram,)
    cursor.execute(sql_get, data_tuple)
    rec = cursor.fetchall()
    return rec

def write_order_to_file(cursor):
    specification, head = get_blank_of_order(2,cursor)
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
    return stroka
