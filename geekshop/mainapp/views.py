import os.path

from django.shortcuts import render
import json
from .models import ProductCategory, Product


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

''' Главное меню сайта, которое встраивается на каждой странице.
products -- написать так -- products:index сделать обязательно, учитывая то, что использщовался include в urls
'''
main_menu = [
    {'menu_section': 'index', 'main_urls': 'index', 'name': 'Главная'},
    {'menu_section': 'products:index',  'main_urls': 'products', 'name': 'Продукты'},
    {'menu_section': 'contact',  'main_urls': 'contact', 'name': 'Контакты'},
]


''' Подгружаем данные о пользователе из json - это только для теста сделано'''


def user_info(user_login):
    with open("users_bd.json", "r", encoding="utf8") as read_file:
        data_user = json.load(read_file)
    return data_user.get(user_login)


user = user_info('user_login')

''' получаем текущую директорию '''
module_dir = os.path.dirname(__file__)


def index(request):
    products = Product.objects.all()[:4]
    content = {
        'title': 'Главная',
        'main_menu': main_menu,
        'user_info': user,
        'products': products
    }
    return render(request, 'mainapp/index.html', content)


def products(request, pk=None):
    print(pk)  # вернем id, если он будет передан в products
    # путь к файлу с данными json
    file_path = os.path.join(module_dir, 'json_products/products.json')
    # products в последствии передаем в список словарей, из которого берем данные по продуктам
    products_data = json.load(open(file_path, 'r', encoding='utf8'))[:3]

    content = {
        'title': 'Продукты',
        'links_menu': links_menu,
        'main_menu': main_menu,
        'user_info': user,
        'products': products_data,
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
