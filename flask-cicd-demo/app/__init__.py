from flask import Flask
app = Flask(__name__)
from app import routes
from database import setup_db
setup_db.main()
