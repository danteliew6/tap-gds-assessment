from flask import Blueprint
from ..controllers.MatchController import MatchController


competition_bp = Blueprint("competition_bp", __name__)

# class_bp.route('/classlist', methods=['GET'])(ClassController.getClassList)
competition_bp.route('/add-teams', methods=['POST'])(MatchController.addTeams)
competition_bp.route('/add-matches', methods=['POST'])(MatchController.addMatches)
competition_bp.route('/get-team-rankings', methods=['GET'])(MatchController.getTeamRankings)




