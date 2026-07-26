import streamlit as st
from database import init_db
from components.styles import inject_css
init_db()
inject_css()

import pandas as pd
from datetime import date
from sqlalchemy import func
from auth import require_admin, logout, change_password
from database import get_session
from models import (
    RealityWallPost, VisitorVote, WeeklyArchive, Activity, TeamMember,
    SocialMediaPost, Resource, NewsSubmission, ContactMessage, WebsiteSetting
)
from services.upload_service import save_uploaded_image

require_admin()
st.title("Admin Dashboard")
st.caption(f"Signed in as {st.session_state.admin_username}")
if st.button("Logout", key="dashboard_logout"):
    logout(); st.switch_page("pages/7_Admin_Login.py")

with get_session() as db:
    counts = {
        "Reality Wall posts": db.query(RealityWallPost).count(),
        "Votes": db.query(VisitorVote).count(),
        "Weekly archives": db.query(WeeklyArchive).count(),
        "Activities": db.query(Activity).count(),
        "Team members": db.query(TeamMember).count(),
        "Social posts": db.query(SocialMediaPost).count(),
        "Resources": db.query(Resource).count(),
        "Submissions": db.query(NewsSubmission).count(),
        "Messages": db.query(ContactMessage).count(),
    }
cols = st.columns(3)
for idx, (label, value) in enumerate(counts.items()):
    cols[idx % 3].metric(label, value)

sections = st.tabs([
    "Reality Wall","Archives","Activities","Team","Social Media",
    "Resources","Submissions","Messages","Website Settings","Security"
])

with sections[0]:
    st.subheader("Add Reality Wall post")
    with st.form("add_wall_post"):
        title=st.text_input("Title", key="rw_title")
        short=st.text_area("Short description", key="rw_short")
        full=st.text_area("Full explanation", key="rw_full")
        original=st.text_input("Original source", key="rw_original")
        fact=st.text_input("Fact-check source", key="rw_fact")
        pubdate=st.date_input("Publication date", value=date.today(), key="rw_date")
        week=st.number_input("Week number", min_value=1, value=1, key="rw_week")
        category=st.selectbox("Category", ["Real","Fake","Misleading","Manipulated","Unverified"], key="rw_cat")
        status=st.text_input("Verification status", value="Fact-checked", key="rw_status")
        image=st.file_uploader("Image", type=["png","jpg","jpeg","webp"], key="rw_img")
        published=st.checkbox("Published", value=True, key="rw_pub")
        save=st.form_submit_button("Add post")
        if save:
            if not title.strip(): st.error("Title is required.")
            else:
                try:
                    path=save_uploaded_image(image,"reality_wall") if image else None
                    with get_session() as db:
                        db.add(RealityWallPost(title=title.strip(), short_description=short, full_explanation=full,
                            original_source=original, fact_check_source=fact, publication_date=pubdate,
                            week_number=int(week), category=category, verification_status=status,
                            image_path=path, is_published=published))
                        db.commit()
                    st.success("Post added."); st.rerun()
                except Exception as exc: st.error(str(exc))
    with get_session() as db:
        rows=db.query(RealityWallPost).order_by(RealityWallPost.id.desc()).all()
        data=[{"ID":x.id,"Title":x.title,"Category":x.category,"Status":x.verification_status,"Week":x.week_number,"Published":x.is_published} for x in rows]
    st.data_editor(pd.DataFrame(data), disabled=True, use_container_width=True, key="rw_table")
    ids=[r["ID"] for r in data]
    if ids:
        selected=st.selectbox("Select post to edit/delete", ids, key="rw_select")
        with get_session() as db:
            item=db.get(RealityWallPost, selected)
            default_title=item.title; default_status=item.verification_status; default_pub=item.is_published
        with st.form("edit_wall_post"):
            new_title=st.text_input("Edit title", value=default_title)
            new_status=st.text_input("Edit verification status", value=default_status)
            new_pub=st.checkbox("Published", value=default_pub)
            replacement=st.file_uploader("Replace image", type=["png","jpg","jpeg","webp"], key="rw_replace")
            update=st.form_submit_button("Update selected post")
            if update:
                try:
                    with get_session() as db:
                        item=db.get(RealityWallPost, selected)
                        item.title=new_title.strip(); item.verification_status=new_status; item.is_published=new_pub
                        if replacement: item.image_path=save_uploaded_image(replacement,"reality_wall")
                        db.commit()
                    st.success("Updated."); st.rerun()
                except Exception as exc: st.error(str(exc))
        confirm=st.checkbox("Confirm deletion of selected Reality Wall post", key="rw_delete_confirm")
        if st.button("Delete selected post", disabled=not confirm, key="rw_delete"):
            with get_session() as db:
                item=db.get(RealityWallPost, selected); db.delete(item); db.commit()
            st.success("Deleted."); st.rerun()

