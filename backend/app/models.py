from app import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(255),default="User")
    timestamp = db.Column(db.DateTime,default=datetime.utcnow)

    reports = db.relationship('Report',backref=db.backref('user',uselist=False),lazy=True) 
                   

class Report(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    validity = db.Column(db.Boolean,default=False)
    reachability = db.Column(db.String(255))
    formation = db.Column(db.String(255))
    dns = db.Column(db.String(255))
    whois = db.Column(db.String(255))
    ssl = db.Column(db.Boolean, default=False)
    score = db.Column(db.Integer,default=0)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)

