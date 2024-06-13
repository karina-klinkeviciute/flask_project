from flask_migrate import Migrate

from app.app import app
from app.models import db

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    migrate = Migrate(app, db)
    app.run()
