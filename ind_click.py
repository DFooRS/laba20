#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os.path
import click
import json
import jsonschema
from jsonschema import validate
from prod_schema import schema


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
        products = json.load(fin)
    for prod in products:
        is_valid, msg = validation(prod)
        print(prod)
        print(msg)
    return products


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


def select_products(products, shop):
    """
    Выбрать товары из конкретного магазина.
    """
    result = []
    for product in products:
        if product.get('shop', '') == shop:
            result.append(product)
    return result


@click.group()
@click.pass_context
def main(ctx):
    """
    Главная функция программы.
    """
    ctx.ensure_object(dict)


@main.command()
@click.pass_context
@click.argument('filename', type=click.Path(exists=True))
@click.option('--name', prompt='Введите название товара')
@click.option('--shop', prompt='Введите название магазина')
@click.option('--cost', prompt='Введите стоимость товара', type=float)
def add(ctx, filename, name, shop, cost):
    """
    Добавить новый товар.
    """
    if os.path.exists(filename):
        products = load_products(filename)
    else:
        products = []

    products = add_product(products, name, shop, cost)
    save_products(filename, products)


@main.command()
@click.pass_context
@click.argument('filename', type=click.Path(exists=True))
def list(ctx, filename):
    """
    Отобразить список товаров.
    """
    if os.path.exists(filename):
        products = load_products(filename)
        product_list(products)


@main.command()
@click.pass_context
@click.argument('filename', type=click.Path(exists=True))
@click.option('--shop', prompt='Введите название магазина')
def select(ctx, filename, shop):
    """
    Выбрать товары из магазина.
    """
    if os.path.exists(filename):
        products = load_products(filename)
        selected = select_products(products, shop)
        product_list(selected)


if __name__ == '__main__':
    main()
