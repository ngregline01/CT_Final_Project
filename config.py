class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:Siassaynatt%4008@localhost:3306/mechanics_shop' #add the db name later
    DEBUG = True #updates the file for you so you don't have to rerun every single time    
    CACHE_TYPE = 'SimpleCache' #initializing the cache time in your config folder
    CACHE_DEFAULT_TIMEOUT = 300 #the amount of seconds the cache can hold the data

class TestingConfig:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///testing.db'
    DEBUG = True
    CACHE_TYPE = 'SimpleCache'

class ProductionConfig:
    pass