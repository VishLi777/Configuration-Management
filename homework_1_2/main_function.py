#Написать на выбранном вами языке программирования (предпочтителен Питон) программу,
#которая принимает в качестве #входных данных имя пакета, а возвращает граф его зависимостей в 
#виде текста на языке Graphviz. На выбор: для npm или для pip. 
#Пользоваться самими этими менеджерами пакетов запрещено.

#Главное, чтобы программа работала даже с неустановленными пакетами и без явного вызова pip/npm.

#https://repl.it/repls/TreasuredPleasedArguments#main.py

import json
import requests
from graphviz import Digraph



#1.get_url() - функция, которая возвращает url
#name_of site переменная в которую помещается название сайта
def get_url(name_of_pack):
    name_of_site = 'https://pypi.org/pypi/'
    url= name_of_site + name_of_pack + '/json'
    return url

#2.get_dependencies() - функция, которая возвращает зависимости, 
#конструкция try catch позволяет избежать исключений в виде None 
#и т.д., либо если пользователь неправильно ввёл данные
#парсится json пакета, создаётся arr куда будут помещаться 
#зависимости и вызывается рекурсия, пока зависимости не закончатся


def get_dependencies(name_of_pack):
    try:
        arr = []
        cont = requests.get(get_url(name_of_pack))
        json_pack = json.loads(cont.text)
        if not json_pack:
          return
        for pack in json_pack['info']['requires_dist']:
          if pack.find("extra") == -1:
              temp_arr = pack.split(' ')
              arr.append(temp_arr[0])
        for pack in arr:
            print_pack(name_of_pack, pack)
        try:
            for pack in arr:
                get_dependencies(pack)
        except TypeError: pass
        except Exception as e:
          return (e)
    except TypeError:
        return

#3.print_pack() - функция, которая выводит зависимости в таком виде, 
#чтобы можно было сразу использовать полученные зависимости для 
#построения строк графа (graphviz)
def print_pack(name_of_pack, pack):
    print('  ' + name_of_pack + ' -> ' + pack + ';') 

#4print_digraph_G() - функция, которая выводит функцию для построения графа на graphviz
def print_digraph_G(name_of_pack):
    print('Graph dependencies')
    print('digraph G {')
    get_dependencies(name_of_pack)
    print('}')
    
#5.main()-главная функция, с помощью которой осуществляется запуск программы, 
#в результате выводится граф зависимостей(Graph dependencies)
def main_function():
    name_of_pack = input()
    print_digraph_G(name_of_pack)

main_function()
