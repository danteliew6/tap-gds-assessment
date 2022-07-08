from src.football_competition import db


class Team(db.Model):
    # Start of DB model
    __tablename__ = 'teams'
    __mapper_args__ = {'polymorphic_identity': 'teams'}
    __table_args__={'mysql_engine':'InnoDB'}


    team_name = db.Column(db.String(50), primary_key = True)
    group = db.Column(db.Integer())
    registration_date = db.Column(db.DateTime())
    current_points = db.Column(db.Integer(), default = 0)
    total_goals = db.Column(db.Integer(), default = 0)
    wins =  db.Column(db.Integer(), default = 0)
    draws =  db.Column(db.Integer(), default = 0)
    losses =  db.Column(db.Integer(), default = 0)


    def to_dict(self):
        """
        'to_dict' converts the object into a dictionary,
        in which the keys correspond to database columns
        """
        columns = self.__mapper__.column_attrs.keys()
        result = {}
        for column in columns:
            result[column] = getattr(self, column)
        return result