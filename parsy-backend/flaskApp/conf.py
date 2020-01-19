import os

class OfflineConfiguration:
    SQLALCHEMY_DATABASE_URI = f'mysql://{os.environ.get(parsyLocalUser)}:{os.environ.get(parsyLocalPassword)}@localhost/myAssist'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

'''class OnlineConfiguration:
    SQLALCHEMY_DATABASE_URI = f'mysql://{os.environ.get(parsyProdUser)}:{os.environ.get(parsyProdPassword)}@{os.environ.get(parsyProdServer)}/parsy'
    SQLALCHEMY_TRACK_MODIFICATIONS = False'''


class OnlineConfiguration:
    SQLALCHEMY_DATABASE_URI = f'mysql://{os.environ.get(parsyDevUser)}:{os.environ.get(parsyDevPassword)}@{os.environ.get(parsyDevServer)}/{os.environ.get(parsyDevDb)}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
