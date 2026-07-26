from database import get_session
from models import SocialMediaPost

def list_social_posts(published_only=True):
    with get_session() as db:
        q = db.query(SocialMediaPost).order_by(SocialMediaPost.publication_date.desc())
        if published_only:
            q = q.filter(SocialMediaPost.is_published.is_(True))
        items = q.all()
        for item in items:
            db.expunge(item)
        return items
