import os
from app import creat_app, db
from app.models import Product, Product_sub
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

app = creat_app('default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, Product=Product, Product_sub=Product_sub)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command("db", MigrateCommand)

if __name__ == '__main__':
    manager.run()
