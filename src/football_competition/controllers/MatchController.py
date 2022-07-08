from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from ..models.Team import Team
from ..models.Match import Match
from flask_cors import CORS
from sqlalchemy import not_, func
from src.football_competition import db
from datetime import datetime
import json

class MatchController():
    def addTeams():
        try:
            # data = request.get_json()
            data = request.get_json()
            teams = data['teams']
            for team in teams:
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
            }), 401

    def addMatches():
        try:
            data = request.get_json()
            matches = data['matches']
            for match in matches:
                match = match.split()
                match_obj = Match(team = match[0], opponent = match[1], team_goals = match[2], opponent_goals = match[3]) 
                team = Team.query.filter(Team.team_name == match[0]).first()
                team.total_goals += int(match[2])
                opponent = Team.query.filter(Team.team_name == match[1]).first()
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
            return jsonify({
                "message": str(e)
            }), 401

    def sortTiedTeams(teamA, teamB):
        if teamA.total_goals != teamB.total_goals:
            return teamA.total_goals - teamB.total_goals
        
        teamA_points = teamA.wins * 5 + teamA.draws * 3 + teamA.losses
        teamB_points = teamB.wins * 5 + teamB.draws * 3 + teamB.losses
        if teamA_points != teamB_points:
            return teamA_points - teamB_points
        
        return teamA.registration_date - teamB.registration_date
        
    def getTeamRankings():
        def sortTiedTeams(teamA, teamB):
            if teamA.total_goals != teamB.total_goals:
                return teamA.total_goals - teamB.total_goals
            
            teamA_points = teamA.wins * 5 + teamA.draws * 3 + teamA.losses
            teamB_points = teamB.wins * 5 + teamB.draws * 3 + teamB.losses
            if teamA_points != teamB_points:
                return teamA_points - teamB_points
            
            return teamA.registration_date - teamB.registration_date
        
        try:
            teams = Team.query.order_by(Team.group.asc(), Team.current_points.desc()).all()
            group_1 = teams[:6]
            group_1.sort(key=sortTiedTeams)
            group_2 = teams[6:]
            group_2.sort(key=sortTiedTeams)
            return jsonify({
                "data": {
                    "group_1": [team.to_dict() for team  in group_1],
                    "group_2": [team.to_dict() for team  in group_2]
                }
            }), 201
        except Exception as e:
            return jsonify({
                "message": str(e)
            }), 401
            
    