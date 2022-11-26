from sqlalchemy import create_engine, select
from sqlalchemy import Column, TEXT, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from uniland.utils.search import SearchEngine
from .config import DB_URI

def start() -> scoped_session:
    # Creating db engine and session
    engine = create_engine(DB_URI)
    BASE.metadata.bind = engine
    BASE.metadata.create_all(engine)
    session = scoped_session(sessionmaker(bind=engine, autoflush=False))
    
    # Indexing all submissions
    search_engine = SearchEngine()
    for sub in engine.execute('SELECT id, search_text, submission_type FROM submissions'):
        search_engine.index_record(*sub)
        
    return (session, search_engine)

BASE = declarative_base()
SESSION, search_engine = start()

print(search_engine)
print(search_engine.keywords.keys())
