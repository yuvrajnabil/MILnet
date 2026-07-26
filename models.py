from datetime import datetime, date
from sqlalchemy import (
    Column, Integer, String, Text, Boolean, Date, DateTime,
    ForeignKey, UniqueConstraint
)
from sqlalchemy.orm import relationship
from database import Base

class TimestampMixin:
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

class PublishMixin:
    is_published = Column(Boolean, default=True, nullable=False)

class AdminUser(Base, TimestampMixin):
    __tablename__ = "admin_users"
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

class TeamMember(Base, TimestampMixin, PublishMixin):
    __tablename__ = "team_members"
    id = Column(Integer, primary_key=True)
    slot_number = Column(Integer, nullable=False, unique=True)
    photo_path = Column(String(255))
    full_name = Column(String(150), nullable=False)
    role = Column(String(150))
    designation = Column(String(150))
    institution = Column(String(200))
    biography = Column(Text)
    email = Column(String(150))
    linkedin = Column(String(255))
    facebook = Column(String(255))
    website = Column(String(255))
    contribution = Column(String(255))

class Activity(Base, TimestampMixin, PublishMixin):
    __tablename__ = "activities"
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    activity_date = Column(Date)
    location = Column(String(255))
    short_description = Column(Text)
    full_description = Column(Text)
    cover_image = Column(String(255))
    video_link = Column(String(255))
    status = Column(String(30), default="Upcoming", nullable=False)
    is_featured = Column(Boolean, default=False, nullable=False)
    gallery_images = relationship("ActivityImage", back_populates="activity", cascade="all, delete-orphan")

class ActivityImage(Base, TimestampMixin):
    __tablename__ = "activity_images"
    id = Column(Integer, primary_key=True)
    activity_id = Column(Integer, ForeignKey("activities.id", ondelete="CASCADE"), nullable=False)
    image_path = Column(String(255), nullable=False)
    caption = Column(String(255))
    activity = relationship("Activity", back_populates="gallery_images")

class WeeklyArchive(Base, TimestampMixin, PublishMixin):
    __tablename__ = "weekly_archives"
    id = Column(Integer, primary_key=True)
    week_number = Column(Integer, unique=True, nullable=False)
    week_title = Column(String(200), nullable=False)
    start_date = Column(Date)
    end_date = Column(Date)
    weekly_summary = Column(Text)
    posts = relationship("RealityWallPost", back_populates="archive")

class RealityWallPost(Base, TimestampMixin, PublishMixin):
    __tablename__ = "reality_wall_posts"
    id = Column(Integer, primary_key=True)
    title = Column(String(250), nullable=False)
    image_path = Column(String(255))
    short_description = Column(Text)
    full_explanation = Column(Text)
    original_source = Column(String(255))
    fact_check_source = Column(String(255))
    publication_date = Column(Date)
    week_number = Column(Integer)
    category = Column(String(40), nullable=False)
    verification_status = Column(String(60), nullable=False)
    archive_id = Column(Integer, ForeignKey("weekly_archives.id", ondelete="SET NULL"))
    archive = relationship("WeeklyArchive", back_populates="posts")
    votes = relationship("VisitorVote", back_populates="post", cascade="all, delete-orphan")

class VisitorVote(Base, TimestampMixin):
    __tablename__ = "visitor_votes"
    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey("reality_wall_posts.id", ondelete="CASCADE"), nullable=False)
    vote = Column(String(20), nullable=False)
    session_token = Column(String(120), nullable=False)
    post = relationship("RealityWallPost", back_populates="votes")
    __table_args__ = (UniqueConstraint("post_id", "session_token", name="uq_vote_post_session"),)

class SocialMediaPost(Base, TimestampMixin, PublishMixin):
    __tablename__ = "social_media_posts"
    id = Column(Integer, primary_key=True)
    platform = Column(String(50), nullable=False)
    post_title = Column(String(200), nullable=False)
    description = Column(Text)
    thumbnail_image = Column(String(255))
    publication_date = Column(Date)
    original_post_link = Column(String(255))
    campaign_hashtag = Column(String(100))
    reactions = Column(Integer, default=0)
    shares = Column(Integer, default=0)
    comments = Column(Integer, default=0)
    views = Column(Integer, default=0)
    activity_category = Column(String(100))

class Resource(Base, TimestampMixin, PublishMixin):
    __tablename__ = "resources"
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    resource_type = Column(String(50), nullable=False)
    topic = Column(String(120))
    file_path = Column(String(255))
    external_link = Column(String(255))

class NewsSubmission(Base, TimestampMixin):
    __tablename__ = "news_submissions"
    id = Column(Integer, primary_key=True)
    submitter_name = Column(String(150), nullable=False)
    email = Column(String(150), nullable=False)
    news_title = Column(String(250), nullable=False)
    news_description = Column(Text)
    original_news_link = Column(String(255))
    source_name = Column(String(200))
    image_path = Column(String(255))
    reason_for_suspicion = Column(Text, nullable=False)
    consent = Column(Boolean, default=False, nullable=False)
    review_status = Column(String(50), default="Pending Review", nullable=False)

class ContactMessage(Base, TimestampMixin):
    __tablename__ = "contact_messages"
    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False)
    email = Column(String(150), nullable=False)
    phone = Column(String(50))
    organisation = Column(String(200))
    subject = Column(String(250), nullable=False)
    message = Column(Text, nullable=False)
    is_read = Column(Boolean, default=False, nullable=False)

class WebsiteSetting(Base, TimestampMixin):
    __tablename__ = "website_settings"
    id = Column(Integer, primary_key=True)
    website_name = Column(String(200), default="MIL Reality Check Bangladesh")
    slogan = Column(String(250), default="Think Before You Believe, Verify Before You Share.")
    introduction = Column(Text)
    logo_path = Column(String(255))
    hero_image_path = Column(String(255))
    contact_email = Column(String(150))
    phone_number = Column(String(50))
    address = Column(String(255))
    facebook_link = Column(String(255))
    instagram_link = Column(String(255))
    youtube_link = Column(String(255))
    linkedin_link = Column(String(255))
