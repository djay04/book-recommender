import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from app.database import Base, engine
from app.models import Users, Books, Ratings



try:
    Base.metadata.create_all(engine)
    print("Success! Created all Tables")
except Exception as e:
    print(f'Error: Could not create all tables {e}')
