from flask import Flask
from flask_apscheduler import APScheduler
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object('config.ProductionConfig')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app.modules.sql_provider import SQLInitializer
sql_provider = SQLInitializer()(db)

scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

store = { 'time_for_rk1': 60, 'time_for_rk2': 60, 'interval': 1, 'groups': list() }

from app.view_controllers import init_controllers
init_controllers(app)