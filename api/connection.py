import mysql.connector


class Connection:
    def __init__(self, user: str, password: str, host: str, database: str):
        self.__user = user
        self.__password = password
        self.__host = host
        self.__database = database
        self.connector = None

    def connect(self):
        try:
            self.connector = mysql.connector.connect(
                user=self.__user,
                password=self.__password,
                host=self.__host,
                database=self.__database
            )

        except mysql.connector.Error as err:
            print("Something went wrong during connection: {}".format(err))
            exit(-1)
        except TypeError as err:
            print("Something went wrong during connection: {}".format(err))
            exit(-1)

    def close(self):
        self.connector.close()















