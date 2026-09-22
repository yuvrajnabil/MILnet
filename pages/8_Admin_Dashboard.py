import streamlit as st
from database import init_db
from components.styles import inject_css

init_db()
inject_css()

import pandas as pd
from datetime import date

from auth import require_admin, logout, change_password
from database import get_session
from models import (
    RealityWallPost,
    VisitorVote,
    WeeklyArchive,
    Activity,
    TeamMember,
    SocialMediaPost,
    Resource,
    NewsSubmission,
    ContactMessage,
    WebsiteSetting,
)
from services.upload_service import save_uploaded_image


# ---------------------------------------------------------
# AUTHENTICATION
# ---------------------------------------------------------

require_admin()

st.title("Admin Dashboard")
st.caption(f"Signed in as {st.session_state.admin_username}")

if st.button("Logout", key="dashboard_logout"):
    logout()
    st.switch_page("pages/7_Admin_Login.py")


# ---------------------------------------------------------
# DASHBOARD COUNTS
# ---------------------------------------------------------

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


# ---------------------------------------------------------
# TABS
# ---------------------------------------------------------

sections = st.tabs(
    [
        "Reality Wall",
        "Archives",
        "Activities",
        "Team",
        "Social Media",
        "Resources",
        "Submissions",
        "Messages",
        "Website Settings",
        "Security",
    ]
)


# =========================================================
# 1. REALITY WALL
# =========================================================

with sections[0]:

    st.subheader("Add Reality Wall post")

    with st.form("add_wall_post"):

        title = st.text_input("Title", key="rw_title")
        short = st.text_area("Short description", key="rw_short")
        full = st.text_area("Full explanation", key="rw_full")
        original = st.text_input("Original source", key="rw_original")
        fact = st.text_input("Fact-check source", key="rw_fact")

        pubdate = st.date_input(
            "Publication date",
            value=date.today(),
            key="rw_date",
        )

        week = st.number_input(
            "Week number",
            min_value=1,
            value=1,
            key="rw_week",
        )

        category = st.selectbox(
            "Category",
            [
                "Real",
                "Fake",
                "Misleading",
                "Manipulated",
                "Unverified",
            ],
            key="rw_cat",
        )

        status = st.text_input(
            "Verification status",
            value="Fact-checked",
            key="rw_status",
        )

        image = st.file_uploader(
            "Image",
            type=["png", "jpg", "jpeg", "webp"],
            key="rw_img",
        )

        published = st.checkbox(
            "Published",
            value=True,
            key="rw_pub",
        )

        save = st.form_submit_button("Add post")

        if save:

            if not title.strip():

                st.error("Title is required.")

            else:

                try:

                    path = (
                        save_uploaded_image(
                            image,
                            "reality_wall",
                        )
                        if image
                        else None
                    )

                    with get_session() as db:

                        db.add(
                            RealityWallPost(
                                title=title.strip(),
                                short_description=short,
                                full_explanation=full,
                                original_source=original,
                                fact_check_source=fact,
                                publication_date=pubdate,
                                week_number=int(week),
                                category=category,
                                verification_status=status,
                                image_path=path,
                                is_published=published,
                            )
                        )

                        db.commit()

                    st.success("Post added.")
                    st.rerun()

                except Exception as exc:

                    st.error(f"Could not add post: {exc}")


    # Existing posts

    with get_session() as db:

        rows = (
            db.query(RealityWallPost)
            .order_by(RealityWallPost.id.desc())
            .all()
        )

        data = [
            {
                "ID": x.id,
                "Title": x.title,
                "Category": x.category,
                "Status": x.verification_status,
                "Week": x.week_number,
                "Published": x.is_published,
            }
            for x in rows
        ]

    if data:

        st.data_editor(
            pd.DataFrame(data),
            disabled=True,
            use_container_width=True,
            key="rw_table",
        )

        ids = [r["ID"] for r in data]

        selected = st.selectbox(
            "Select post to edit/delete",
            ids,
            key="rw_select",
        )

        with get_session() as db:

            item = db.get(
                RealityWallPost,
                selected,
            )

            if item:

                default_title = item.title
                default_status = item.verification_status
                default_pub = item.is_published

            else:

                default_title = ""
                default_status = ""
                default_pub = True


        with st.form("edit_wall_post"):

            new_title = st.text_input(
                "Edit title",
                value=default_title,
            )

            new_status = st.text_input(
                "Edit verification status",
                value=default_status,
            )

            new_pub = st.checkbox(
                "Published",
                value=default_pub,
            )

            replacement = st.file_uploader(
                "Replace image",
                type=["png", "jpg", "jpeg", "webp"],
                key="rw_replace",
            )

            update = st.form_submit_button(
                "Update selected post"
            )

            if update:

                try:

                    with get_session() as db:

                        item = db.get(
                            RealityWallPost,
                            selected,
                        )

                        if item:

                            item.title = new_title.strip()
                            item.verification_status = new_status
                            item.is_published = new_pub

                            if replacement:

                                item.image_path = (
                                    save_uploaded_image(
                                        replacement,
                                        "reality_wall",
                                    )
                                )

                            db.commit()

                    st.success("Updated.")
                    st.rerun()

                except Exception as exc:

                    st.error(str(exc))


        confirm = st.checkbox(
            "Confirm deletion of selected Reality Wall post",
            key="rw_delete_confirm",
        )

        if st.button(
            "Delete selected post",
            disabled=not confirm,
            key="rw_delete",
        ):

            with get_session() as db:

                item = db.get(
                    RealityWallPost,
                    selected,
                )

                if item:

                    db.delete(item)
                    db.commit()

            st.success("Deleted.")
            st.rerun()

    else:

        st.info("No Reality Wall posts have been added yet.")


