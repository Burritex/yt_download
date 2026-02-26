from flask import Flask
from routes import app_routes
from config import Config


app = Flask(__name__, template_folder='templates', static_folder='static')
app.config.from_object(Config)
app.register_blueprint(app_routes)

if __name__ == "__main__":
   app.run(host="0.0.0.0", port=2159, debug=True)