with sections[1]:
    with st.form("archive_form"):
        number=st.number_input("Week number", min_value=1, value=4)
        title=st.text_input("Week title")
        start=st.date_input("Start date", value=date.today(), key="arc_start")
        end=st.date_input("End date", value=date.today(), key="arc_end")
        summary=st.text_area("Weekly summary")
        pub=st.checkbox("Published", value=True, key="arc_pub")
        if st.form_submit_button("Add archive"):
            try:
                with get_session() as db:
                    db.add(WeeklyArchive(week_number=int(number),week_title=title or f"Week {number}",
                        start_date=start,end_date=end,weekly_summary=summary,is_published=pub)); db.commit()
                st.success("Archive added."); st.rerun()
            except Exception as exc: st.error(f"Could not add archive: {exc}")
    with get_session() as db:
        arcs=db.query(WeeklyArchive).order_by(WeeklyArchive.week_number).all()
    st.data_editor(pd.DataFrame([{"ID":a.id,"Week":a.week_number,"Title":a.week_title,"Published":a.is_published} for a in arcs]), disabled=True, key="arc_table")
    if arcs:
        aid=st.selectbox("Select archive", [a.id for a in arcs])
        with get_session() as db: a=db.get(WeeklyArchive,aid); atitle=a.week_title; apub=a.is_published
        with st.form("edit_archive"):
            nt=st.text_input("Archive title",value=atitle); np=st.checkbox("Published",value=apub)
            if st.form_submit_button("Update archive"):
                with get_session() as db: a=db.get(WeeklyArchive,aid); a.week_title=nt; a.is_published=np; db.commit()
                st.success("Updated."); st.rerun()
        c=st.checkbox("Confirm archive deletion",key="arc_del_c")
        if st.button("Delete archive",disabled=not c):
            with get_session() as db: a=db.get(WeeklyArchive,aid); db.delete(a); db.commit()
            st.rerun()

with sections[2]:
    with st.form("activity_form"):
        title=st.text_input("Activity title"); adate=st.date_input("Date",value=date.today(),key="act_date")
        location=st.text_input("Location"); short=st.text_area("Short description"); full=st.text_area("Full description")
        status=st.selectbox("Status",["Upcoming","Ongoing","Completed"]); video=st.text_input("Video link")
        featured=st.checkbox("Current featured activity"); image=st.file_uploader("Cover image",type=["png","jpg","jpeg","webp"],key="act_img")
        pub=st.checkbox("Published",value=True,key="act_pub")
        if st.form_submit_button("Add activity"):
            try:
                path=save_uploaded_image(image,"activities") if image else None
                with get_session() as db:
                    db.add(Activity(title=title,activity_date=adate,location=location,short_description=short,
                        full_description=full,status=status,video_link=video,is_featured=featured,cover_image=path,is_published=pub)); db.commit()
                st.success("Activity added."); st.rerun()
            except Exception as exc: st.error(str(exc))
    with get_session() as db: acts=db.query(Activity).all()
    st.data_editor(pd.DataFrame([{"ID":a.id,"Title":a.title,"Status":a.status,"Featured":a.is_featured,"Published":a.is_published} for a in acts]),disabled=True,key="act_table")

