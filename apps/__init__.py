# flask library
from flask import Flask, render_template, url_for
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

# app library
from .configure import config
from .configure.configDB import ConnectDB


load_dotenv(
    os.path.join(os.path.dirname(__file__), ".env"),
    override=True
)

env_path = os.path.join(
    os.path.dirname(__file__),
    ".env"
)

server_key = os.getenv("MIDTRANS_SERVER_KEY")
client_key = os.getenv("MIDTRANS_CLIENT_KEY")


# ========================= APPS CONFIGURATION =========================
# Apps Section ==============================##
app = Flask(__name__)
app.config['PRODUCT_ENVIRONMENT'] = config.PRODUCT_ENVIRONMENT
app.config['BASE_URL'] = config.BASE_URL
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = config.JWT_ACCESS_TOKEN_EXPIRED
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config["JWT_COOKIE_SECURE"] = False  # True jika HTTPS
app.config["JWT_COOKIE_CSRF_PROTECT"] = False  # sementara saat development
app.config['SECRET_KEY'] = config.JWT_SECRET_KEY
app.config["JWT_SECRET_KEY"] = config.JWT_SECRET_KEY
app.config["MIDTRANS_SERVER_KEY"] = (
    os.getenv("MIDTRANS_SERVER_KEY", "").strip()
)

app.config["MIDTRANS_CLIENT_KEY"] = (
    os.getenv("MIDTRANS_CLIENT_KEY", "").strip()
)

app.config["MIDTRANS_IS_PRODUCTION"] = (
    os.getenv(
        "MIDTRANS_IS_PRODUCTION",
        "False"
    ).strip().lower() == "true"
)

server_key = app.config["MIDTRANS_SERVER_KEY"]
client_key = app.config["MIDTRANS_CLIENT_KEY"]


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
# ====================== END - APPS CONFIGURATION =======================

# ========================= DATABASE CONFIGURATION =========================
from .database import db_users
from .database import db_workshops
from .database import db_cashier
from .database import db_customers
from .database import db_vehicles
from .database import db_categories
from .database import db_suppliers
from .database import db_products
from .database import db_purchases
from .database import db_purchase_details
from .database import db_payment
from .database import db_sale_details
from .database import db_services
from .database import db_sale_service_details
from .database import db_cash_deposits
from .database import db_subscription_payment
# Database Seed
from .database import seed
with app.app_context():
    seed.seed_users()

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
from .routes.controllers.auth import auth
from .routes.controllers.workshop_management import workshop_management
from .routes.controllers.cashier_management import cashier_management
from .routes.controllers.dashboard import dashboard
from .routes.controllers.dashboard_cashier import dashboard_cashier
from .routes.controllers.dashboard_administrator import dashboard_administrator
from .routes.controllers.owner_account import owner_account
from .routes.controllers.cashier import cashier
from .routes.controllers.category import category
from .routes.controllers.customer import customer
from .routes.controllers.vehicle import vehicle
from .routes.controllers.workshop import workshop
from .routes.controllers.product import product
from .routes.controllers.supplier import supplier
from .routes.controllers.services import service
from .routes.controllers.purchase import purchase
from .routes.controllers.history_sales import history_sales
from .routes.controllers.history_purchase import history_purchase
from .routes.controllers.report_sales import report_sales
from .routes.controllers.report_purchase import report_purchase
from .routes.controllers.cash_deposit import cash_deposit
from .routes.controllers.subscription import subscription
from .routes.controllers.subscription_payment_history import subscription_payment_history

# Register
app.register_blueprint(auth)
app.register_blueprint(workshop_management)
app.register_blueprint(cashier_management)
app.register_blueprint(dashboard)
app.register_blueprint(dashboard_cashier)
app.register_blueprint(dashboard_administrator)
app.register_blueprint(owner_account)
app.register_blueprint(cashier)
app.register_blueprint(category)
app.register_blueprint(workshop)
app.register_blueprint(customer)
app.register_blueprint(vehicle)
app.register_blueprint(product)
app.register_blueprint(supplier)
app.register_blueprint(service)
app.register_blueprint(purchase)
app.register_blueprint(history_sales)
app.register_blueprint(history_purchase)
app.register_blueprint(report_sales)
app.register_blueprint(report_purchase)
app.register_blueprint(cash_deposit)
app.register_blueprint(subscription)
app.register_blueprint(subscription_payment_history)

# End Blueprint Section ==========================##
# ====================== END - ROUTE CONFIGURATION ======================