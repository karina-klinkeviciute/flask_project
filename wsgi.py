from flask_migrate import Migrate

from project.app import app
from project.models import db

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    migrate = Migrate(app, db)
    app.run()
