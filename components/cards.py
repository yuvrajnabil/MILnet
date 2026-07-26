import streamlit as st


def info_card(title, description, icon="💡"):
    with st.container(border=True):
        st.markdown(
            f"<div style='font-size:2rem; text-align:center;'>{icon}</div>",
            unsafe_allow_html=True,
        )

        st.subheader(title)
        st.write(description)


def team_card(member):
    """
    TeamMember model-এর সঙ্গে compatible safe card.
    """

    image = getattr(member, "photo_path", None)

    name = (
        getattr(member, "full_name", None)
        or "Team Member"
    )

    designation = (
        getattr(member, "designation", None)
        or getattr(member, "role", None)
        or "Member"
    )

    institution = getattr(member, "institution", None)

    bio = (
        getattr(member, "biography", None)
        or ""
    )

    email = getattr(member, "email", None)

    with st.container(border=True):
        if image:
            try:
                st.image(image, use_container_width=True)
            except Exception:
                pass

        st.subheader(name)
        st.caption(designation)

        if institution:
            st.write(f"**{institution}**")

        if bio:
            st.write(bio)

        if email:
            st.caption(f"📧 {email}")


def activity_card(activity):
    """
    Activity model-এর সঙ্গে compatible safe activity card.
    """

    cover_image = getattr(activity, "cover_image", None)
    title = getattr(activity, "title", None) or "Untitled Activity"
    status = getattr(activity, "status", None) or "Upcoming"
    activity_date = getattr(activity, "activity_date", None)
    location = getattr(activity, "location", None)
    short_description = getattr(activity, "short_description", None)
    full_description = getattr(activity, "full_description", None)
    is_featured = getattr(activity, "is_featured", False)

    with st.container(border=True):
        if cover_image:
            try:
                st.image(cover_image, use_container_width=True)
            except Exception:
                pass

        title_col, status_col = st.columns([4, 1])

        with title_col:
            st.subheader(title)

        with status_col:
            if status == "Ongoing":
                st.success("Ongoing")
            elif status == "Completed":
                st.info("Completed")
            else:
                st.warning(status)

        if is_featured:
            st.caption("⭐ Featured activity")

        details = []

        if activity_date:
            details.append(f"📅 {activity_date.strftime('%d %B %Y')}")

        if location:
            details.append(f"📍 {location}")

        if details:
            st.caption("   |   ".join(details))

        if short_description:
            st.write(short_description)

        if full_description and full_description != short_description:
            with st.expander("Read more"):
                st.write(full_description)