# =========================================================
# 2. WEEKLY ARCHIVES
# =========================================================

with sections[1]:

    st.subheader("Weekly Archive")

    with st.form("archive_form"):

        number = st.number_input(
            "Week number",
            min_value=1,
            value=1,
        )

        title = st.text_input(
            "Week title"
        )

        start = st.date_input(
            "Start date",
            value=date.today(),
            key="arc_start",
        )

        end = st.date_input(
            "End date",
            value=date.today(),
            key="arc_end",
        )

        summary = st.text_area(
            "Weekly summary"
        )

        pub = st.checkbox(
            "Published",
            value=True,
            key="arc_pub",
        )

        if st.form_submit_button(
            "Add archive"
        ):

            try:

                with get_session() as db:

                    db.add(
                        WeeklyArchive(
                            week_number=int(number),
                            week_title=(
                                title.strip()
                                if title.strip()
                                else f"Week {number}"
                            ),
                            start_date=start,
                            end_date=end,
                            weekly_summary=summary,
                            is_published=pub,
                        )
                    )

                    db.commit()

                st.success("Archive added.")
                st.rerun()

            except Exception as exc:

                st.error(
                    f"Could not add archive: {exc}"
                )


    with get_session() as db:

        arcs = (
            db.query(WeeklyArchive)
            .order_by(WeeklyArchive.week_number)
            .all()
        )


    if arcs:

        st.data_editor(
            pd.DataFrame(
                [
                    {
                        "ID": a.id,
                        "Week": a.week_number,
                        "Title": a.week_title,
                        "Published": a.is_published,
                    }
                    for a in arcs
                ]
            ),
            disabled=True,
            key="arc_table",
        )

        aid = st.selectbox(
            "Select archive",
            [a.id for a in arcs],
            key="archive_select",
        )

        with get_session() as db:

            a = db.get(
                WeeklyArchive,
                aid,
            )

            if a:

                atitle = a.week_title
                apub = a.is_published

            else:

                atitle = ""
                apub = True


        with st.form("edit_archive"):

            nt = st.text_input(
                "Archive title",
                value=atitle,
            )

            np = st.checkbox(
                "Published",
                value=apub,
            )

            if st.form_submit_button(
                "Update archive"
            ):

                with get_session() as db:

                    a = db.get(
                        WeeklyArchive,
                        aid,
                    )

                    if a:

                        a.week_title = nt
                        a.is_published = np
                        db.commit()

                st.success("Updated.")
                st.rerun()


        c = st.checkbox(
            "Confirm archive deletion",
            key="arc_del_c",
        )

        if st.button(
            "Delete archive",
            disabled=not c,
            key="archive_delete",
        ):

            with get_session() as db:

                a = db.get(
                    WeeklyArchive,
                    aid,
                )

                if a:

                    db.delete(a)
                    db.commit()

            st.success("Deleted.")
            st.rerun()

    else:

        st.info(
            "No weekly archives have been added yet."
        )


