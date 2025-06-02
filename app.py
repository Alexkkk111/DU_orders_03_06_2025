from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ulgx2qc8whowxk5fbgdp:RdEsOfAYMFhevhlBbBRFJx325hEXHK@bwuyhatiodiebom8kxav-postgresql.services.clever-cloud.com:50013/bwuyhatiodiebom8kxav'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from customers import Customer
from orders import Order

@app.route('/customers')
def list_customers():
    customers = Customer.query.all()
    customers_dict = [customer.dict() for customer in customers]
    return jsonify(customers_dict)

@app.route('/orders')
def list_orders():
    orders = Order.query.all()
    orders_dict = [order.dict() for order in orders]
    return jsonify(orders_dict)

@app.route('/customers/<customer_id>/orders')
def list_orders_by_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if not customer:
        return jsonify({'error': 'Customer not found'}), 404
    orders = [order.dict() for order in customer.orders]
    return jsonify(orders)

@app.route('/customers/<customer_id>/orders', methods=['POST'])
def add_order_to_customer(customer_id):
    entry = request.json
    order = Order()
    order.customer_id = customer_id
    order.product_name = entry['product_name']
    order.quantity = entry['quantity']
    db.session.add(order)
    db.session.commit()
    return jsonify(order.dict())

@app.route('/orders/<order_id>', methods=['PUT'])
def edit_order(order_id):
    entry = request.json
    order = Order.query.get(order_id)
    order.product_name = entry['product_name']
    order.order_date = entry['order_date']
    order.quantity = entry['quantity']
    db.session.commit()
    return jsonify(order.dict())

@app.route('/orders/<order_id>', methods=['DELETE'])
def delete_order(order_id):
    order = Order.query.get(order_id)
    if not order:
        return jsonify({'error': 'Order not found'}), 404
    db.session.delete(order)
    db.session.commit()
    return jsonify({'message': 'Order deleted successfully'})


if __name__ == '__main__':
    app.run()