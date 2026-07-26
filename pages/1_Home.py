import streamlit as st
from database import init_db
from components.styles import inject_css
from components.footer import render_footer
from components.cards import info_card, team_card
from services.site_service import get_settings
from services.activity_service import list_activities
from services.reality_wall_service import list_posts, total_votes
from services.archive_service import list_archives
from services.social_media_service import list_social_posts
from services.team_service import list_team
from database import get_session
from models import TeamMember, Resource

init_db()
inject_css()

s = get_settings()
st.markdown(
    f"""<div class="hero">
    <h1>{s.website_name}</h1>
    <p><b>{s.slogan}</b></p>
    <p>{s.introduction or ""}</p>
    </div>""",
    unsafe_allow_html=True
)

if s.hero_image_path:
    from utils import show_image
    show_image(s.hero_image_path)

c1, c2 = st.columns([1, 1])
with c1:
    if st.button("Explore Reality Wall", type="primary", use_container_width=True):
        st.switch_page("pages/2_Reality_Wall.py")
with c2:
    if st.button("View Current Activities", use_container_width=True):
        st.switch_page("pages/3_Current_Activities.py")

activities = list_activities()
posts = list_posts()
archives = list_archives()
social = list_social_posts()
team = list_team()

st.header("Current Featured Activity")
featured = next(
    (a for a in activities if a.is_featured and a.status == "Ongoing"),
    activities[0] if activities else None
)
if featured:
    with st.container(border=True):
        st.subheader(featured.title)
        st.write(featured.short_description or "")
        st.caption(f"{featured.activity_date or 'Date TBA'} · {featured.location or 'Location TBA'}")
else:
    st.info("No featured activity is available yet.")

st.header("Latest Updates")
u1, u2, u3 = st.columns(3)
with u1:
    st.subheader("Reality Wall")
    if posts:
        st.write(f"**{posts[0].title}**")
        st.write(posts[0].short_description or "")
    else:
        st.info("No Reality Wall post yet.")
with u2:
    st.subheader("Weekly Archive")
    if archives:
        st.write(f"**Week {archives[0].week_number}: {archives[0].week_title}**")
        st.write(archives[0].weekly_summary or "")
    else:
        st.info("No archive yet.")
with u3:
    st.subheader("Social Media")
    if social:
        st.write(f"**{social[0].platform}: {social[0].post_title}**")
        st.write(social[0].description or "")
    else:
        st.info("No social activity yet.")

st.header("About the Initiative")
about_tabs = st.tabs(["What is MIL?", "Why it matters", "Who is involved", "MIL Cities"])
with about_tabs[0]:
    st.info(
        "Media and Information Literacy means the ability to access, understand, evaluate, "
        "create, and share information responsibly."
    )
    st.write(
        "It helps people question viral claims, identify manipulated content, check reliable "
        "sources, and make informed decisions."
    )
with about_tabs[1]:
    st.warning(
        "Misinformation, disinformation, hate speech, racism, and manipulated media can damage "
        "public trust, safety, social harmony, and democratic participation."
    )
    st.success(
        "MIL promotes critical thinking, responsible journalism, digital citizenship, "
        "gender-sensitive communication, freedom of expression, and peacebuilding."
    )
with about_tabs[2]:
    left, right = st.columns(2)
    with left:
        st.markdown("**Journalists and media organisations**")
        st.write("Verify sources, explain evidence, correct errors, and avoid amplifying harmful claims.")
        st.markdown("**Students and youth groups**")
        st.write("Develop fact-checking habits and encourage responsible online behaviour.")
        st.markdown("**Educational institutions**")
        st.write("Integrate verification, ethics, and critical thinking into learning.")
    with right:
        st.markdown("**Government bodies**")
        st.write("Provide transparent, accessible, and evidence-based public communication.")
        st.markdown("**Civil society organisations**")
        st.write("Build community awareness and respond to harmful narratives.")
        st.markdown("**United Nations agencies**")
        st.write("Support standards, partnerships, Global MIL Week, and capacity-building.")
with about_tabs[3]:
    st.write(
        "MIL Cities bring media literacy into schools, local government, public spaces, "
        "community programmes, cultural institutions, and digital services."
    )
    st.write(
        "This supports Smart Bangladesh Vision 2041 through Smart Citizens, Smart Government, "
        "Smart Economy, and Smart Society."
    )

st.header("Smart Bangladesh Vision 2041")
cols = st.columns(4)
cards = [
    ("Smart Citizens", "Critical thinkers who verify information before acting or sharing.", "👥"),
    ("Smart Government", "Transparent, evidence-based communication and public services.", "🏛️"),
    ("Smart Economy", "Trustworthy digital markets, innovation, and informed consumers.", "📈"),
    ("Smart Society", "Inclusive, peaceful, safe, and resilient communities.", "🤝"),
]
for col, (title, text, icon) in zip(cols, cards):
    with col:
        info_card(title, text, icon)

with get_session() as db:
    team_count = db.query(TeamMember).count()
    resource_count = db.query(Resource).count()

st.header("Project Statistics")
m1, m2, m3, m4 = st.columns(4)
m1.metric("Reality Wall posts", len(posts))
m2.metric("Public votes", total_votes())
m3.metric("Team members", team_count)
m4.metric("MIL resources", resource_count)

st.header("Meet Our Team")
st.write("Our ten editable team profile slots are managed from the Admin Dashboard.")
for start in range(0, min(len(team), 10), 5):
    cols = st.columns(5)
    for col, member in zip(cols, team[start:start+5]):
        with col:
            team_card(member)

render_footer()
