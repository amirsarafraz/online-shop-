from flask import Flask, jsonify , request
import sqlite3
from flask_cors import CORS, cross_origin
import io
from datetime import datetime
from fileinput import filename 

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# Connect to the database
def get_db_connection():
    conn = sqlite3.connect('Online-shop.db')
    conn.row_factory = sqlite3.Row
    return conn

# back test
@app.route('/',methods=['GET'])
def test():
    return "ok"

# users crud function
def get_all_users():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM Users')
    customers = cur.fetchall()
    final_customers = []
    for customer in customers:
        final_customers.append({
            "user_id": customer[0],
            "username": customer[1],
            "password_hash": customer[2],
            "email": customer[3],
            "phone_number": customer[4],
            "registration_date": customer[5],
            "role": customer[6],
            "default_shipping_address": customer[7],
        })
    conn.close()
    return final_customers

def get_users(users_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM Users WHERE user_id = ?', (users_id,))
    User = cur.fetchone()
    final_users = {
           "user_id": User[0],
            "username": User[1],
            "password_hash": User[2],
            "email": User[3],
            "phone_number": User[4],
            "registration_date": User[5],
            "role": User[6],
            "default_shipping_address": User[7]
        }
    conn.close()
    return final_users
def create_user(username, password_hash,email,phone_number, role,default_shipping_address):
    conn = get_db_connection()
    cur = conn.cursor()
    registration_date = datetime.today().strftime('%Y-%m-%d')
    cur.execute('INSERT INTO Users (username, password_hash,email,phone_number,registration_date,role,default_shipping_address) VALUES (?, ?, ?, ? , ?, ?, ?)', (username, password_hash,email,phone_number,registration_date, role,default_shipping_address))
    conn.commit()
    customer_id = cur.lastrowid
    conn.close()
    return customer_id
def update_user(users_id,username, password_hash,email,phone_number, role,default_shipping_address):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('UPDATE Users SET username = ?, password_hash = ?, email = ?, phone_number = ?, registration_date = ?, role = ? , default_shipping_address = ? WHERE user_id = ?', (users_id,username, password_hash,email,phone_number, role,default_shipping_address))
    conn.commit()
    conn.close()
    return get_users(id)
def delete_user(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM Users WHERE user_id = ?', (user_id,))
    conn.commit()
    conn.close()


# products
# def get_all_products():
#     conn = get_db_connection()
#     cur = conn.cursor()
#     cur.execute('SELECT * FROM Products')
#     products = cur.fetchall()
#     final_products = []
#     for product in products:
#         final_products.append({
#             "product_id": product[0],
#             "name": product[1],
#             "description": product[2],
#             "price": product[3],
#             "category_id": product[4],
#             "picture": product[5],
#         })
#     conn.close()
#     return final_products
# def get_product(product_id):
#     conn = get_db_connection()
#     cur = conn.cursor()
#     cur.execute("SELECT * FROM Products WHERE product_id = ?", (product_id,))
#     product = cur.fetchone()
#     conn.close()
#     return {
#         'product_id': product[0],
#         'name': product[1],
#         'description': product[2],
#         'price': product[3],
#         'category_id': product[4],
#         'picture': product[5]
#     }
# def create_product(name, description, price, category_id, picture):
#     conn = get_db_connection()
#     cur = conn.cursor()
#     rnd = random.randint(1,50000)
#     picture.save("./pics/"+ str(rnd) + ".jpg")
#     picture_path = "./pics/" + str(rnd) + ".jpg"
#     cur.execute('INSERT INTO Products (name, description,price,category_id,picture_path) VALUES (?, ?, ?, ? , ? )', (name, description, price, category_id,picture_path))
#     conn.commit()
#     product_id = cur.lastrowid
#     conn.close()
#     return product_id
# def update_product(id,name, description, price, category_id, picture):
    # conn = get_db_connection()
    # cur = conn.cursor()
    # cur.execute('UPDATE Products SET name = ?, description = ?, price = ?, category_id = ?, picture_path = ? WHERE product_id = ?', (name, description, price, category_id, picture,id))
    # conn.commit()
    # conn.close()
    # return get_product(id)



#category
def get_all_Categories():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM Categories')
    Categories = cur.fetchall()
    final_Categories = []
    for Categorie in Categories:
        final_Categories.append({
            "category_id": Categorie[0],
            "name": Categorie[1],
            "description": Categorie[2],
            "parent_category_id": Categorie[3],
            "created_at": Categorie[4],
        })
    conn.close()
    return final_Categories
def create_Categories(name, description, parent_category_id):
    conn = get_db_connection()
    cur = conn.cursor()
    created_at = datetime.today().strftime('%Y-%m-%d')
    cur.execute('INSERT INTO Categories (name, description,parent_category_id,created_at) VALUES (?, ?, ?, ?)', (name, description, parent_category_id, created_at))
    conn.commit()
    conn.close()
    return "ok"
def get_Categories(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM Categories WHERE category_id = ?',(id,))
    Categorie = cur.fetchone()
    conn.close()
    final_category = {
        "category_id": Categorie[0],
        "name": Categorie[1],
        "description": Categorie[2],
        "parent_category_id": Categorie[3],
        "created_at": Categorie[4],
    }
    return final_category
def delete_category(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM Categories WHERE category_id = ?', (id,))
    conn.commit()
    conn.close()
def update_category(name,description,parent_category_id,created_at,id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('UPDATE Categories SET name = ?, description = ?, parent_category_id = ?, created_at = ? WHERE category_id = ?', (name,description,parent_category_id,created_at,id))
    conn.commit()
    conn.close()
    return get_Categories(id)


# category crud routes
@app.route('/Categories', methods=['GET'])
def list_Categories():
    Categories = get_all_Categories()
    response = jsonify(Categories)
    response.headers['Access-Control-Expose-Headers'] = 'Content-Range'
    response.headers['Content-Range'] = len(Categories)
    return response
@app.route('/Category/<int:id>', methods=['GET'])
def Category(id):
    Category = get_Categories(id)
    if Category is None:
        return '', 404
    return jsonify(Category), 200
@app.route('/Categories', methods=['POST'])
def add_Categories():
    name = request.json['name']
    description = request.json['description']
    parent_category_id = request.json['parent_category_id']
    Categories_id = create_Categories(name, description, parent_category_id)
    return "ok", 201
@app.route('/Category/<int:id>', methods=['DELETE'])
def delete_category_by_id(id):
    delete_category(id)
    return jsonify({"id":id}), 200
@app.route('/Category/<int:id>', methods=['PUT'])
def update_category_by_id(id):
    name = request.json['name']
    description = request.json['description']
    parent_category_id = request.json['parent_category_id']
    created_at = request.json['created_at']
    updated = update_category(name, description, parent_category_id, created_at,id)
    return jsonify(updated), 200



# users CRUD routes
@app.route('/Users', methods=['GET'])
def list_users():
    customers = get_all_users()
    response = jsonify(customers)
    response.headers['Access-Control-Expose-Headers'] = 'Content-Range'
    response.headers['Content-Range'] = len(customers)
    return response

@app.route('/Users/<int:user_id>', methods=['GET'])
def get_customer_by_id(user_id):
    user = get_users(user_id)
    if user is None:
        return '', 404
    return jsonify(user), 200

@app.route('/Users', methods=['POST'])
def add_customer():
    username = request.json['username']
    password_hash = request.json['password_hash']
    email = request.json['email']
    phone_number = request.json['phone_number']
    role = request.json['role']
    default_shipping_address = request.json['default_shipping_address']
    user_id = create_user(username, password_hash,email,phone_number, role,default_shipping_address)
    return jsonify(get_users(user_id)), 201

@app.route('/Users/<int:user_id>', methods=['PUT'])
def update_user_by_id(user_id):
    username = request.json['username']
    password_hash = request.json['password_hash']
    email = request.json['email']
    phone_number = request.json['phone_number']
    role = request.json['role']
    default_shipping_address = request.json['default_shipping_address']
    registration_date = request.json['registration_date']
    updated = update_user(user_id,username, password_hash,email,phone_number, registration_date,role,default_shipping_address)
    return jsonify(updated), 200

@app.route('/Users/<int:user_id>', methods=['DELETE'])
def delete_user_by_id(user_id):
    delete_user(user_id)
    return jsonify({"user_id":user_id}), 200







#order crud function
def get_all_orders():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM Orders')
    orders = cur.fetchall()
    final_orders = []
    for order in orders:
        final_orders.append({
            "order_id": order[0],
            "user_id": order[1],
            "order_date": order[2].strftime('%Y-%m-%d %H:%M:%S'),
            "total_amount": order[3],
            "status": order[4],
    })
    conn.close()
    return final_orders

def create_order(user_id, order_date, total_amount, status):
    conn = get_db_connection()
    cur = conn.cursor()
    order_date_str = order_date.strftime('%Y-%m-%d %H:%M:%S')
    cur.execute('INSERT INTO Orders (customer_id, order_date, total_amount, status) VALUES (?, ?, ?, ?)', (user_id, order_date_str, total_amount, status))
    conn.commit()
    conn.close()
    return "ok"

def get_order(order_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM Orders WHERE order_id = ?', (order_id,))
    order = cur.fetchone()
    conn.close()
    if order is None:
        return None
    return {
        "order_id": order[0],
        "user_id": order[1],
        "order_date": order[2].strftime('%Y-%m-%d %H:%M:%S'),
        "total_amount": order[3],
        "status": order[4],
    }

def delete_order(order_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM Orders WHERE order_id = ?', (order_id,))
    conn.commit()
    conn.close()
    return "ok"

def update_order(order_id, customer_id, order_date, total_amount, status):
    conn = get_db_connection()
    cur = conn.cursor()
    update_stmt = "UPDATE Orders SET "
    update_params = []
    if customer_id is not None:
        update_stmt += "customer_id = ?, "
        update_params.append(customer_id)
    if order_date is not None:
        order_date_str = order_date.strftime('%Y-%m-%d %H:%M:%S')
        update_stmt += "order_date = ?, "
        update_params.append(order_date_str)        

#order crud routes
@app.route('/Orders', methods=['GET'])
def list_orders():
    orders = get_all_orders()
    response = jsonify(orders)
    response.headers['Access-Control-Expose-Headers'] = 'Content-Range'
    response.headers['Content-Range'] = len(orders)
    return response

@app.route('/Order/<int:order_id>', methods=['GET'])
def order(order_id):
    order = get_order(order_id)
    if order is None:
        return '', 404
    return jsonify(order), 200

@app.route('/Orders', methods=['POST'])
def add_order():
    user_id = request.json['customer_id']
    order_date_str = request.json['order_date']
    order_date = datetime.strptime(order_date_str, '%Y-%m-%d %H:%M:%S')
    total_amount = request.json['total_amount']
    status = request.json['status']
    order_id = create_order(user_id, order_date, total_amount, status)
    return jsonify({"order_id": order_id}), 201

@app.route('/Order/<int:order_id>', methods=['DELETE'])
def delete_order_by_id(order_id):
    delete_order(order_id)
    return jsonify({"id": order_id}), 200

@app.route('/Order/<int:order_id>', methods=['PUT'])
def update_order_by_id(order_id):
    user_id = request.json['customer_id']
    order_date_str = request.json['order_date']
    order_date = datetime.strptime(order_date_str, '%Y-%m-%d %H:%M:%S')
    total_amount = request.json['total_amount']
    status = request.json['status']
    updated_order = update_order(order_id, user_id, order_date, total_amount, status)
    return jsonify(updated_order), 200




#order-detail crud function
def get_all_orderDetail():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM OrderDetails')
    details = cur.fetchall()
    final_details = []
    for detail in details:
        final_details.append({
            "order_detail_id": detail[0],
            "order_id": detail[1],
            "product_id": detail[2],
            "quantity": detail[3],
            "unit_price": detail[4],
        })
    conn.close()
    return final_details

def get_details(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM OrderDetails WHERE order_detail_id = ?',(id,))
    detail = cur.fetchone()
    conn.close()
    final_details = {
            "order_detail_id": detail[0],
            "order_id": detail[1],
            "product_id": detail[2],
            "quantity": detail[3],
            "unit_price": detail[4],
    }
    return final_details

def create_detail(order_id, product_id,quantity,unit_price):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO OrderDetails (order_id,product_id,quantity,unit_price) VALUES (?, ?, ?,?)', (order_id,product_id,quantity,unit_price,))
    conn.commit()
    conn.close()
    return "ok"

def delete_detail(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM OrderDetails WHERE order_detail_id = ?', (id,))
    conn.commit()
    conn.close()
    
def update_detail(order_id, product_id,quantity,unit_price,id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('UPDATE OrderDetails SET order_id = ?, product_id = ?, quantity = ?, unit_price = ? WHERE order_detail_id = ?', (order_id, product_id,quantity,unit_price,id))
    conn.commit()
    conn.close()
    return get_details(id)

# order-detail routes
@app.route('/details', methods=['GET'])
def list_details():
    details = get_all_orderDetail()
    response = jsonify(details)
    response.headers['Access-Control-Expose-Headers'] = 'Content-Range'
    response.headers['Content-Range'] = len(details)
    return response

@app.route('/detail/<int:id>', methods=['GET'])
def detail(id):
    detail = get_details(id)
    if detail is None:
        return '', 404
    return jsonify(detail), 200

@app.route('/newDetail', methods=['POST'])
def add_details():
    order_id = request.json['order_id']
    product_id = request.json['product_id']
    quantity = request.json['quantity']
    unit_price = request.json['unit_price']
    detail_id = create_detail(order_id, product_id, quantity,unit_price)
    return "ok", 201

@app.route('/delDetail/<int:id>', methods=['DELETE'])
def delete_detail_by_id(id):
    delete_detail(id)
    return jsonify({"id":id}), 200

@app.route('/upDetail/<int:id>', methods=['PUT'])
def update_detail_by_id(id):
    order_id = request.json['order_id']
    product_id = request.json['product_id']
    quantity = request.json['quantity']
    unit_price = request.json['unit_price']
    updated = update_detail(order_id, product_id, quantity,unit_price,id)
    return jsonify(updated), 200
#-------------------------------------------------




# @app.route('/Products', methods=['POST'])
# def add_product():
#     name = request.json['name']
#     description = request.json['description']
#     price = request.json['price']
#     category_id = request.json['category_id']
#     picture = request.files['picture']
#     create_product(name, description, price, category_id,picture)
#     return {'Content-Type': 'multipart/format-data'}


# # product

#     data = request.get_json()
#     image = request.files['image']

#     conn = get_db_connection()
#     img_binary = io.BytesIO(image.read())

#     cursor = conn.cursor()
#     cursor.execute("INSERT INTO Products (name, description, price, category_id, picture) VALUES (?, ?, ?, ?, ?)",
#                    (data['name'], data['description'], data['price'], data['category_id'], img_binary.getvalue()))
#     conn.commit()
#     product_id = cursor.lastrowid
#     conn.close()

#     return jsonify(get_product(product_id)), 201




if __name__ == '__main__':
    app.run(debug=True)