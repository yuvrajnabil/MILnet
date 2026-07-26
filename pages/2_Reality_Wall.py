import streamlit as st
from database import init_db
from components.styles import inject_css
init_db()
inject_css()

from services.reality_wall_service import list_posts, cast_vote
from components.charts import vote_chart
from utils import show_image, get_or_create_session_token

st.title("Reality vs Reality Wall")
st.write("A physical and digital awareness activity where visitors inspect real, fake, misleading, manipulated, and unverified content, then share their judgement.")
with st.expander("Objectives"):
    st.write("Build verification habits, expose manipulation techniques, promote discussion, and track how public opinion changes over multiple weeks.")

st.subheader("Current Wall photograph")
st.info("Current wall photograph placeholder — replace it from the Admin Dashboard.")
st.subheader("Video")
st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
st.caption("Sample video link. Replace it with the official activity video.")

posts = list_posts()
if not posts:
    st.info("No published Reality Wall posts are available.")
for post in posts:
    with st.container(border=True):
        st.subheader(post.title)
        show_image(post.image_path)
        st.write(post.short_description or "")
        cols = st.columns(3)
        cols[0].markdown(f"**Category:** {post.category}")
        cols[1].markdown(f"**Status:** {post.verification_status}")
        cols[2].markdown(f"**Week:** {post.week_number or 'N/A'}")
        st.caption(f"Published: {post.publication_date or 'Unknown'}")
        with st.expander("Full explanation and sources"):
            st.write(post.full_explanation or "")
            st.write(f"Original source: {post.original_source or 'Not provided'}")
            st.write(f"Fact-check source: {post.fact_check_source or 'Not provided'}")
        token = get_or_create_session_token()
        voted_key = f"voted_post_{post.id}"
        if not st.session_state.get(voted_key):
            with st.form(f"vote_form_{post.id}"):
                choice = st.radio("What do you think?", ["Real","Fake","Not sure"], key=f"vote_radio_{post.id}")
                submitted = st.form_submit_button("Submit vote")
                if submitted:
                    ok, msg = cast_vote(post.id, choice, token)
                    if ok:
                        st.session_state[voted_key] = True
                        st.success(msg); st.rerun()
                    else:
                        st.warning(msg)
        else:
            st.success("You voted on this item during this session.")
        total = len(post.votes)
        real_count = sum(v.vote == "Real" for v in post.votes)
        st.progress((real_count / total) if total else 0, text=f"Real votes: {real_count} of {total}")
        st.plotly_chart(vote_chart(post.votes), use_container_width=True, key=f"vote_chart_{post.id}")

st.warning("Educational disclaimer: labels and explanations are for media-literacy learning. Always inspect primary evidence and credible fact-checking sources.")
st.info("Fact-checking tips: check the date, author, domain, evidence, context, image origin, independent coverage, and correction history.")
