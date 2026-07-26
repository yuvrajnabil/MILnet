from database import get_session
from models import WebsiteSetting

def get_settings():
    with get_session() as db:
        item = db.query(WebsiteSetting).first()
        if item:
            db.expunge(item)
            return item
        item = WebsiteSetting(
            website_name="MIL Reality Check Bangladesh",
            slogan="Think Before You Believe, Verify Before You Share.",
            introduction="A national awareness platform for critical thinking, fact-checking, and responsible digital citizenship."
        )
        db.add(item); db.commit(); db.refresh(item); db.expunge(item)
        return item
