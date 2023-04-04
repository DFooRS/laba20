#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os.path
import sys
import click
import json
import jsonschema
from jsonschema import validate


schema = {
    "type": "object",
    "properties": {
        "product": {
            "type": "string"
        },
        "shop": {
            "type": "string"
        },
        "cost": {
            "type": "number"
        }
    }
}


def add_product(products, prod, shop, cost):
    """
    Ввод информации о товарах.
    """
    products.append(
        {
            "product": prod,
            "shop": shop,
            "cost": cost
        }
    )
    return products


def save_products(file_name, products):
    """
    Сохранить список всех товаров в формате JSON
    """
    with open(file_name, "w", encoding="utf-8") as fout:
        json.dump(products, fout, ensure_ascii=False, indent=4)


def load_products(file_name):
    """
    Загрузить список всех товаров из файла JSON
    """
    with open(file_name, "r", encoding="utf-8") as fin:
        return json.load(fin)


def product_list(products):
    """
    Вывод списка товаров
    """
    if products:
        line = '+-{}-+-{}-+-{}-+'.format(
            '-' * 4,
            '-' * 30,
            '-' * 20
        )
        print(line)
        print(
            '| {:^25} | {:^15} | {:^14} |'.format(
                "Товар",
                "Магазин",
                "Стоимость"
            )
        )
        print(line)

        for product in products:
            print(
                '| {:^25} | {:^15} | {:^14} |'.format(
                    product.get('product', ''),
                    product.get('shop', ''),
                    product.get('cost', 0)
                )
            )
            print(line)


def select(products, shop):
    """
    Выбрать товары из конкретного магазина.
    """
    result = []
    for product in products:
        if product.get('shop', '') == shop:
            result.append(product)
    return result


def validation(json_data):
    """
    Валидация данных
    """
    try:
        validate(instance=json_data, schema=schema)
    except:
        raise jsonschema.exceptions.ValidationError("Данные недействительны")

    msg = "Данные успешно загружены"
    return True, msg

@click.command()
@click.argument('command')
@click.argument('filename')
@click.option('--name', help='Название продукта')
@click.option('--shop', help='Название магазина')
@click.option('--cost', help='Стоимость товара')

def main(command, filename, name, shop, cost):
    """
    Главная функция программы.
    """
    is_dirty = False
    if os.path.exists(filename):
        products = load_products(filename)
    else:
        products = []

    if command == 'add':
        name = click.prompt("Введите название товара: ")
        shop = click.prompt("Введите название магазина: ")
        cost = click.prompt("Введите стоимость товара: ")
        products = add_product(
            products,
            name,
            shop,
            cost
        )
        is_dirty = True

    elif command == 'list':
        product_list(products)

    elif command == 'select':
        shop = click.prompt("Введите название магазина: ")
        selected = select(products, shop)
        product_list(selected)

    if is_dirty:
        save_products(filename, products)


if __name__ == '__main__':
    main()
