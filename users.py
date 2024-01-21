from database import db
class Users(db.Model):
    userid = db.Column(db.String(255), primary_key=True, nullable=True, server_default=db.text('NULL::character varying'))
    username = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255))
    password = db.Column(db.String(255))
    admin = db.Column(db.Boolean, default=False)

    def __str__(self):
        return f"User: {self.userid}, {self.username}, {self.email}, {self.password}, {self.admin}"
