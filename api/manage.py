from connection import Connection
from getpass import getpass


class Manage:
    def __init__(self, user: str, password: str, host: str, database: str):
        self.connection = Connection(user, password, host, database)
        self.available_tables = []
        self.table_name = ''
        self.choose_table()

    @classmethod
    def data_input(cls):
        __user = input("Enter username: ")
        __password = getpass("Enter password: ")
        __host = input("Enter host: ")
        __database = input("Enter database name: ")
        return cls(__user, __password, __host, __database)

    def choose_table(self):
        self.get_tables()
        self.table_name = ''
        while True:
            for table_name in self.available_tables:
                print(table_name)

            self.table_name = input("Table: ")
            if self.table_name not in self.available_tables:
                print("You need to choose one of the tables shown under \"Available Tables\"! ")
            else:
                print("You have chosen the \"{}\" table.".format(self.table_name))
                break

    def get_tables(self):
        self.connection.connect()
        cursor = self.connection.connector.cursor()
        cursor.execute("""
        SHOW TABLES;
        """)

        tables = cursor.fetchall()
        for t in tables:
            self.available_tables.append(t[0])

        self.connection.close()

    def describe(self):
        cursor = self.connection.connect()
        cursor.execute("""
        DESCRIBE {};
        """.format(self.table_name))


if __name__ == "__main__":
    overseer = Manage(
        user="artole",
        password="YGDAX3wy",
        host="localhost",
        database="typing_database"
    )

    while True:
        print('Describe table:           "d"\n'
              'Choose different table:   "ct"\n'
              'Exit:                     "e"\n')

        commands = {
            "d":  overseer.describe,
            "ct": overseer.choose_table,
            "e": exit,
        }

        command = input("Enter your command:")

        if command.lower() in commands.keys():
            commands[command]()

