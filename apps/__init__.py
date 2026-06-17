# flask library
from flask import Flask, Blueprint, render_template, url_for
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import os

# app library
from .configure import config
from .configure.configDB import ConnectDB

# ========================= APPS CONFIGURATION =========================
# Apps Section ==============================##
app = Flask(__name__)
app.config['PRODUCT_ENVIRONMENT'] = config.PRODUCT_ENVIRONMENT
app.config['BASE_URL'] = config.BASE_URL
app.config['JWT_ACCESS_TOKE_EXPIRES'] = config.JWT_ACCESS_TOKEN_EXPIRED
app.config['SECRET_KEY'] = 'posbegkel_secret_key'

# Database Section ==============================##
app.config.from_object(ConnectDB)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# ========================= DATABASE CONFIGURATION =========================
from .database import db_admins
from .database import db_customer
from .database import db_categories
from .database import db_suppliers
from .database import db_items
from .database import db_purchases
from .database import db_purchase_details
from .database import db_sales
from .database import db_sale_details
# ====================== END - DATABASE CONFIGURATION ======================

# JWT Section ==============================##
jwt = JWTManager(app)

# Folder Section ==============================##
# Base ------------------------###
app.config['PROFILE_IMAGES'] = config.STATIC_FOLDER_PATH + "images/profiles"
app.config['ITEM_IMAGES'] = config.STATIC_FOLDER_PATH + "images/items"

# Auto Created Set ------------------------###
list_folder = [
    app.config['PROFILE_IMAGES'],
    app.config['ITEM_IMAGES'],
]
for x in list_folder:
    if os.path.exists(x) == False:
        os.makedirs(x)
# End Folder Section ==========================##
# ====================== END - APPS CONFIGURATION =======================

# ========================= ROUTE CONFIGURATION =========================
# Route Base Section ==============================##
@app.route("/")
@app.route("/index")
def index():
    return render_template(
        template_name_or_list='pages/index.html'
    )
# End Route Base Section ==========================##

# Blueprint Section ==============================##
# Import
from .routes.controllers.signin import auth
from .routes.controllers.dashboard import dashboard
from .routes.controllers.category import category
from .routes.controllers.customer import customer
from .routes.controllers.supplier import supplier
from .routes.controllers.item import item
from .routes.controllers.purchase import purchase
from .routes.controllers.sales import sales
from .routes.controllers.report import report

# Register
app.register_blueprint(auth)
app.register_blueprint(dashboard)
app.register_blueprint(category)
app.register_blueprint(customer)
app.register_blueprint(supplier)
app.register_blueprint(item)
app.register_blueprint(purchase)
app.register_blueprint(sales)
app.register_blueprint(report)
# End Blueprint Section ==========================##
# ====================== END - ROUTE CONFIGURATION ======================