"""
Database initialization script
Run this to create initial database tables
"""
from app.db.session import Base, engine
# Import all models here when you create them


def init_db():
    """Initialize database tables"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")


if __name__ == "__main__":
    init_db()
