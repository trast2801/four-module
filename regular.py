import re

def has_cyrillic(text):
    return bool(re.search('[a-zA-Z]', text) or  text.isalnum())

def has_cyrillic_adress(text):
    return bool(re.search('[a-zA-Z]', text))

def check_adress(text):

    numbers_list = text.split(",")
    if has_cyrillic(numbers_list[0]):
        return ('В ФИО используйте только русские буквы \n')
    if has_cyrillic_adress(numbers_list[1]):
        return ('В адресе используйте только русские буквы \n')
    if re.match(r'[78][0-9]{10}', numbers_list[2].replace(' ','')) :
        return True
    else:
        print(print('Телефон должен содержат только цифры \n'
              'Пример: 89623845406'))
        return False

text = "Сидоров иван петрович, г Москва  кр площадь 2, 79622845406"

print(check_adress(text))