# =========================================================
# 3. ACTIVITIES
# =========================================================

with sections[2]:

    st.subheader("Activities")

    with st.form("activity_form"):

        title = st.text_input(
            "Activity title"
        )

        adate = st.date_input(
            "Date",
            value=date.today(),
            key="act_date",
        )

        location = st.text_input(
            "Location"
        )

        short = st.text_area(
            "Short description"
        )

        full = st.text_area(
            "Full description"
        )

        status = st.selectbox(
            "Status",
            [
                "Upcoming",
                "Ongoing",
                "Completed",
            ],
        )

        video = st.text_input(
            "Video link"
        )

        featured = st.checkbox(
            "Current featured activity"
        )

        image = st.file_uploader(
            "Cover image",
            type=["png", "jpg", "jpeg", "webp"],
            key="act_img",
        )

        pub = st.checkbox(
            "Published",
            value=True,
            key="act_pub",
        )

        if st.form_submit_button(
            "Add activity"
        ):

            try:

                path = (
                    save_uploaded_image(
                        image,
                        "activities",
                    )
                    if image
                    else None
                )

                with get_session() as db:

                    db.add(
                        Activity(
                            title=title,
                            activity_date=adate,
                            location=location,
                            short_description=short,
                            full_description=full,
                            status=status,
                            video_link=video,
                            is_featured=featured,
                            cover_image=path,
                            is_published=pub,
                        )
                    )

                    db.commit()

                st.success("Activity added.")
                st.rerun()

            except Exception as exc:

                st.error(
                    f"Could not add activity: {exc}"
                )


    with get_session() as db:

        acts = (
            db.query(Activity)
            .order_by(Activity.id.desc())
            .all()
        )


    if acts:

        st.data_editor(
            pd.DataFrame(
                [
                    {
                        "ID": a.id,
                        "Title": a.title,
                        "Status": a.status,
                        "Featured": a.is_featured,
                        "Published": a.is_published,
                    }
                    for a in acts
                ]
            ),
            disabled=True,
            key="act_table",
        )

    else:

        st.info(
            "No activities have been added yet."
        )


# =========================================================
# 4. TEAM
# =========================================================