with sections[3]:
    st.info("Exactly 10 editable slots are maintained.")
    with get_session() as db: members=db.query(TeamMember).order_by(TeamMember.slot_number).all()
    slot=st.selectbox("Select slot",[m.slot_number for m in members])
    with get_session() as db:
        m=db.query(TeamMember).filter_by(slot_number=slot).first()
        values=(m.full_name,m.role or "",m.designation or "",m.institution or "",m.biography or "",m.email or "",m.linkedin or "",m.facebook or "",m.website or "",m.contribution or "",m.is_published)
    with st.form("edit_team"):
        name=st.text_input("Full name",value=values[0]); role=st.text_input("Role",value=values[1])
        des=st.text_input("Designation",value=values[2]); inst=st.text_input("Institution",value=values[3])
        bio=st.text_area("Biography",value=values[4]); email=st.text_input("Email",value=values[5])
        linkedin=st.text_input("LinkedIn",value=values[6]); facebook=st.text_input("Facebook",value=values[7])
        website=st.text_input("Website",value=values[8]); contribution=st.text_input("Area of contribution",value=values[9])
        photo=st.file_uploader("Replace profile photograph",type=["png","jpg","jpeg","webp"],key="team_photo")
        pub=st.checkbox("Published",value=values[10])
        if st.form_submit_button("Update team profile"):
            try:
                with get_session() as db:
                    m=db.query(TeamMember).filter_by(slot_number=slot).first()
                    m.full_name=name;m.role=role;m.designation=des;m.institution=inst;m.biography=bio;m.email=email
                    m.linkedin=linkedin;m.facebook=facebook;m.website=website;m.contribution=contribution;m.is_published=pub
                    if photo:m.photo_path=save_uploaded_image(photo,"team")
                    db.commit()
                st.success("Team profile updated."); st.rerun()
            except Exception as exc: st.error(str(exc))

with sections[4]:
    with st.form("social_form"):
        platform=st.selectbox("Platform",["Facebook","Instagram","YouTube","LinkedIn","Other"])
        title=st.text_input("Post title"); description=st.text_area("Description")
        pdate=st.date_input("Publication date",value=date.today(),key="soc_date")
        link=st.text_input("Original post link"); hashtag=st.text_input("Campaign hashtag")
        reactions=st.number_input("Reactions",min_value=0); shares=st.number_input("Shares",min_value=0)
        comments=st.number_input("Comments",min_value=0); views=st.number_input("Views",min_value=0)
        category=st.text_input("Activity category"); thumb=st.file_uploader("Thumbnail",type=["png","jpg","jpeg","webp"],key="soc_img")
        pub=st.checkbox("Published",value=True,key="soc_pub")
        if st.form_submit_button("Add social post"):
            try:
                path=save_uploaded_image(thumb,"social_media") if thumb else None
                with get_session() as db:
                    db.add(SocialMediaPost(platform=platform,post_title=title,description=description,publication_date=pdate,
                        original_post_link=link,campaign_hashtag=hashtag,reactions=int(reactions),shares=int(shares),
                        comments=int(comments),views=int(views),activity_category=category,thumbnail_image=path,is_published=pub));db.commit()
                st.success("Social post added.");st.rerun()
            except Exception as exc: st.error(str(exc))
    with get_session() as db: social=db.query(SocialMediaPost).all()
    st.data_editor(pd.DataFrame([{"ID":x.id,"Platform":x.platform,"Title":x.post_title,"Published":x.is_published} for x in social]),disabled=True,key="soc_table")

with sections[5]:
    with st.form("resource_form"):
        title=st.text_input("Resource title"); desc=st.text_area("Description")
        rtype=st.selectbox("Type",["PDF","Checklist","Poster","Infographic","Video","External link"])
        topic=st.text_input("Topic"); link=st.text_input("External link")
        file=st.file_uploader("Optional image resource",type=["png","jpg","jpeg","webp"],key="res_file")
        pub=st.checkbox("Published",value=True,key="res_pub")
        if st.form_submit_button("Add resource"):
            try:
                path=save_uploaded_image(file,"resources") if file else None
                with get_session() as db:
                    db.add(Resource(title=title,description=desc,resource_type=rtype,topic=topic,file_path=path,external_link=link,is_published=pub));db.commit()
                st.success("Resource added.");st.rerun()
            except Exception as exc:st.error(str(exc))
    with get_session() as db: resources=db.query(Resource).all()
    st.data_editor(pd.DataFrame([{"ID":r.id,"Title":r.title,"Type":r.resource_type,"Published":r.is_published} for r in resources]),disabled=True,key="res_table")

