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

# Database Section ==============================##
app.config.from_object(ConnectDB)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

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
# ====================== END - APPS CONFIGURATION ======================


# ========================= DATABASE CONFIGURATION =========================
from .database import db_admin
# from .database import db_auth
# from .database import db_item
# from .database import db_item
# ====================== END - DATABASE CONFIGURATION ======================


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
# from .routes.models import admin

# Register
# app.register_blueprint()
# End Blueprint Section ==========================##
# ====================== END - ROUTE CONFIGURATION ======================