with sections[3]:

    st.subheader("Team Members")

    st.info(
        "You can add up to 10 team member slots."
    )


    with get_session() as db:

        members = (
            db.query(TeamMember)
            .order_by(TeamMember.slot_number)
            .all()
        )


    # -----------------------------------------------------
    # EMPTY DATABASE
    # -----------------------------------------------------

    if not members:

        st.warning(
            "No team members have been added yet."
        )

        with st.form(
            "create_first_team_member"
        ):

            slot = st.number_input(
                "Slot number",
                min_value=1,
                max_value=10,
                value=1,
                step=1,
            )

            name = st.text_input(
                "Full name"
            )

            role = st.text_input(
                "Role"
            )

            des = st.text_input(
                "Designation"
            )

            inst = st.text_input(
                "Institution"
            )

            bio = st.text_area(
                "Biography"
            )

            email = st.text_input(
                "Email"
            )

            linkedin = st.text_input(
                "LinkedIn"
            )

            facebook = st.text_input(
                "Facebook"
            )

            website = st.text_input(
                "Website"
            )

            contribution = st.text_input(
                "Area of contribution"
            )

            photo = st.file_uploader(
                "Profile photograph",
                type=[
                    "png",
                    "jpg",
                    "jpeg",
                    "webp",
                ],
                key="first_team_photo",
            )

            pub = st.checkbox(
                "Published",
                value=True,
            )

            submit = st.form_submit_button(
                "Add team member"
            )

            if submit:

                if not name.strip():

                    st.error(
                        "Full name is required."
                    )

                else:

                    try:

                        with get_session() as db:

                            existing = (
                                db.query(TeamMember)
                                .filter_by(
                                    slot_number=int(slot)
                                )
                                .first()
                            )

                            if existing:

                                st.error(
                                    "This slot is already in use."
                                )

                            else:

                                path = (
                                    save_uploaded_image(
                                        photo,
                                        "team",
                                    )
                                    if photo
                                    else None
                                )

                                db.add(
                                    TeamMember(
                                        slot_number=int(slot),
                                        full_name=name.strip(),
                                        role=role,
                                        designation=des,
                                        institution=inst,
                                        biography=bio,
                                        email=email,
                                        linkedin=linkedin,
                                        facebook=facebook,
                                        website=website,
                                        contribution=contribution,
                                        photo_path=path,
                                        is_published=pub,
                                    )
                                )

                                db.commit()

                                st.success(
                                    "Team member added successfully."
                                )

                                st.rerun()

                    except Exception as exc:

                        st.error(
                            f"Could not add team member: {exc}"
                        )


    # -----------------------------------------------------
    # EXISTING MEMBERS
    # -----------------------------------------------------

    else:

        st.success(
            f"{len(members)} team member(s) found."
        )

        slot = st.selectbox(
            "Select team member slot",
            [m.slot_number for m in members],
            key="team_slot",
        )


        with get_session() as db:

            m = (
                db.query(TeamMember)
                .filter_by(
                    slot_number=slot
                )
                .first()
            )


        if m is None:

            st.error(
                "Selected team member could not be found."
            )

        else:

            with st.form(
                "edit_team"
            ):

                name = st.text_input(
                    "Full name",
                    value=m.full_name or "",
                )

                role = st.text_input(
                    "Role",
                    value=m.role or "",
                )

                des = st.text_input(
                    "Designation",
                    value=m.designation or "",
                )

                inst = st.text_input(
                    "Institution",
                    value=m.institution or "",
                )

                bio = st.text_area(
                    "Biography",
                    value=m.biography or "",
                )

                email = st.text_input(
                    "Email",
                    value=m.email or "",
                )

                linkedin = st.text_input(
                    "LinkedIn",
                    value=m.linkedin or "",
                )

                facebook = st.text_input(
                    "Facebook",
                    value=m.facebook or "",
                )

                website = st.text_input(
                    "Website",
                    value=m.website or "",
                )

                contribution = st.text_input(
                    "Area of contribution",
                    value=m.contribution or "",
                )

                photo = st.file_uploader(
                    "Replace profile photograph",
                    type=[
                        "png",
                        "jpg",
                        "jpeg",
                        "webp",
                    ],
                    key="team_photo",
                )

                pub = st.checkbox(
                    "Published",
                    value=bool(m.is_published),
                )

                if st.form_submit_button(
                    "Update team profile"
                ):

                    try:

                        with get_session() as db:

                            member = (
                                db.query(TeamMember)
                                .filter_by(
                                    slot_number=slot
                                )
                                .first()
                            )

                            if member is None:

                                st.error(
                                    "Team member no longer exists."
                                )

                            else:

                                member.full_name = name.strip()
                                member.role = role
                                member.designation = des
                                member.institution = inst
                                member.biography = bio
                                member.email = email
                                member.linkedin = linkedin
                                member.facebook = facebook
                                member.website = website
                                member.contribution = contribution
                                member.is_published = pub

                                if photo:

                                    member.photo_path = (
                                        save_uploaded_image(
                                            photo,
                                            "team",
                                        )
                                    )

                                db.commit()

                                st.success(
                                    "Team profile updated."
                                )

                                st.rerun()

                    except Exception as exc:

                        st.error(
                            f"Could not update team profile: {exc}"
                        )