with sections[6]:
    statuses=["Pending Review","Verified Real","Verified Fake","Misleading","Manipulated","Rejected"]
    with get_session() as db: subs=db.query(NewsSubmission).order_by(NewsSubmission.created_at.desc()).all()
    st.data_editor(pd.DataFrame([{"ID":s.id,"Title":s.news_title,"Submitter":s.submitter_name,"Status":s.review_status} for s in subs]),disabled=True,key="sub_table")
    if subs:
        sid=st.selectbox("Select submission",[s.id for s in subs])
        with get_session() as db: s=db.get(NewsSubmission,sid); st.write(s.news_description); st.write(s.reason_for_suspicion); current=s.review_status
        new=st.selectbox("Review status",statuses,index=statuses.index(current) if current in statuses else 0)
        if st.button("Update submission status"):
            with get_session() as db:s=db.get(NewsSubmission,sid);s.review_status=new;db.commit()
            st.success("Status updated.");st.rerun()

with sections[7]:
    with get_session() as db: msgs=db.query(ContactMessage).order_by(ContactMessage.created_at.desc()).all()
    st.data_editor(pd.DataFrame([{"ID":m.id,"Name":m.name,"Subject":m.subject,"Read":m.is_read,"Received":m.created_at} for m in msgs]),disabled=True,key="msg_table")
    if msgs:
        mid=st.selectbox("Select message",[m.id for m in msgs])
        with get_session() as db:m=db.get(ContactMessage,mid);st.write(f"From: {m.name} <{m.email}>");st.write(m.message)
        if st.button("Mark as read"):
            with get_session() as db:m=db.get(ContactMessage,mid);m.is_read=True;db.commit()
            st.rerun()
        conf=st.checkbox("Confirm message deletion")
        if st.button("Delete message",disabled=not conf):
            with get_session() as db:m=db.get(ContactMessage,mid);db.delete(m);db.commit()
            st.rerun()

with sections[8]:
    with get_session() as db: s=db.query(WebsiteSetting).first()
    with st.form("settings_form"):
        name=st.text_input("Website name",value=s.website_name or ""); slogan=st.text_input("Slogan",value=s.slogan or "")
        intro=st.text_area("Introduction",value=s.introduction or ""); email=st.text_input("Contact email",value=s.contact_email or "")
        phone=st.text_input("Phone number",value=s.phone_number or ""); address=st.text_input("Address",value=s.address or "")
        facebook=st.text_input("Facebook link",value=s.facebook_link or ""); instagram=st.text_input("Instagram link",value=s.instagram_link or "")
        youtube=st.text_input("YouTube link",value=s.youtube_link or ""); linkedin=st.text_input("LinkedIn link",value=s.linkedin_link or "")
        logo=st.file_uploader("Replace logo",type=["png","jpg","jpeg","webp"],key="site_logo")
        hero=st.file_uploader("Replace hero image",type=["png","jpg","jpeg","webp"],key="site_hero")
        if st.form_submit_button("Save website settings"):
            try:
                with get_session() as db:
                    s=db.query(WebsiteSetting).first();s.website_name=name;s.slogan=slogan;s.introduction=intro;s.contact_email=email
                    s.phone_number=phone;s.address=address;s.facebook_link=facebook;s.instagram_link=instagram;s.youtube_link=youtube;s.linkedin_link=linkedin
                    if logo:s.logo_path=save_uploaded_image(logo,"website")
                    if hero:s.hero_image_path=save_uploaded_image(hero,"website")
                    db.commit()
                st.success("Settings saved.");st.rerun()
            except Exception as exc:st.error(str(exc))

with sections[9]:
    with st.form("password_form"):
        current=st.text_input("Current password",type="password")
        new=st.text_input("New password",type="password")
        confirm=st.text_input("Confirm new password",type="password")
        if st.form_submit_button("Change password"):
            if new != confirm: st.error("New passwords do not match.")
            else:
                ok,msg=change_password(st.session_state.admin_username,current,new)
                st.success(msg) if ok else st.error(msg)
