from src.football_competition import db


class Match(db.Model):
    # Start of DB model
    __tablename__ = 'matches'
    __mapper_args__ = {'polymorphic_identity': 'matches'}
    __table_args__={'mysql_engine':'InnoDB','mysql_auto_increment': '1'}


    team = db.Column(db.String(50),  db.ForeignKey('teams.team_name'), primary_key = True)
    opponent = db.Column(db.String(50),  db.ForeignKey('teams.team_name'), primary_key = True)
    round = db.Column(db.Integer(), primary_key = True, default = 1)
    team_goals = db.Column(db.Integer())
    opponent_goals = db.Column(db.Integer()) 


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