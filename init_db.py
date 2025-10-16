from app import db
from models import Notice

def init_db():
    db.create_all()
    # Optional sample seed
    if Notice.query.count() == 0:
        sample = Notice(
            title="Welcome to E-Notice-Board",
            content="This is a sample notice. Login to create, edit, or delete notices.",
            author="System"
        )
        db.session.add(sample)
        db.session.commit()
        print("Seeded sample notice.")
    print("Database initialized.")

if __name__ == '__main__':
    init_db()