# =========================================================
# 5. SOCIAL MEDIA
# =========================================================

with sections[4]:

    st.subheader("Social Media Posts")

    with st.form("social_form"):

        platform = st.selectbox(
            "Platform",
            [
                "Facebook",
                "Instagram",
                "YouTube",
                "LinkedIn",
                "Other",
            ],
        )

        title = st.text_input(
            "Post title"
        )

        description = st.text_area(
            "Description"
        )

        pdate = st.date_input(
            "Publication date",
            value=date.today(),
            key="soc_date",
        )

        link = st.text_input(
            "Original post link"
        )

        hashtag = st.text_input(
            "Campaign hashtag"
        )

        reactions = st.number_input(
            "Reactions",
            min_value=0,
        )

        shares = st.number_input(
            "Shares",
            min_value=0,
        )

        comments = st.number_input(
            "Comments",
            min_value=0,
        )

        views = st.number_input(
            "Views",
            min_value=0,
        )

        category = st.text_input(
            "Activity category"
        )

        thumb = st.file_uploader(
            "Thumbnail",
            type=[
                "png",
                "jpg",
                "jpeg",
                "webp",
            ],
            key="soc_img",
        )

        pub = st.checkbox(
            "Published",
            value=True,
            key="soc_pub",
        )

        if st.form_submit_button(
            "Add social post"
        ):

            try:

                path = (
                    save_uploaded_image(
                        thumb,
                        "social_media",
                    )
                    if thumb
                    else None
                )

                with get_session() as db:

                    db.add(
                        SocialMediaPost(
                            platform=platform,
                            post_title=title,
                            description=description,
                            publication_date=pdate,
                            original_post_link=link,
                            campaign_hashtag=hashtag,
                            reactions=int(reactions),
                            shares=int(shares),
                            comments=int(comments),
                            views=int(views),
                            activity_category=category,
                            thumbnail_image=path,
                            is_published=pub,
                        )
                    )

                    db.commit()

                st.success(
                    "Social post added."
                )

                st.rerun()

            except Exception as exc:

                st.error(str(exc))


    with get_session() as db:

        social = (
            db.query(SocialMediaPost)
            .order_by(
                SocialMediaPost.id.desc()
            )
            .all()
        )


    if social:

        st.data_editor(
            pd.DataFrame(
                [
                    {
                        "ID": x.id,
                        "Platform": x.platform,
                        "Title": x.post_title,
                        "Published": x.is_published,
                    }
                    for x in social
                ]
            ),
            disabled=True,
            key="soc_table",
        )

    else:

        st.info(
            "No social media posts have been added yet."
        )


# =========================================================
# 6. RESOURCES
# =========================================================

with sections[5]:

    st.subheader("MIL Resources")

    with st.form("resource_form"):

        title = st.text_input(
            "Resource title"
        )

        desc = st.text_area(
            "Description"
        )

        rtype = st.selectbox(
            "Type",
            [
                "PDF",
                "Checklist",
                "Poster",
                "Infographic",
                "Video",
                "External link",
            ],
        )

        topic = st.text_input(
            "Topic"
        )

        link = st.text_input(
            "External link"
        )

        file = st.file_uploader(
            "Optional image resource",
            type=[
                "png",
                "jpg",
                "jpeg",
                "webp",
            ],
            key="res_file",
        )

        pub = st.checkbox(
            "Published",
            value=True,
            key="res_pub",
        )

        if st.form_submit_button(
            "Add resource"
        ):

            try:

                path = (
                    save_uploaded_image(
                        file,
                        "resources",
                    )
                    if file
                    else None
                )

                with get_session() as db:

                    db.add(
                        Resource(
                            title=title,
                            description=desc,
                            resource_type=rtype,
                            topic=topic,
                            file_path=path,
                            external_link=link,
                            is_published=pub,
                        )
                    )

                    db.commit()

                st.success(
                    "Resource added."
                )

                st.rerun()

            except Exception as exc:

                st.error(str(exc))


    with get_session() as db:

        resources = (
            db.query(Resource)
            .order_by(Resource.id.desc())
            .all()
        )


    if resources:

        st.data_editor(
            pd.DataFrame(
                [
                    {
                        "ID": r.id,
                        "Title": r.title,
                        "Type": r.resource_type,
                        "Published": r.is_published,
                    }
                    for r in resources
                ]
            ),
            disabled=True,
            key="res_table",
        )

    else:

        st.info(
            "No resources have been added yet."
        )


