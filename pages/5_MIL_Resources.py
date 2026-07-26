import streamlit as st
from database import init_db
from components.styles import inject_css
init_db()
inject_css()

from pathlib import Path
from services.resource_service import list_resources
from utils import local_file

st.title("MIL Resources")
topics = [
"How to identify fake news","How to verify photographs","How to check sources",
"How to detect manipulated videos","How to avoid spreading misinformation",
"Responsible social media use","Digital safety","Ethical journalism",
"Hate-speech awareness","Gender-sensitive communication","Peacebuilding through media"
]
with st.expander("Learning topics"):
    for topic in topics: st.write(f"• {topic}")

for r in list_resources():
    with st.container(border=True):
        st.subheader(r.title)
        st.caption(f"{r.resource_type} · {r.topic or 'General MIL'}")
        st.write(r.description or "")
        path = local_file(r.file_path)
        if path:
            st.download_button("Download resource", data=path.read_bytes(), file_name=path.name, key=f"download_{r.id}")
        elif r.external_link:
            st.link_button("Open resource", r.external_link)
        else:
            sample = f"{r.title}\n\n{r.description or ''}".encode()
            st.download_button("Download sample text", sample, file_name=f"resource_{r.id}.txt", key=f"sample_{r.id}")
