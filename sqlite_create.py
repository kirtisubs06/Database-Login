"""
import sqlite3

connection = sqlite3.connect('business.db')
connection.execute('CREATE TABLE products (prodname, price, weight)')
#This line creates the first table, called products, which holds the name, price, and weight of the product.
connection.execute('CREATE TABLE users (name, password, email)')
#This line creates a second table, called users, which holds the name, password, and email of the user.

_______________________________________________________

import sqlite3

connection = sqlite3.connect('business.db')

connection = sqlite3.connect('business.db')
connection.execute('CREATE TABLE products (prodname, price, weight)')
#This line creates the first table, called products, which holds the name, price, and weight of the product.
connection.execute('CREATE TABLE users (name, password, email)')
#This line creates a second table, called users, which holds the name, password, and email of the user.
connection.execute('INSERT INTO products VALUES (?, ?, ?)', ['book', 7.99, 0.5])
connection.execute('INSERT INTO products VALUES (?, ?, ?)', ['drink', 2.00, 0.4])
connection.execute('INSERT INTO products VALUES (?, ?, ?)', ['car', 70000, 1875])

connection.commit()
"""

import sqlite3

connection = sqlite3.connect('business.db')
connection = sqlite3.connect('business.db')
connection.execute('CREATE TABLE products (prodname, price, weight)')
#This line creates the first table, called products, which holds the name, price, and weight of the product.
connection.execute('CREATE TABLE users (name, password, email)')
#This line creates a second table, called users, which holds the name, password, and email of the user.

cursor = connection.cursor()

product_cursor = cursor.execute('SELECT * FROM products')
product_list = product_cursor.fetchall()

for product in product_list:
    print(product)
