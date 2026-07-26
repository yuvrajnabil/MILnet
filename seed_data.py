from datetime import date, timedelta
from werkzeug.security import generate_password_hash
from database import init_db, get_session
from models import (
    AdminUser, TeamMember, Activity, WeeklyArchive, RealityWallPost,
    VisitorVote, SocialMediaPost, Resource, WebsiteSetting
)

def seed():
    init_db()
    with get_session() as db:
        if not db.query(AdminUser).first():
            db.add(AdminUser(username="admin", password_hash=generate_password_hash("admin123")))
        if not db.query(WebsiteSetting).first():
            db.add(WebsiteSetting(
                website_name="MIL Reality Check Bangladesh",
                slogan="Think Before You Believe, Verify Before You Share.",
                introduction="A national awareness and advocacy platform that helps citizens recognise misinformation, verify media, and use digital platforms responsibly.",
                contact_email="contact@milrealitycheck.org",
                phone_number="+880 1XXXXXXXXX",
                address="Dhaka, Bangladesh"
            ))
        if db.query(TeamMember).count() == 0:
            for i in range(1, 11):
                db.add(TeamMember(slot_number=i, full_name=f"Team Member {i}", role="MIL Contributor",
                    designation="Editable designation", institution="Editable institution",
                    biography="This profile can be fully edited from the Admin Dashboard.",
                    email=f"member{i}@example.org", contribution="Media and Information Literacy awareness"))
        if db.query(WeeklyArchive).count() == 0:
            archives=[]
            for i in range(1,4):
                a=WeeklyArchive(week_number=i, week_title=f"Reality Check Week {i}",
                    start_date=date.today()-timedelta(days=(4-i)*7),
                    end_date=date.today()-timedelta(days=(3-i)*7+1),
                    weekly_summary=f"Sample archive for week {i}: public verification, discussion, and learning.")
                db.add(a); archives.append(a)
            db.flush()
            post_data=[
                ("Verified public-service update","A genuine notice confirmed through official channels.","Real","Verified Real"),
                ("Viral fabricated scholarship claim","A false scholarship post used an imitation logo and unofficial form.","Fake","Verified Fake"),
                ("Old flood photograph shared as current","A real photograph was reused with a false date and location.","Misleading","Misleading context"),
            ]
            posts=[]
            for i,(title,desc,cat,status) in enumerate(post_data,1):
                p=RealityWallPost(title=title,short_description=desc,
                    full_explanation="Check publication date, primary source, image history, independent reporting, and corrections before sharing.",
                    original_source="https://example.org/original",fact_check_source="https://example.org/fact-check",
                    publication_date=date.today()-timedelta(days=4-i),week_number=i,category=cat,
                    verification_status=status,archive_id=archives[i-1].id)
                db.add(p);posts.append(p)
            db.flush()
            samples=[("Real","Fake","Real"),("Fake","Fake","Not sure"),("Real","Not sure","Real")]
            for p,votes in zip(posts,samples):
                for j,v in enumerate(votes):
                    db.add(VisitorVote(post_id=p.id,vote=v,session_token=f"seed-{p.id}-{j}"))
        if db.query(Activity).count() == 0:
            db.add_all([
                Activity(title="Reality vs Reality Wall Exhibition",activity_date=date.today(),
                    location="Dhaka",short_description="A live public verification wall and discussion activity.",
                    full_description="Visitors inspect selected media items, vote, and compare their judgement with evidence.",
                    status="Ongoing",is_featured=True),
                Activity(title="Youth Fact-checking Workshop",activity_date=date.today()+timedelta(days=14),
                    location="Sylhet",short_description="Hands-on source and image verification training.",
                    full_description="Students practise lateral reading, reverse-image verification, and responsible sharing.",
                    status="Upcoming"),
                Activity(title="MIL Week Community Dialogue",activity_date=date.today()-timedelta(days=30),
                    location="Chattogram",short_description="A completed stakeholder discussion on MIL Cities.",
                    full_description="Journalists, educators, youth, and civil society discussed local MIL priorities.",
                    status="Completed")
            ])
        if db.query(SocialMediaPost).count() == 0:
            db.add_all([
                SocialMediaPost(platform="Facebook",post_title="Verify Before You Share",description="A five-step verification carousel.",
                    publication_date=date.today(),original_post_link="https://facebook.com",campaign_hashtag="#MILRealityCheck",
                    reactions=320,shares=95,comments=28,views=5200,activity_category="Fact-checking"),
                SocialMediaPost(platform="Instagram",post_title="Spot the Red Flags",description="A youth-friendly misinformation infographic.",
                    publication_date=date.today()-timedelta(days=2),original_post_link="https://instagram.com",campaign_hashtag="#ThinkVerifyShare",
                    reactions=410,shares=80,comments=35,views=6100,activity_category="Awareness"),
                SocialMediaPost(platform="YouTube",post_title="Reality Wall Explained",description="A short activity documentary.",
                    publication_date=date.today()-timedelta(days=5),original_post_link="https://youtube.com",campaign_hashtag="#MILBangladesh",
                    reactions=220,shares=60,comments=40,views=8400,activity_category="Video"),
                SocialMediaPost(platform="LinkedIn",post_title="Building MIL Cities",description="A professional stakeholder briefing.",
                    publication_date=date.today()-timedelta(days=7),original_post_link="https://linkedin.com",campaign_hashtag="#MILCities",
                    reactions=180,shares=45,comments=22,views=3300,activity_category="Advocacy"),
            ])
        if db.query(Resource).count() == 0:
            db.add_all([
                Resource(title="Fake News Identification Checklist",description="A printable checklist for evaluating suspicious claims.",resource_type="Checklist",topic="Fake news"),
                Resource(title="Photo Verification Guide",description="Basic steps for reverse-image searching and context checking.",resource_type="PDF",topic="Image verification"),
                Resource(title="Responsible Social Media Poster",description="Pause, verify, and consider harm before posting.",resource_type="Poster",topic="Digital citizenship"),
                Resource(title="Ethical Journalism Learning Video",description="A sample external learning resource.",resource_type="Video",topic="Ethical journalism",external_link="https://www.youtube.com"),
            ])
        db.commit()
    print("Sample data is ready. Existing non-empty tables were not duplicated.")

if __name__ == "__main__":
    seed()
