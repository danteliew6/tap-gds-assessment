from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from ..models.Team import Team
from ..models.Match import Match
from flask_cors import CORS
from sqlalchemy import not_, func
from src.football_competition import db
from datetime import datetime
import json
import functools

class MatchController():
    def addTeams():
        try:
            data = request.get_json()
            teams = data['teams']
            for team in teams:
                if team == '':
                    continue
                team = team.split()
                team_name = team[0]
                registration_date = datetime.strptime(team[1], '%d/%m')
                registration_date = registration_date.replace(year=datetime.today().year)
                group = team[2]
                team_obj = Team(team_name = team_name, registration_date = registration_date, group = group) 
                db.session.add(team_obj)
                db.session.flush()
            
            db.session.commit()
            return jsonify({
                "data": {
                    "teams": [team for team in teams]
                }
            }), 201
        except Exception as e:
            return jsonify({
                "message": str(e)
            }), 400

    def addMatches():
        try:
            data = request.get_json()
            matches = data['matches']
            for match in matches:
                if match == '':
                    continue
                match = match.split()
                sorted_team_names = [match[0], match[1]]
                sorted_team_names.sort()
                match_obj = Match(team = sorted_team_names[0], opponent = sorted_team_names[1], team_goals = match[2], opponent_goals = match[3]) 
                team = Team.query.filter(Team.team_name == match_obj.team).first()
                opponent = Team.query.filter(Team.team_name == match_obj.opponent).first()
                if team == None or opponent == None:
                    raise Exception("Either one or both teams do not exist")
                
                team.total_goals += int(match[2])
                opponent.total_goals += int(match[3])
                
                if team.group != opponent.group:
                    raise Exception("both teams are not in the same group")
                
                if int(match[2]) > int(match[3]):
                    team.current_points += 3
                    team.wins += 1
                    opponent.losses += 1
                elif int(match[2]) == int(match[3]):
                    team.current_points += 1
                    team.draws += 1
                    opponent.current_points += 1
                    opponent.draws += 1
                else:
                    opponent.current_points += 3
                    opponent.wins += 1
                    team.losses += 1
                    
                db.session.add(match_obj)
                db.session.flush()
            db.session.commit()
            return jsonify({
                "data": {
                    "matches": [match for match in matches]
                }
            }), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({
                "message": str(e)
            }), 400

        
    def getTeamRankings():
        def compare(teamA, teamB):
            if teamA.current_points != teamB.current_points:
                return teamB.current_points - teamA.current_points
            
            if teamA.total_goals != teamB.total_goals:
                return teamB.total_goals - teamA.total_goals
            
            teamA_points = teamA.wins * 5 + teamA.draws * 3 + teamA.losses
            teamB_points = teamB.wins * 5 + teamB.draws * 3 + teamB.losses
            if teamA_points != teamB_points:
                return teamB_points - teamA_points
            
            if teamA.registration_date.date() > teamB.registration_date.date():
                return 1
            elif teamA.registration_date.date() < teamB.registration_date.date():
                return -1
            
            return 0
        
        try:
            teams = Team.query.order_by(Team.group.asc()).all()
            group_1 = teams[:6]
            group_1 = sorted(group_1, key=functools.cmp_to_key(compare))
            group_2 = teams[6:]
            group_2 = sorted(group_2, key=functools.cmp_to_key(compare))
            return jsonify({
                "data": {
                    "group_1": [team.to_dict() for team  in group_1],
                    "group_2": [team.to_dict() for team  in group_2]
                }
            }), 200
        except Exception as e:
            return jsonify({
                "message": str(e)
            }), 400
            
    def deleteCompetitionData():
        try:
            match_rows_deleted = Match.query.delete()
            team_rows_deleted = Team.query.delete()
            db.session.commit()
            return jsonify({
                "data": {
                    "match_rows_deleted": match_rows_deleted,
                    "team_rows_deleted": team_rows_deleted
                }
            }), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({
                "message": str(e)
            }), 400