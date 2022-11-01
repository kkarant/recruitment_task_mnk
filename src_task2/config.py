import os


class DatabaseSettings:
    def __init__(self) -> None:
        self.database = os.getenv('DATABASE')
        self.user = os.getenv('USER_DB')
        self.password = os.getenv('PASSWORD_DB')
        self.host = os.getenv('HOST_DB')
        self.port = os.getenv('PORT_DB')


class FTPSettings:
    def __init__(self) -> None:
        self.ip = os.environ['IP']
        self.login = os.environ['LOGIN']
        self.password = os.environ['PASSWORD']
