import os
import datetime
from dotenv import load_dotenv

# Read .env file
load_dotenv()

# Environment Configuration
PRODUCT_ENVIRONMENT = os.getenv("PRODUCT_ENVIRONMENT")
BASE_URL = os.getenv("BASE_URL")

# App Port Configuration
PORT = os.getenv("PORT")

# Database Configuration
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST")

# JWT Configuration
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ACCESS_TOKEN_EXPIRED = datetime.timedelta(hours=3)

# Folder Configuration
STATIC_FOLDER_PATH = os.path.abspath(os.path.join(__file__, "../../static")) + "/"