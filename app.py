import logging
from logging.handlers import SysLogHandler
from flask import Flask
from models import db, init_db
from routes import user_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configure logging to send logs to Logstash
syslog_handler = SysLogHandler(address=('logstash', 5000))
syslog_handler.setLevel(logging.INFO)
app.logger.addHandler(syslog_handler)
app.logger.setLevel(logging.INFO)

# Initialize the database
db.init_app(app)
init_db(app)

# Register the user blueprint
app.register_blueprint(user_bp, url_prefix='/user')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
