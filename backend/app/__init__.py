from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    from app.models import product, supplier, product_supplier, purchase_order, purchase_order_line, inventory, stock_movement

    from app.routes.product_routes import product_bp
    app.register_blueprint(product_bp, url_prefix='/api/products')
    CORS(app)

    return app
