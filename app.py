from flask import Flask
from database.models import create_tables

from routes.auth_routes import auth_bp
from routes.menu_routes import menu_bp
from routes.order_routes import order_bp
from routes.payment_routes import payment_bp

app = Flask(__name__)
orders = []
create_tables()

app.register_blueprint(auth_bp)
app.register_blueprint(menu_bp)
app.register_blueprint(order_bp)
app.register_blueprint(payment_bp)

@app.route("/")
def home():
    return "Paratha Vendor Backend Running"

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5001,debug=True)