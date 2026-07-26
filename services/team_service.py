from database import get_session
from models import TeamMember

def list_team(published_only=True):
    with get_session() as db:
        q = db.query(TeamMember).order_by(TeamMember.slot_number)
        if published_only:
            q = q.filter(TeamMember.is_published.is_(True))
        items = q.all()
        for item in items:
            db.expunge(item)
        return items
