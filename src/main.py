import os
from flask import Flask
from flask import jsonify
from src.api.utils.database import db, ma
from src.api.config.config import DevelopmentConfig, ProductionConfig, TestingConfig
from src.api.utils.responses import response_with
import src.api.utils.responses as resp
import logging
from src.api.routes.users import user_routes
from src.api.routes.station import station_routes
from src.api.routes.battery import battery_routes
app = Flask(__name__)

if os.environ.get('WORK_ENV') == 'PROD':
    app_config = ProductionConfig
elif os.environ.get('WORK_ENV') == 'TEST':
    app_config = TestingConfig
else:
    app_config = DevelopmentConfig

app.config.from_object(app_config)

db.init_app(app)
ma.init_app(app)
with app.app_context():
    db.create_all()

app.register_blueprint(user_routes, url_prefix='/api/users')
app.register_blueprint(station_routes, url_prefix='/api/station')
app.register_blueprint(battery_routes, url_prefix='/api/battery')

@app.after_request
def add_header(response):
    return response


@app.errorhandler(400)
def bad_request(e):
    logging.error(e)
    return response_with(resp.BAD_REQUEST_400)


@app.errorhandler(500)
def server_error(e):
    logging.error(e)
    return response_with(resp.SERVER_ERROR_500)


@app.errorhandler(404)
def not_found(e):
    logging.error(e)
    return response_with(resp.SERVER_ERROR_404)


db.init_app(app)
ma.init_app(app)

with app.app_context():
    db.create_all()

# if __name__ == '__main__':
#     app.run(port=5000, host='0.0.0.0', user_reloader=False)
