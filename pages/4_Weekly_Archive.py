import streamlit as st
from database import init_db
from components.styles import inject_css
init_db()
inject_css()

from services.archive_service import list_archives

st.title("Weekly News Archive")
archives = list_archives()
weeks = sorted({a.week_number for a in archives})
week_filter = st.selectbox("Week filter", ["All"] + weeks)
category_options = sorted({p.category for a in archives for p in a.posts})
status_options = sorted({p.verification_status for a in archives for p in a.posts})
categories = st.multiselect("Category filter", category_options)
statuses = st.multiselect("Verification status filter", status_options)
dates = st.date_input("Date range", value=[])
keyword = st.text_input("Keyword search").strip().lower()

for archive in archives:
    if week_filter != "All" and archive.week_number != week_filter:
        continue
    posts = []
    for p in archive.posts:
        if categories and p.category not in categories: continue
        if statuses and p.verification_status not in statuses: continue
        if keyword and keyword not in f"{p.title} {p.short_description or ''} {p.full_explanation or ''}".lower(): continue
        if isinstance(dates, (list, tuple)) and len(dates) == 2 and p.publication_date:
            if not (dates[0] <= p.publication_date <= dates[1]): continue
        posts.append(p)
    if not posts and (categories or statuses or keyword or (isinstance(dates,(list,tuple)) and len(dates)==2)):
        continue
    with st.expander(f"Week {archive.week_number}: {archive.week_title}", expanded=True):
        st.caption(f"{archive.start_date} to {archive.end_date}")
        st.write(archive.weekly_summary or "")
        for p in posts:
            st.markdown(f"### {p.title}")
            st.write(p.short_description or "")
            st.write(f"Category: {p.category} | Status: {p.verification_status}")
            st.write(f"Source: {p.original_source or 'N/A'}")
            st.write(f"Fact-check: {p.fact_check_source or 'N/A'}")
            st.write(f"Votes: {len(p.votes)}")
