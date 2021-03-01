from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os


engine = create_engine(os.environ["DATABASE_URL"], convert_unicode=True)
db = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()
Base.query = db.query_property()


def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    Base.metadata.create_all(bind=engine)

    # now = datetime.now()
    # db.add(Submit(now - timedelta(days=7), now.date() - timedelta(days=7), 10))
    # db.add(Submit(now - timedelta(days=6), now.date() - timedelta(days=6), 12))
    # db.commit()
