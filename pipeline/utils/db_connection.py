import psycopg2
from abc import ABC, abstractmethod

__all__=['DataBasePostgreSQLConnection']
#Абстрактный класс для КМ
class DataBaseConnection(ABC):
    @abstractmethod
    def __enter__(self):
        pass
    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

class DataBasePostgreSQLConnection(DataBaseConnection):
    #
    def __init__(self, settings_param):
        self.db_host = settings_param.db_host
        self.db_port = settings_param.db_port
        self.db_user = settings_param.db_user
        self.db_password = settings_param.db_password
        self.db_name = settings_param.db_name
        self.connection = None
        self.cursor = None

    def __enter__(self):
        self.connection = psycopg2.connect(
            host=self.db_host,
            port=self.db_port,
            user=self.db_user,
            password=self.db_password,
            database=self.db_name
        )
        print('Successfully connected to Database')

        self.cursor = self.connection.cursor()
        return  self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.connection.commit()
        else:
            print('Error something wrong with connection')
            self.connection.rollback()
        self.cursor.close()
        self.connection.close()

