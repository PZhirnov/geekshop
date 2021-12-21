import os.path

from django.shortcuts import render, get_object_or_404
import json
from .models import ProductCategory, Product
from basketapp.models import Basket
import random

# Create your views here.



''' Главное меню сайта, которое встраивается на каждой странице.
products -- написать так -- products:index сделать обязательно, учитывая то, что использщовался include в urls
'''
main_menu = [
    {'menu_section': 'index', 'main_urls': 'index', 'name': 'Главная'},
    {'menu_section': 'products:index',  'main_urls': 'products', 'name': 'Продукты'},
    {'menu_section': 'contact',  'main_urls': 'contact', 'name': 'Контакты'},
]


def get_basket(user):
    if user.is_authenticated:
        return Basket.objects.filter(user=user)
    else:
        return []

# Горячее предложение
def get_hot_product():
    products = Product.objects.all()
    return random.sample(list(products), 1)[0]

# Похожие продукты
def get_same_products(hot_product):
    same_products = Product.objects.filter(category=hot_product.category).exclude(pk=hot_product.pk)[:3]
    return same_products




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
    # print(pk) - можно получить id, если он будет передан в products
    # путь к файлу с данными json - 1 вариант вывода
    # file_path = os.path.join(module_dir, 'json_products/products.json')
    # products_data = json.load(open(file_path, 'r', encoding='utf8'))[:3]

    title = 'продукты'
    basket = []
    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)

    # Вариант вывода по запросу для категории
    # 1. Получим все категории
    links_menu = ProductCategory.objects.all()

    if pk is not None:
        if pk == 0:
            products = Product.objects.all().order_by('price')
            category = {'name': 'все'}
        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            products = Product.objects.filter(category__pk=pk).order_by('price')
        print(basket[0].product)
        content = {
            'title': 'Продукты',
            'links_menu': links_menu,
            'main_menu': main_menu,
            'user_info': user,
            'products': products,
            'category': category,
            'basket': basket,
        }
        return render(request, 'mainapp/products_list.html', content)

    # Горячее предложение
    hot_product = get_hot_product()
    same_products = get_same_products(hot_product)

    content = {
        'title': 'Продукты',
        'links_menu': links_menu,
        'main_menu': main_menu,
        'hot_product': hot_product,
        'same_products': same_products,
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

# Страница продукта
def product(request, pk):
    title = 'продукты'

    content = {
        'title': title,
        'links_menu': ProductCategory.objects.all(),
        'product': get_object_or_404(Product, pk=pk),
        'basket': get_basket(request.user),
    }

    return render(request, 'mainapp/product.html', content)

