from flask import Flask,request,jsonify,json
from flask_restx import Api,Resource
from flask_sqlalchemy import SQLAlchemy,session
from flask_migrate import Migrate
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash,check_password_hash
from flask_jwt_extended import create_access_token,create_refresh_token,JWTManager,jwt_required,get_jwt_identity

app = Flask(__name__)
api = Api(app)
jwt = JWTManager(app)

app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:hashi@localhost/Ecommerce practice'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY']="hashim this is secret"

db = SQLAlchemy()
db.init_app(app)

migrate = Migrate()
migrate.init_app(app,db)

#model


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username =db.Column(db.String(255), nullable = False,unique=True)
    email =db.Column(db.String(255), nullable = False,unique=True)
    password =db.Column(db.String(255), nullable = False,unique=True)
    phno =db.Column(db.BigInteger, nullable = False)
    is_admin = db.Column(db.Boolean, default =False)
    order = db.relationship('Order',backref='oredred',lazy = True)
    payment = db.relationship('Payment',backref='payment',lazy = True)
    
class Category(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    cat_name = db.Column(db.String(255), nullable = False)
    product = db.relationship('Product',backref='product',lazy=True)
    order = db.relationship('Order',backref='oredred_type',lazy = True)


class Product(db.Model):
    id =db.Column(db.Integer, primary_key = True)
    name =db.Column(db.String(255), nullable = False)
    desc =db.Column(db.String(255), nullable = False)
    prize =db.Column(db.Integer)
    quantity = db.Column(db.Integer, default = 1)
    item = db.Column(db.Integer, default=10,)
    category_id =db.Column(db.Integer, db.ForeignKey('category.id'))
    order = db.relationship('Order',backref='oredred_to',lazy = True)
    
    


# Intermediate table for the many-to-many relationship
class Order(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    total_prize = db.Column(db.Integer )
    oredred_customer = db.Column(db.Integer, db.ForeignKey('customer.id'))
    ordered_category = db.Column(db.Integer, db.ForeignKey('category.id'))
    ordered_product = db.Column(db.Integer, db.ForeignKey('product.id'))
    pay = db.relationship('Payment',backref='payed_by',lazy=True) 


class Payment(db.Model):
    id = db.Column(db.Integer, primary_key =True)
    total_cost = db.Column(db.Integer )
    address = db.Column(db.String(255), nullable = False)
    payment_date = db.Column(db.DateTime, default = datetime.utcnow)
    is_payed = db.Column(db.Boolean, default = False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    

@api.route('/customer')
class Customer_detail(Resource):
    def post(self):
        # import pdb; pdb.set_trace()
        username = request.json['username']
        email = request.json['email']
        phno = request.json['phno']
        password = request.json['password']
        hashed_password = generate_password_hash(password,method='sh256')
        customers = Customer(username=usernam,email = email,phno = phno, password = hashed_password)
        db.session.add(customers)
        db.session.commit()
        return jsonify({"message":"customer added successfully"})
    def get(self):
        customers = Customer.query.all()
        output = []
        for customer in customers:
            output.append({"customer_id":customer.id,"username":customer.username,"email":customer.email,"password":customer.password,"phno":customer.phno,"is_admin":customer.is_admin})
        return jsonify({"customers":output})
        
@api.route('/customer/<int:id>')
class Customer_Modify(Resource):
    @jwt_required()
    def get(self,id):
        # Perform operations based on the user's identity
        username = get_jwt_identity()
        customer = Customer.query.filter_by(id = id).first()
        if customer:
            admin = Customer.query.filter_by(username=username, is_admin= True).first()
            if customer.username == username or admin:
                return jsonify({"customer_id":customer.id,"customer_name":customer.username,"customer_email":customer.email,"customer_password":customer.password,"customer_phno":customer.phno,"is_admin":customer.is_admin})
            else:
                return jsonify({"message":"not authorized user "})
        return jsonify({"message":f"customer with id number {id} is not availbale"})

    @jwt_required()
    def put(self,id):
        username = get_jwt_identity()
        admin = Customer.query.filter_by(username=username, is_admin= True).first()
        if admin:
            customer = Customer.query.filter_by(id = id).first()
            if customer:
                customer.username = request.json['username']
                customer.email = request.json['email']
                customer.phno = request.json['phno']
                hashed_password = generate_password_hash(request.json['password'],method='sha256')
                customer.password = hashed_password
                db.session.commit()
                return jsonify({"message":"updated all detail successfully"})
            else:
                return jsonify({"message":f"customer with id number {id} is not availbale"})
        else:
            return jsonify({"message":"not authorized user "})

    @jwt_required()
    def delete(self,id):
        username = get_jwt_identity()
        admin = Customer.query.filter_by(username=username, is_admin= True).first()
        if admin:
            customer = Customer.query.filter_by(id = id).first()
            if customer:
                db.session.delete(customer)
                db.session.commit()
                return jsonify({"message":" customer deleted successfully"})
            else:
                return jsonify({"message":f"customer with id number {id} is not availbale"})
        else:
            return jsonify({"message":"not authorized user "})
        
        
@api.route('/customer_update/<int:id>')
class Promote(Resource):
    @jwt_required()
    def put(self,id):
        username = get_jwt_identity()
        admin = Customer.query.filter_by(username=username, is_admin= True).first()
        if admin:
            customer = Customer.query.filter_by(id = id).first()
            if customer:
                customer.is_admin = True
                db.session.commit()
                return jsonify({"message":f"Mr.{customer.username} is Promoted as Admin"})
            else:
                return jsonify({"message":f"customer with id number {id} is not availbale"})
        else:
            return jsonify({"message":"not authorized user "})
        

@api.route('/login')
class Login(Resource):
    def post(self):
        # import pdb; pdb.set_trace()
        name = request.json['username']
        password =request.json['password']
        user = Customer.query.filter_by(username = name).first()
        if user:
            hashed_password = user.password
            if check_password_hash(hashed_password,password):
                customer = Customer.query.filter_by(username = name, password = hashed_password).first()
                if customer:
                    exp_date = timedelta(hours=1)
                    access_token = create_access_token(identity=name)
                    refresh_token = create_refresh_token(identity=name,expires_delta=exp_date)
                    return jsonify({"access_token":access_token,"refresh_token":refresh_token})
                else:
                    return jsonify({"message":"No such user"})
            else:
                return jsonify({"message":"password does not match"})
        else:
            return jsonify({"message":f"username {name} not found"})

    
@api.route('/category')
class Categories(Resource):
    def get(self):
        categories = Category.query.all()
        out = []
        for category in categories:
            out.append({"category_id":category.id,"category":category.cat_name})
            
        return {"categories":out}
    
    @jwt_required()
    def post(self):
        username = get_jwt_identity()
        admin = Customer.query.filter_by(username = username,is_admin = True).first()
        name = request.json['name']
        if admin:
            category = Category(cat_name=name)
            db.session.add(category)
            db.session.commit()
            return jsonify({"message":"added new category successfully"})
        else:
            return jsonify({"message":"not authorized user "})
        
@api.route('/category/<int:id>')
class Del_Categories(Resource):
    @jwt_required()
    def delete(self,id):
        username = get_jwt_identity()
        admin = Customer.query.filter_by(username = username,is_admin = True).first()
        if admin:
            category = Category.query.filter_by(id = id).first()
            if category:
                db.session.delete(category)
                db.session.commit()
                return jsonify({"message":"deleted category successfully"})
            else:
                return jsonify({"message":"No such category"})
                
        else:
            return jsonify({"message":"not authorized user "})
        
        
@api.route('/product')
class Products(Resource):
    def get(self):
        products = Product.query.all()
        out = []
        for product in products:
            out.append({"name":product.name,"desc":product.desc,"prize":product.prize,"quantity":product.quantity,"items":product.item})
        return {"categories":out}
    
    @jwt_required()
    def post(self):
        username = get_jwt_identity()
        admin = Customer.query.filter_by(username = username,is_admin = True).first()
        if admin:
            name = request.json['name']
            desc = request.json['desc']
            prize = request.json['prize']
            category_name = request.json['category_name']
            cat_id = Category.query.filter_by(cat_name = category_name).first().id
            product = Product(name = name,desc = desc, prize = prize,category_id =cat_id )
            db.session.add(product)
            db.session.commit()
            return jsonify(({"message":"added new product"}))
        else:
            return jsonify({"message":"not authorized user "})


@api.route('/product/<int:id>')
class Del_Put_Products(Resource):
    @jwt_required()
    def delete(self,id):
        username = get_jwt_identity()
        admin = Customer.query.filter_by(username = username,is_admin = True).first()
        if admin:
            product = Product.query.filter_by(id = id).first()
            if product:
                db.session.delete(product)
                db.session.commit()
                return jsonify({"message":"deleted product successfully"})
            else:
                return jsonify({"message":"No such product"})
                
        else:
            return jsonify({"message":"not authorized user "})

    @jwt_required()
    def put(self,id):
        username = get_jwt_identity()
        admin = Customer.query.filter_by(username=username, is_admin= True).first()
        if admin:
            product = Product.query.filter_by(id = id).first()
            if product:
                product.name = request.json['name']
                product.desc = request.json['desc']
                product.prize = request.json['prize']
                product.quantity = request.json['quantity']
                product.item = request.json['items']
                # here we passing category name  but assigning  id 
                category_name = request.json['category_name']
                # cat_id is a variabble
                cat_id = Category.query.filter_by(cat_name = category_name).first().id
                product.category_id = cat_id
                print( cat_id )
                print(product.category_id)
                db.session.commit()
                return jsonify({"message":"product is updated successfully"})
            return jsonify({"message":"no such product"})
        return jsonify({"message":"not authorized user"})
    
    
@api.route('/order/<int:customer_id>/<int:category_id>/<int:product_id>')
class Oredring(Resource):
    @jwt_required()
    def post(self,customer_id,category_id,product_id):
        username = get_jwt_identity()
        customer = Customer.query.filter_by(username = username).first()
        if customer.id == customer_id:
            product = Product.query.filter_by(id = product_id,category_id= category_id).first()
            if product:
                order = Order(total_prize=product.prize*product.quantity ,oredred_customer = customer_id,ordered_category = product.category_id,ordered_product = product.id)
                db.session.add(order)
                db.session.commit()
                return jsonify({"message":" successfully added to cart "})
            return jsonify({"message":"choose the valid category or valid product"})
        else:
            return jsonify({"message":"not authorized user"})

@api.route('/order_details')        
class Order_Details(Resource):
    @jwt_required()     
    def get(self):
        username = get_jwt_identity()
        customer = Customer.query.filter_by(username = username).first()
        if customer:
            order_deatils = Order.query.filter_by(oredred_customer = customer.id).all()
            if order_deatils:
                order_collection = []
                for order_detail in order_deatils:
                    order_collection.append({"Category":order_detail.oredred_type.cat_name,
                                             "Name":order_detail.oredred_to.name,
                                             "Details":order_detail.oredred_to.desc,
                                             "Prize":order_detail.oredred_to.prize,
                                             "Quantity":order_detail.oredred_to.quantity,
                                             "Total Prize":order_detail.total_prize})
                return jsonify({customer.username:order_collection})
            
            return jsonify({"message":f"No order took placed by {customer.username}"})   

        return jsonify({"message":"not authorized user"})
    
# @api.route('/payment')
# class Paying(Resource):
#     @jwt_required()
#     def post(self):
#         username = get_jwt_identity()
#         customer = Customer.query.filter_by(username = username).first()
#         if customer:
#             orders = Order.query.filter_by(oredred_customer = customer.id)
            
#             payment =Payment(address = address,total_cost = )
            
    
    
if __name__ == "__main__":
    app.run(debug=True)