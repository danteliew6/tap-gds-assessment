from flask import Flask, request, jsonify, render_template


class UIController():
    def index():
        return render_template('./index.html')
    
    def team_rankings():
        return render_template('./team_rankings.html')
    