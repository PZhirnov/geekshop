from django.shortcuts import render
import json

# Create your views here.

''' Формируем данные для создания меню категорий на странице products
обращаемся к href и получаем ссылки, обращаемся к name и получаем название категории '''

links_menu = [
    {'href': 'products_all', 'name': 'все'},
    {'href': 'products_home', 'name': 'дом'},
    {'href': 'products_office', 'name': 'офис'},
    {'href': 'products_modern', 'name': 'модерн'},
    {'href': 'products_classic', 'name': 'классика'},
]

''' Главное меню сайта, которое встраивается на каждой странице
'''
main_menu = [
    {'menu_section': 'index', 'name': 'Главная'},
    {'menu_section': 'products', 'name': 'Продукты'},
    {'menu_section': 'contact', 'name': 'Контакты'},
]

''' Подгружаем данные о пользователе из json '''


def user_info(user_login):
    with open("users_bd.json", "r") as read_file:
        data_user = json.load(read_file)
    return data_user.get(user_login)


user = user_info('user_login')


def index(request):
    content = {
        'title': 'Главная',
        'main_menu': main_menu,
        'user_info': user,
    }
    return render(request, 'mainapp/index.html', content)


def products(request):
    content = {
        'title': 'Продукты',
        'links_menu': links_menu,
        'main_menu': main_menu,
        'user_info': user,
    }
    return render(request, 'mainapp/products.html', content)


def contact(request):
    content = {
        'title': 'Контакты',
        'main_menu': main_menu,
        'user_info': user,
    }
    return render(request, 'mainapp/contact.html', content)


''' Тестовая функция '''
def context(request):
    # данные, которые будут передаваться в шаблон
    content = {
        'title': 'магазин',
        'header': 'Добро пожаловать на сайт',
        'username': 'Иван Иванов',
        'products': [
            {'name': 'Стулья', 'price': 4535},
            {'name': 'Диваны', 'price': 1535},
            {'name': 'Кровати', 'price': 2535},
        ]
    }
    return render(request, 'mainapp/test_context.html', content)
