import mysql.connector
import os
import json


class SingletonMeta(type):

    _instances = {}

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Singleton(metaclass=SingletonMeta):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.args = args
        self.kwargs = kwargs
        self.conn = mysql.connector.connect(
            **self.kwargs)
        self.cursor = self.conn.cursor()

    def show_db(self, sql):
        try:
            self.cursor.execute(sql)
        except :
            self.conn.rollback()
        print(self.cursor.fetchall())
        self.conn.close()

    def insert_db(self, sql):
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except :
            self.conn.rollback()
        self.conn.close()








