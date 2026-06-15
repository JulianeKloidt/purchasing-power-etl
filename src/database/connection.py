import psycopg


class DatabaseConnection:
    def __init__(
        self,
        dbname: str,
        user: str,
        #password: str,
        host: str = "localhost",
        port: int = 5432,
    ):
        self.dbname = dbname
        self.user = user
        #self.password = password
        self.host = host
        self.port = port

    def connect(self):
        return psycopg.connect(
            dbname=self.dbname,
            user=self.user,
            #password=self.password,
            host=self.host,
            port=self.port,
        )