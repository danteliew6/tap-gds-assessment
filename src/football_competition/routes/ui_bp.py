from flask import Blueprint
from ..controllers.UIController import UIController


ui_bp = Blueprint("ui_bp", __name__,template_folder='templates')

ui_bp.route('/')(UIController.index)
ui_bp.route('/team_rankings')(UIController.team_rankings)