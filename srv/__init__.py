from flask import Flask
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from config import Config
import os
import logging
import smtplib
from logging.handlers import SMTPHandler,RotatingFileHandler
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
#login.refresh_view = 'auth.login'
bootstrap = Bootstrap()
moment = Moment()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)

    from srv.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from srv.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from srv.main import bp as main_bp
    app.register_blueprint(main_bp)


    if not app.debug and not app.testing:
      if app.config['MAIL_SERVER']:
          auth = None
          print("mail")
          if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
              auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
          secure = None
          if app.config['MAIL_USE_TLS']:
              secure = ()
          mail_handler = SSLSMTPHandler(
              mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
              #fromaddr='no-reply@' + app.config['MAIL_SERVER'],
              fromaddr='nicholas-r@mail.ru',
              toaddrs=app.config['ADMINS'], subject='SRV Failure',
              credentials=auth, secure=secure)
          mail_handler.setLevel(logging.ERROR)
          #mail_handler.setLevel(logging.INFO)
          app.logger.addHandler(mail_handler)
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/srv.log', maxBytes=10240,
                                       backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Srv startup')
    return  app 

class SSLSMTPHandler(SMTPHandler):
    def emit(self, record):
        """
        Emit a record.
        """
        try:
            port = self.mailport
            if not port:
                port = smtplib.SMTP_PORT
            smtp = smtplib.SMTP_SSL(self.mailhost, port)
            msg = self.format(record)
            if self.username:
                smtp.login(self.username, self.password)
            smtp.sendmail(self.fromaddr, self.toaddrs, msg)
            smtp.quit()
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)
