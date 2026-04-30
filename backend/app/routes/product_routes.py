from flask import Blueprint
from app.controllers import product_controller

product_bp = Blueprint('products', __name__)

product_bp.route('/', methods=['GET'])(product_controller.get_all)
product_bp.route('/<int:product_id>', methods=['GET'])(product_controller.get_one)
product_bp.route('/', methods=['POST'])(product_controller.create)
product_bp.route('/<int:product_id>', methods=['PUT'])(product_controller.update)
product_bp.route('/<int:product_id>', methods=['DELETE'])(product_controller.delete)