# =========================================================
# 7. SUBMISSIONS
# =========================================================

with sections[6]:

    st.subheader("News Submissions")

    statuses = [
        "Pending Review",
        "Verified Real",
        "Verified Fake",
        "Misleading",
        "Manipulated",
        "Rejected",
    ]

    with get_session() as db:

        subs = (
            db.query(NewsSubmission)
            .order_by(
                NewsSubmission.created_at.desc()
            )
            .all()
        )


    if subs:

        st.data_editor(
            pd.DataFrame(
                [
                    {
                        "ID": s.id,
                        "Title": s.news_title,
                        "Submitter": s.submitter_name,
                        "Status": s.review_status,
                    }
                    for s in subs
                ]
            ),
            disabled=True,
            key="sub_table",
        )

        sid = st.selectbox(
            "Select submission",
            [s.id for s in subs],
            key="submission_select",
        )

        with get_session() as db:

            submission = db.get(
                NewsSubmission,
                sid,
            )

            if submission:

                st.write(
                    submission.news_description
                )

                st.write(
                    submission.reason_for_suspicion
                )

                current = submission.review_status

            else:

                current = statuses[0]


        new = st.selectbox(
            "Review status",
            statuses,
            index=(
                statuses.index(current)
                if current in statuses
                else 0
            ),
        )

        if st.button(
            "Update submission status",
            key="update_submission",
        ):

            with get_session() as db:

                submission = db.get(
                    NewsSubmission,
                    sid,
                )

                if submission:

                    submission.review_status = new
                    db.commit()

            st.success(
                "Status updated."
            )

            st.rerun()

    else:

        st.info(
            "No news submissions yet."
        )


# =========================================================
# 8. CONTACT MESSAGES
# =========================================================

with sections[7]:

    st.subheader("Contact Messages")

    with get_session() as db:

        msgs = (
            db.query(ContactMessage)
            .order_by(
                ContactMessage.created_at.desc()
            )
            .all()
        )


    if msgs:

        st.data_editor(
            pd.DataFrame(
                [
                    {
                        "ID": m.id,
                        "Name": m.name,
                        "Subject": m.subject,
                        "Read": m.is_read,
                        "Received": m.created_at,
                    }
                    for m in msgs
                ]
            ),
            disabled=True,
            key="msg_table",
        )

        mid = st.selectbox(
            "Select message",
            [m.id for m in msgs],
            key="message_select",
        )

        with get_session() as db:

            message = db.get(
                ContactMessage,
                mid,
            )

            if message:

                st.write(
                    f"From: {message.name} <{message.email}>"
                )

                st.write(
                    message.message
                )


        if st.button(
            "Mark as read",
            key="mark_read",
        ):

            with get_session() as db:

                message = db.get(
                    ContactMessage,
                    mid,
                )

                if message:

                    message.is_read = True
                    db.commit()

            st.success(
                "Marked as read."
            )

            st.rerun()


        conf = st.checkbox(
            "Confirm message deletion",
            key="message_delete_confirm",
        )

        if st.button(
            "Delete message",
            disabled=not conf,
            key="delete_message",
        ):

            with get_session() as db:

                message = db.get(
                    ContactMessage,
                    mid,
                )

                if message:

                    db.delete(message)
                    db.commit()

            st.success(
                "Message deleted."
            )

            st.rerun()

    else:

        st.info(
            "No contact messages yet."
        )


# =========================================================
# 9. WEBSITE SETTINGS
# =========================================================

