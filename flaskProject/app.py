from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models.models import *
from controllers.invoiceController import invoiceController
from controllers.studentController import studentController
from controllers.portalController import portalController
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password@localhost/Invoices'

db.init_app(app)
migrate = Migrate(app, db)

app.register_blueprint(invoiceController)
app.register_blueprint(studentController)
app.register_blueprint(portalController)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run(port=5000)
