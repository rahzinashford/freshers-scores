import os
from flask import render_template, request, jsonify, redirect, url_for, flash
from werkzeug.utils import secure_filename
from app import app, db
from models import Team

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Redirect to leaderboard as default page"""
    return redirect(url_for('leaderboard'))

@app.route('/admin')
def admin():
    """Admin dashboard for managing teams and scores"""
    teams = Team.query.order_by(Team.id).all()
    return render_template('admin.html', teams=teams)

@app.route('/leaderboard')
def leaderboard():
    """Public leaderboard showing teams sorted by total score"""
    teams = Team.query.all()
    # Sort teams by total score in descending order
    teams.sort(key=lambda x: x.total_score, reverse=True)
    return render_template('leaderboard.html', teams=teams)

@app.route('/api/teams', methods=['GET'])
def get_teams():
    """API endpoint to get all teams data"""
    teams = Team.query.all()
    teams_data = [team.to_dict() for team in teams]
    # Sort by total score descending
    teams_data.sort(key=lambda x: x['total_score'], reverse=True)
    return jsonify(teams_data)

@app.route('/api/teams/<int:team_id>', methods=['PUT'])
def update_team(team_id):
    """API endpoint to update team data"""
    team = Team.query.get_or_404(team_id)
    data = request.get_json()
    
    if 'name' in data:
        team.name = data['name']
    if 'dance_score' in data:
        team.dance_score = float(data['dance_score'])
    if 'song_score' in data:
        team.song_score = float(data['song_score'])
    if 'ramp_walk_score' in data:
        team.ramp_walk_score = float(data['ramp_walk_score'])
    if 'game_score' in data:
        team.game_score = float(data['game_score'])
    
    db.session.commit()
    return jsonify(team.to_dict())

@app.route('/api/teams/<int:team_id>/upload_photo', methods=['POST'])
def upload_team_photo(team_id):
    """API endpoint to upload team photo"""
    team = Team.query.get_or_404(team_id)
    
    if 'photo' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['photo']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and allowed_file(file.filename):
        # Create secure filename with team ID prefix
        filename = secure_filename(f"team_{team_id}_{file.filename}")
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Remove old photo if exists
        if team.photo_url:
            old_file_path = os.path.join('static', team.photo_url.lstrip('/'))
            if os.path.exists(old_file_path):
                os.remove(old_file_path)
        
        file.save(file_path)
        team.photo_url = f"/static/uploads/{filename}"
        db.session.commit()
        
        return jsonify({
            'message': 'Photo uploaded successfully',
            'photo_url': team.photo_url
        })
    
    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/api/finalize_results', methods=['POST'])
def finalize_results():
    """API endpoint to finalize results and trigger celebration"""
    teams = Team.query.all()
    teams.sort(key=lambda x: x.total_score, reverse=True)
    
    # Get top 3 teams
    top_teams = teams[:3] if len(teams) >= 3 else teams
    top_team_ids = [team.id for team in top_teams]
    
    return jsonify({
        'message': 'Results finalized',
        'top_teams': top_team_ids
    })
