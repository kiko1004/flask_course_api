from resources import *
from config import create_app
from psycopg2.errorcodes import UNIQUE_VIOLATION
from werkzeug.exceptions import BadRequest, InternalServerError

app = create_app()

@app.before_first_request
def init_request():
    db.init_app(app)
    db.create_all()


if __name__ == "__main__":
    app.run()






