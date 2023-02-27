from flask import Flask
from config import Config
from ad_tools import ad_tools

app = Flask(__name__)
app.config.from_object(Config)

from app import routes