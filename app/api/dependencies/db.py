def get_db():
    from app.db import Session
    db = Session()
    try:
        yield db
    finally:
        db.close()
