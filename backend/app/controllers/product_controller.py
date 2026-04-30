from flask import request, jsonify
from app.services import product_service

def get_all():
    products = product_service.get_all_products()
    return jsonify({
        'success': True,
        'data': [product_service.serialize_product(p) for p in products]
    })

def get_one(product_id):
    product = product_service.get_product_by_id(product_id)
    if not product:
        return jsonify({'success': False, 'message': 'Product not found'}), 404
    return jsonify({'success': True, 'data': product_service.serialize_product(product)})

def create():
    try:
        data = request.get_json()
        product = product_service.create_product(data)
        return jsonify({'success': True, 'data': product_service.serialize_product(product)}), 201
    except ValueError as e:
        return jsonify({'success': False, 'message': str(e)}), 400

def update(product_id):
    try:
        data = request.get_json()
        product = product_service.update_product(product_id, data)
        return jsonify({'success': True, 'data': product_service.serialize_product(product)})
    except LookupError as e:
        return jsonify({'success': False, 'message': str(e)}), 404
    except ValueError as e:
        return jsonify({'success': False, 'message': str(e)}), 400

def delete(product_id):
    try:
        product_service.delete_product(product_id)
        return jsonify({'success': True, 'message': 'Product deleted successfully'})
    except LookupError as e:
        return jsonify({'success': False, 'message': str(e)}), 404
    except ValueError as e:
        return jsonify({'success': False, 'message': str(e)}), 400
