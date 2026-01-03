import sys
import os

# Ajoute le dossier parent au chemin de recherche de Python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from api.database.session import engine
from api.database.models import Base

def init_db():
    Base.metadata.create_all(bind=engine)
    print("SQLite database initialized")

if __name__ == "__main__":
    init_db()
