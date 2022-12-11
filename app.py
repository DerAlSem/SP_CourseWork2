from flask import Flask

from main.views import main_bp
from api.views import api_bp
from bookmarks.views import bookmarks_bp

app = Flask(__name__)

app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024
app.register_blueprint(main_bp)
app.register_blueprint(api_bp)
app.register_blueprint(bookmarks_bp)

app.run()