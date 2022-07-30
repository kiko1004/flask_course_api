from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
from models import *
from flask_migrate import Migrate
from db import db
from decouple import config
from schemas import *
from resources import *

app = Flask(__name__)
db_user = config('DB_USER')
db_password = config("DB_PASSWORD")
database = config("DATABASE")
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_password}@localhost:5432/{database}'
db.init_app(app)
migrate = Migrate(app, db)
app.app_context().push()
api = Api(app)
api.add_resource(SignUp, "/register")
api.add_resource(Login, "/login")
api.add_resource(Recommendation, "/recommendation")
api.add_resource(BalanceSheet, "/balancesheet")
api.add_resource(Analysis, '/analysis')
api.add_resource(PaymentProcessor, '/upgrade')

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)





