from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from database import get_session
from models import RealityWallPost, VisitorVote

def list_posts(published_only=True):
    with get_session() as db:
        q = db.query(RealityWallPost).order_by(RealityWallPost.publication_date.desc(), RealityWallPost.id.desc())
        if published_only:
            q = q.filter(RealityWallPost.is_published.is_(True))
        items = q.all()
        for item in items:
            _ = list(item.votes)
            db.expunge(item)
        return items

def get_post(post_id):
    with get_session() as db:
        item = db.get(RealityWallPost, post_id)
        if item:
            _ = list(item.votes)
            db.expunge(item)
        return item

def cast_vote(post_id, vote, session_token):
    if vote not in {"Real", "Fake", "Not sure"}:
        return False, "Invalid vote."
    with get_session() as db:
        db.add(VisitorVote(post_id=post_id, vote=vote, session_token=session_token))
        try:
            db.commit()
            return True, "Your vote has been recorded."
        except IntegrityError:
            db.rollback()
            return False, "You already voted on this item in this session."

def total_votes():
    with get_session() as db:
        return db.query(func.count(VisitorVote.id)).scalar() or 0
