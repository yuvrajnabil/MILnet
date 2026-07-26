import streamlit as st
import pandas as pd
from database import init_db
from components.styles import inject_css
from services.activity_service import list_activities
from services.social_media_service import list_social_posts
from components.cards import activity_card
from components.charts import social_platform_chart
from utils import show_image

init_db()
inject_css()

st.title("Current Activities")
activities = list_activities()
social_posts = list_social_posts()

featured = next((a for a in activities if a.is_featured and a.status == "Ongoing"), None)
st.subheader("Current Featured Activity")
if featured:
    activity_card(featured)
else:
    st.info("No ongoing featured activity.")

activity_tab, social_tab = st.tabs(["Programme Activities", "Social Media Activities"])

with activity_tab:
    status_filter = st.radio(
        "Filter activities",
        ["All", "Upcoming", "Ongoing", "Completed"],
        horizontal=True
    )
    selected = activities if status_filter == "All" else [
        a for a in activities if a.status == status_filter
    ]

    if not selected:
        st.info("No activities match this filter.")

    for activity in selected:
        activity_card(activity)
        if activity.gallery_images:
            gallery_columns = st.columns(min(3, len(activity.gallery_images)))
            for col, image in zip(gallery_columns, activity.gallery_images):
                with col:
                    show_image(image.image_path, image.caption)
        if activity.video_link:
            st.video(activity.video_link)

with social_tab:
    platforms = sorted({p.platform for p in social_posts})
    categories = sorted({p.activity_category for p in social_posts if p.activity_category})

    f1, f2 = st.columns(2)
    with f1:
        platform_filter = st.multiselect("Platform", platforms)
    with f2:
        category_filter = st.multiselect("Category", categories)

    filtered = [
        p for p in social_posts
        if (not platform_filter or p.platform in platform_filter)
        and (not category_filter or p.activity_category in category_filter)
    ]

    rows = [{
        "Platform": p.platform,
        "Title": p.post_title,
        "Date": p.publication_date,
        "Reactions": p.reactions,
        "Shares": p.shares,
        "Comments": p.comments,
        "Views": p.views,
        "Engagement": p.reactions + p.shares + p.comments,
        "Category": p.activity_category,
    } for p in filtered]

    df = pd.DataFrame(rows)

    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("Total posts", len(filtered))
    m2.metric("Total reach", int(df["Views"].sum()) if not df.empty else 0)
    m3.metric("Engagement", int(df["Engagement"].sum()) if not df.empty else 0)
    m4.metric("Videos", sum(p.platform == "YouTube" for p in filtered))
    m5.metric("Campaigns", len({p.campaign_hashtag for p in filtered if p.campaign_hashtag}))

    if not df.empty:
        st.plotly_chart(
            social_platform_chart(df),
            use_container_width=True,
            key="activities_social_chart"
        )
        st.dataframe(df, use_container_width=True)

    for post in filtered:
        with st.container(border=True):
            show_image(post.thumbnail_image)
            st.subheader(f"{post.platform}: {post.post_title}")
            st.write(post.description or "")
            st.caption(f"{post.publication_date or ''} · {post.campaign_hashtag or ''}")
            if post.original_post_link:
                st.link_button("Open original post", post.original_post_link)
