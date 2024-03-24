from contextlib import contextmanager


@contextmanager
def handle_db_exception(db):
    try:
        yield
        db.commit()
    except Exception as e:
        print(e)
        db.rollback()
