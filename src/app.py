from db import db, User, Data, Category
from flask import Flask, request
from configparser import ConfigParser
import json
import sqlalchemy
import os
import dao
import threading
import time

app = Flask(__name__)

###
###     Connect To Cloud SQL
###

db_config = {
    "pool_size": 5,
    "max_overflow": 2,
    "pool_timeout": 30,  # 30 seconds
    "pool_recycle": 1800,  # 30 minutes
}

configParser = ConfigParser() 
configParser.read(os.environ.get("APP_HOME") + '/vars.config')

#Load Connect And Login Values

db_user = configParser.get("DBVARS", 'user')
db_pass = configParser.get("DBVARS", 'pass')
db_name = configParser.get("DBVARS", 'name')
db_host = configParser.get("DBVARS", 'host')
db_port = configParser.getint("DBVARS", 'port')

#API Variables
pexels_key = configParser.get("APIKEY", 'pexels_key')
quotes_key = configParser.get("APIKEY", 'quotes_key')
quotes_host = configParser.get("APIKEY", 'quotes_host')

#Initiate Connection

pool = sqlalchemy.create_engine(
    # Equivalent URL:
    # mysql+pymysql://<db_user>:<db_pass>@<db_host>:<db_port>/<db_name>
    sqlalchemy.engine.url.URL(
        drivername="mysql+pymysql",
        username=db_user,  # e.g. "my-database-user"
        password=db_pass,  # e.g. "my-database-password"
        host=db_host,  # e.g. "127.0.0.1"
        port=db_port,  # e.g. 3306
        database=db_name,  # e.g. "my-database-name"
    ),
    **db_config
)

app.config["SQLALCHEMY_DATABASE_URI"]= f"mysql+pymysql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]= True

#Create Databases

db.init_app(app)
with app.app_context():
    db.create_all()

###
###     Global Methods
###

def success_response(data, code=200):
    return json.dumps({"success": True, "data": data}), code

def failure_response(message, code=404):
    return json.dumps({"success": False, "error": message}), code

def init_category(name):
    with app.app_context():
        if Category().query.filter(Category.name==name).first() is None:
            new_category = Category(category=name)
            db.session.add(new_category)
            db.session.commit()

def init_data(dat, ind):
    with app.app_context():
        c = Category().query.filter(Category.name==dat.get('category')).first().id
        new_data = Data(category=c, 
            photo=dat.get('photo'), 
            photographer=dat.get('photographer'))

        if Data.query.filter_by(id=ind).first() is None:
            db.session.add(new_data)
        else:
            row = Data.query.filter_by(id=ind).first()
            row.category=c, 
            row.photo=dat.get('photo'), 
            row.photographer=dat.get('photographer')
        
        db.session.commit()

categories = ["pets","food","outdoors","sports","fashion"]

for i in categories:
    init_category(name=i)

data = dao.retrive_data(categories, pexels_key)
j = 1
for dat in data:
   init_data(dat, j)
   j = j + 1

def extract_token(request):
    body = json.loads(request.data)
    auth_header = body.get('authorization')
    if auth_header is None:
        return False, None, failure_response("Missing auth header")
    bearer_token = auth_header.replace("Bearer ","").strip()
    if bearer_token is None or not bearer_token:
        return False, None, failure_response("Invalid auth header")
    return True, bearer_token, ""

def verify_session(request):
    success, session_token, error = extract_token(request)
    if not success:
        return False, error
    user = User.query.filter_by(session_token=session_token).first()
    if not user or not user.verify_session_token(session_token):
        return False, failure_response("Invalid session token")
    return True, None

###
###     ROUTES
###

@app.route("/api/register/", methods=["POST"])
def register():
    body = json.loads(request.data)
    name = body.get("name")
    password = body.get("password")
    email = body.get("email")
    if name is None:
        return failure_response("No name provided", 400)
    if password is None:
        return failure_response("No password provided", 400)
    if email is None:
        return failure_response("No email provided", 400)
    user = User.query.filter_by(email=email).first()
    if user is not None:
        return failure_response("User already exists")

    new_user = User(
        name=name,
        password=password,
        email=email
    )

    db.session.add(new_user)
    db.session.commit()
    return success_response(new_user.session(), 201)

@app.route("/api/login/", methods=["POST"])
def login():
    body = json.loads(request.data)
    password = body.get("password")
    email = body.get("email")
    if password is None:
        return failure_response("No password provided", 400)
    if email is None:
        return failure_response("No email provided", 400)
    user = User.query.filter(User.email==email).first()
    success = user is not None and user.verify_password(password)
    if not success:
        return failure_response("No email or password")
    return success_response(user.session(), 201)

@app.route("/api/update_session/", methods=["POST"])
def update_session():
    success, update_token, error = extract_token(request)
    if not success:
        return error
    user = User.query.filter(User.update_token==update_token).first()
    if user is None:
        return failure_response("Invalid update token")
    user.renew_session()
    db.session.commit()
    return success_response(user.session(), 201)
    


@app.route("/api/categories/", methods=["GET"])
def get_categories():
    return success_response([c.serialize() for c in Category.query.all()])

#Yet to Be Implemented
@app.route("/api/data/", methods=["POST"])
def get_data_by_category():
    verify, error = verify_session(request)
    print(verify)
    if not verify:
        return error

    body = json.loads(request.data)
    cat = body.get("category")
    category = Category.query.filter_by(name=cat).first()
    if category is None:
        return failure_response("No category")
    #####
    return success_response([x.serialize() for x in Data.query.filter_by(category=category.id)])


#Yet To Be Implemented
@app.route("/api/data/<int:user_id>/", methods=["POST"])
def get_data_for_user(user_id):
    verify, error = verify_session(request)
    if not verify:
        return error

    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("No user")
    categories = user.categories
    data=[]
    for i in categories:
        data+=[x.serialize() for x in Data.query.filter_by(category=i.id)]
    return success_response(data)



@app.route("/api/<int:user_id>/category/", methods=["POST"])
def assign_category(user_id):
    verify, error = verify_session(request)
    if not verify:
        return error

    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("User not found")
    body=json.loads(request.data)
    name=body.get("category")
    if name is None:
        return failure_response("No category name")
    category = Category().query.filter(Category.name==name).first()
    if category is None:
        return failure_response("Invalid category", 400)
    user.categories.append(category)
    db.session.commit()
    return success_response(user.serialize())


@app.route("/api/<int:user_id>/category/", methods=["DELETE"])
def remove_category(user_id):
    verify, error = verify_session(request)
    if not verify:
        return error

    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("User not found")
    body=json.loads(request.data)
    name=body.get("category")
    if name is None:
        return failure_response("No category name")
    category = Category().query.filter(Category.name==name).first()
    if category not in user.categories:
        return failure_response("User does not have this category")
    
    user.categories.remove(category)
    db.session.commit()
    return success_response(user.serialize())

@app.route("/api/quote/", methods=["POST"])
def get_quote():
    verify, error = verify_session(request)

    if not verify:
        return error

    body = json.loads(request.data)
    category = body.get('category')

    if category is None:
        return failure_response("No Category Specified", 400)

    quote = dao.get_quote(category, quotes_key, quotes_host)
    return success_response(quote)

def load_data():
    while True:
        time.sleep(3600)
        dat = dao.retrive_data(categories, pexels_key)
        j = 1
        for dat in data:
           init_data(dat, j)
           j = j + 1

if __name__ == "__main__":
    thread = threading.Thread(target=load_data, daemon=True)
    thread.start()

    app.run(host='127.0.0.1', port=8080)
