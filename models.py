from datetime import datetime
from db import db

class URL(db.Model):
    __tablename__ = "urls"
    id = db.Column(db.Integer,primary_key=True,index=True)
    original_url = db.Column(db.String(2048),nullable=False)
    short_code = db.Column(db.String(32),unique=True,nullable=False)
    created_at = db.Column(db.DateTime(timezone=True),default=datetime.now)
    visits = db.relationship("Visit",back_populates="url",cascade="all,delete")

class Visit(db.Model):
    __tablename__ = "visits"
    id = db.Column(db.Integer,primary_key=True,index=True)
    url_id = db.Column(db.Integer,db.ForeignKey("urls.id",ondelete="CASCADE"))
    timestamp = db.Column(db.DateTime(timezone=True),default=datetime.now)
    user_agent = db.Column(db.String(256),nullable=False)
    referrer = db.Column(db.String(256),nullable=True)
    url=db.relationship("URL",back_populates="visits")
    