from database import get_session
from models import Resource

def list_resources(published_only=True):
    with get_session() as db:
        q = db.query(Resource).order_by(Resource.created_at.desc())
        if published_only:
            q = q.filter(Resource.is_published.is_(True))
        items = q.all()
        for item in items:
            db.expunge(item)
        return items
