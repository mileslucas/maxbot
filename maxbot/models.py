from maxbot import db

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gm_id = db.Column(db.String(100))
    user_id = db.Column(db.String(100))
    name = db.Column(db.String(60))
    text = db.Column(db.String(2000))

    def __repr__(self):
        return '{} said: {}'.format(self.name, self.text)



