from Mechanic_App import create_app
from Mechanic_App.models import db

mechanics_shop = create_app('DevelopmentConfig')
with mechanics_shop.app_context():
    #db.drop_all()
    db.create_all()

mechanics_shop.run()