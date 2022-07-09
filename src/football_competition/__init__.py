from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)
migrate.init_app(app, db, compare_type=True)

#BluePrints
# from .routes.course_bp import course_bp
# from .routes.competition_bp import class_bp
# from .routes.enrollment_bp import enrollment_bp
from .routes.api_bp import api_bp
app.register_blueprint(api_bp, url_prefix='/api')

from .routes.ui_bp import ui_bp
app.register_blueprint(ui_bp, url_prefix='/')

# app.register_blueprint(lesson_bp, url_prefix='/lessons')

