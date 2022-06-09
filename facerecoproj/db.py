from .main import db
import sqlalchemy.types as types


class ChoiceType(types.TypeDecorator):
    impl = types.String

    def __init__(self, choices, **kw):
        self.choices = dict(choices)
        super(ChoiceType, self).__init__(**kw)

    def process_bind_param(self, value, dialect):
        return [k for k, v in self.choices.items() if v == value][0]

    def process_result_value(self, value, dialect):
        return self.choices[value]


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    dept = db.Column(db.String(50))
    gender = db.Column(ChoiceType({"male": "male", "female": "female"}), nullable=False)

    def __str__(self):
        return self.name
