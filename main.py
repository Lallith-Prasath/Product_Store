from flask import Flask, redirect, render_template,request,url_for,flash
import json
from flask_sqlalchemy import SQLAlchemy
import pyodbc
from flask_mail import Mail, Message
local_server = True
app = Flask(__name__)

app.secret_key = "*&^%$#@(!)0"

# app.config.update(
#     MAIL_SERVER='smtp.gmail.com',
#     MAIL_PORT=587,
#     MAIL_USE_SSL=True,
#     MAIL_USERNAME="rlallithprasath@gmail.com"   ,
#     MAIL_PASSWORD="biam rhqc roaz ndrz")
# mail = Mail(app)
 
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://tap2023:tap2023@APINP-ELPT7H4FQ\SQLEXPRESS/crudApp?driver=SQL Server'
db = SQLAlchemy(app)
 
 
class Test(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(15))
 
class Products(db.Model):
    pid=db.Column(db.Integer,primary_key=True)
    productName=db.Column(db.String(50))
    productDescription=db.Column(db.String(100))
    rating=db.Column(db.Integer)
    stocks=db.Column(db.Integer)
    price=db.Column(db.Integer)
 
@app.route("/test/")
def test():
    try:
        # query=Test.query.all()
        # print(query)
        sql_query="Select * from test"
        with db.engine.begin() as conn:
            response=conn.exec_driver_sql(sql_query).all()
            print(response)
        return f"Database is connected"
 
    except Exception as e:
        return f"Database is not connected {e} "
 
 
@app.route("/")
def home():
    products=Products.query.all()
    return render_template("index.html",products=products)
 
# create operation
@app.route("/create",methods=['GET','POST'])
def create():
    if request.method=="POST":
        pName=request.form.get('productname')
        pDesc=request.form.get('productDesc')
        pRating=request.form.get('rating')
        pStocks=request.form.get('stocks')
        pPrice=request.form.get('price')
        # query=Products(productName=pName,productDescription=pDesc,rating=pRating,stocks=pStocks,price=pPrice)
        # db.session.add(query)
        # db.session.commit()
        sql_query=f"INSERT INTO `Products` (`productName`, `productDescription`, `rating`, `stocks`, `price`) VALUES ('{pName}', '{pDesc}', {pRating}, {pStocks}, {pPrice})"
        with db.engine.begin() as conn:
            conn.exec_driver_sql(sql_query)
            flash("Product is Added Successfully","success")
            return redirect(url_for('home'))
 
    return render_template("index.html")
 
# update operation
@app.route("/update/<int:id>",methods=['GET','POST'])
def update(id):
    product=Products.query.filter_by(pid=id).first()
    if request.method=="POST":
        pName=request.form.get('productname')
        pDesc=request.form.get('productDesc')
        pRating=request.form.get('rating')
        pStocks=request.form.get('stocks')
        pPrice=request.form.get('price')
        # query=Products(productName=pName,productDescription=pDesc,rating=pRating,stocks=pStocks,price=pPrice)
        # db.session.add(query)
        # db.session.commit()
        sql_query=f"UPDATE `products` SET `productName`='{pName}',`productDescription`='{pDesc}',`rating`={pRating},`stocks`={pStocks},`price`={pPrice} WHERE `pid`={id}"     
        with db.engine.begin() as conn:
            conn.exec_driver_sql(sql_query)
            flash("Product is Updated Successfully","primary")
            return redirect(url_for('home'))
 
    return render_template("edit.html",product=product)


@app.route('/search', methods=['POST'])
def search():
    if request.method == 'POST':
        query = request.form.get('search_query')
        #print(query)
        try:
            if query.isdigit():
                sql_query=f'SELECT * FROM `PRODUCTS` WHERE `pid` = {int(query)}'
                with db.engine.begin() as conn:
                    response = conn.exec_driver_sql(sql_query).all()
                    if len(response) == 0:
                        flash('No such product found.','info')
                    else:
                        return render_template('index.html', products = response)
            else:
                sql_query = f"SELECT * FROM Products WHERE `productName` LIKE '%{query}%'"
            #print(sql_query)
            with db.engine.begin() as conn:
                response = conn.exec_driver_sql(sql_query).all()
                if len(response) == 0:
                    flash('No such product found.','info')
                else:
                    return render_template('index.html', products = response)
        except Exception as e:
            return redirect(url_for('home'))

    return redirect(url_for('home'))
 
# delete operation
@app.route("/delete/<int:id>",methods=['GET'])
def delete(id):
    # print(id)
    query=f"DELETE FROM `products` WHERE `pid`={id}"
    with db.engine.begin() as conn:
        conn.exec_driver_sql(query)
        flash("Product Deleted Successfully","danger")
        return redirect(url_for('home'))

@app.route("/contact",methods =['POST','GET'])
def contact():
    return render_template("contact.html")
    #mail.send_message('')


app.run(debug=True)