with sections[8]:

    st.subheader("Website Settings")

    with get_session() as db:

        settings = (
            db.query(WebsiteSetting)
            .first()
        )


    # -----------------------------------------------------
    # CREATE SETTINGS IF DATABASE IS EMPTY
    # -----------------------------------------------------

    if settings is None:

        st.info(
            "Website settings have not been configured yet. "
            "Fill in the form below to create them."
        )

        current_name = ""
        current_slogan = ""
        current_intro = ""
        current_email = ""
        current_phone = ""
        current_address = ""
        current_facebook = ""
        current_instagram = ""
        current_youtube = ""
        current_linkedin = ""

    else:

        current_name = settings.website_name or ""
        current_slogan = settings.slogan or ""
        current_intro = settings.introduction or ""
        current_email = settings.contact_email or ""
        current_phone = settings.phone_number or ""
        current_address = settings.address or ""
        current_facebook = settings.facebook_link or ""
        current_instagram = settings.instagram_link or ""
        current_youtube = settings.youtube_link or ""
        current_linkedin = settings.linkedin_link or ""


    with st.form(
        "settings_form"
    ):

        name = st.text_input(
            "Website name",
            value=current_name,
        )

        slogan = st.text_input(
            "Slogan",
            value=current_slogan,
        )

        intro = st.text_area(
            "Introduction",
            value=current_intro,
        )

        email = st.text_input(
            "Contact email",
            value=current_email,
        )

        phone = st.text_input(
            "Phone number",
            value=current_phone,
        )

        address = st.text_input(
            "Address",
            value=current_address,
        )

        facebook = st.text_input(
            "Facebook link",
            value=current_facebook,
        )

        instagram = st.text_input(
            "Instagram link",
            value=current_instagram,
        )

        youtube = st.text_input(
            "YouTube link",
            value=current_youtube,
        )

        linkedin = st.text_input(
            "LinkedIn link",
            value=current_linkedin,
        )

        logo = st.file_uploader(
            "Replace logo",
            type=[
                "png",
                "jpg",
                "jpeg",
                "webp",
            ],
            key="site_logo",
        )

        hero = st.file_uploader(
            "Replace hero image",
            type=[
                "png",
                "jpg",
                "jpeg",
                "webp",
            ],
            key="site_hero",
        )

        if st.form_submit_button(
            "Save website settings"
        ):

            try:

                with get_session() as db:

                    settings = (
                        db.query(
                            WebsiteSetting
                        )
                        .first()
                    )


                    # Create settings if none exist
                    if settings is None:

                        settings = WebsiteSetting()

                        db.add(settings)


                    settings.website_name = name
                    settings.slogan = slogan
                    settings.introduction = intro
                    settings.contact_email = email
                    settings.phone_number = phone
                    settings.address = address
                    settings.facebook_link = facebook
                    settings.instagram_link = instagram
                    settings.youtube_link = youtube
                    settings.linkedin_link = linkedin


                    if logo:

                        settings.logo_path = (
                            save_uploaded_image(
                                logo,
                                "website",
                            )
                        )


                    if hero:

                        settings.hero_image_path = (
                            save_uploaded_image(
                                hero,
                                "website",
                            )
                        )


                    db.commit()


                st.success(
                    "Website settings saved successfully."
                )

                st.rerun()

            except Exception as exc:

                st.error(
                    f"Could not save website settings: {exc}"
                )


# =========================================================
# 10. SECURITY
# =========================================================

with sections[9]:

    st.subheader("Change Admin Password")

    with st.form(
        "password_form"
    ):

        current = st.text_input(
            "Current password",
            type="password",
        )

        new = st.text_input(
            "New password",
            type="password",
        )

        confirm = st.text_input(
            "Confirm new password",
            type="password",
        )

        if st.form_submit_button(
            "Change password"
        ):

            if not current:

                st.error(
                    "Please enter your current password."
                )

            elif not new:

                st.error(
                    "Please enter a new password."
                )

            elif new != confirm:

                st.error(
                    "New passwords do not match."
                )

            else:

                ok, msg = change_password(
                    st.session_state.admin_username,
                    current,
                    new,
                )

                if ok:

                    st.success(msg)

                else:

                    st.error(msg)
