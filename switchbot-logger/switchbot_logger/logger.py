import mysql.connector
from mysql.connector import errorcode

class DBHandler(object):
    def __init__(
        self,
        host: str,
        port: int,
        database: str,
        user: str,
        password: str,
        table: str,
    ) -> None:
        self.host = host
        self.port = port
        self.database = database
        self.password = password
        self.user = user
        self.table = table

        self.check_connect()

    def connect(self) -> None:
        self.cnx = mysql.connector.connect(
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.database,
        )

    def close(self) -> None:
        self.cnx.close()

    def check_connect(self) -> None:
        try:
            self.connect()
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        # else:
        #     self.close_connect()

    def create_table(self, table: str = None) -> None:
        if table is None:
            table = self.table
        cursor = self.cnx.cursor()
        cursor.execute(
            f"CREATE TABLE IF NOT EXISTS {table} ("
            "`SensorType` varchar(16) not null,"
            "`Temperature` float not null,"
            "`Humidity` int not null,"
            "`BatteryVoltage` int not null,"
            "`Datetime` datetime not null"
            ")"
        )

    def drop_table(self, table: str) -> None:
        cursor = self.cnx.cursor()
        cursor.execute(f"DROP TABLE IF EXISTS {table};")

    def insert(self, operation: str, data: dict):
        cursor = self.cnx.cursor()
        cursor.execute(operation, data)
        self.cnx.commit()
