from app import app
from data import db_session

if __name__ == '__main__':
    db_session.global_init('database.db')
    from waitress import serve
    serve(app, host="0.0.0.0", port=80)
