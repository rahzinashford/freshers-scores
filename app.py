import os
import logging

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix

# Setup logging
logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# configure the database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///event_scores.db")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# File upload configuration
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create upload directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# initialize the app with the extension
db.init_app(app)

with app.app_context():
    # Import models and routes
    import models
    import routes
    
    # Create tables
    db.create_all()
    
    # Initialize default teams if none exist
    from models import Team, Performance
    if Team.query.count() == 0:
        default_teams = [
            "Team Alpha", "Team Beta", "Team Gamma", "Team Delta", "Team Epsilon",
            "Team Zeta", "Team Eta", "Team Theta", "Team Iota", "Team Kappa", "Team Lambda",
            "Team 12", "Team 13", "Team 14", "Team 15", "Team 16", "Team 17", "Team 18", "Team 19", "Team 20"
        ]
        
        for i, team_name in enumerate(default_teams, 1):
            team = Team(
                name=team_name,
                photo_url=None,
                dance_score=0,
                song_score=0,
                ramp_walk_score=0,
                game_score=0
            )
            db.session.add(team)
        
        db.session.commit()
        logging.info("Created 11 default teams")

    # Initialize performance data if none exist
    if Performance.query.count() == 0:
        performances_data = [
            # MC-1 (9:15-9:45Am)
            ('Diya', 'Group Dance', 'III', None, 'MC-1', '9:15-9:45Am'),
            ('Shivada', 'Duo Dance', 'III', '6362819768', 'MC-1', '9:15-9:45Am'),
            ('Mizaj', 'Song', 'II', '8129795812', 'MC-1', '9:15-9:45Am'),
            ('Vaishnav', 'Group Dance', 'II', '8891803450', 'MC-1', '9:15-9:45Am'),
            ('Ayesha', 'Group Dance', 'I', '9483281379', 'MC-1', '9:15-9:45Am'),
            
            # MC-2 (10:10-10:35Am)
            ('Sagara', 'Single Dance', 'II', '9567257130', 'MC-2', '10:10-10:35Am'),
            ('Hiraganna', 'Song', 'I', '8618080826', 'MC-2', '10:10-10:35Am'),
            ('Nandhana TS', 'Group Dance', 'III', '9995845193', 'MC-2', '10:10-10:35Am'),
            ('Shanumol', 'Group Dance', 'II', '97455590308', 'MC-2', '10:10-10:35Am'),
            ('Mushayil', 'Group Dance', 'I', '8589887788', 'MC-2', '10:10-10:35Am'),
            ('Gouri lakshmi', 'Group Dance', 'III', '7560860551', 'MC-2', '10:10-10:35Am'),
            
            # MC-3 (10:35-11:00Am)
            ('Devna Mohanan', 'Duo Dance', 'I', '8606390525', 'MC-3', '10:35-11:00Am'),
            ('Antonia Elizabeth', 'Group Dance', 'II', '8590456825', 'MC-3', '10:35-11:00Am'),
            ('Devanjana', 'Group Dance', 'II', '8891789148', 'MC-3', '10:35-11:00Am'),
            ('Afsal', 'Group Dance', 'I', '9633801508', 'MC-3', '10:35-11:00Am'),
            ('Rihan', 'Group Dance', 'I', '6363921190', 'MC-3', '12:00PM-12:30PM'),
            ('Ananya', 'Group Dance', 'II', '8075010479', 'MC-3', '10:35-11:00Am'),
            
            # MC-4 (11:00-11:25Am)
            ('Mohammed Shamoor', 'Group Dance', 'II', '9567266227', 'MC-4', '11:00-11:25Am'),
            ('Anvika Pramod', 'Group Dance', 'I', '8089034221', 'MC-4', '11:00-11:25Am'),
            ('Fathima Noora', 'Group Dance', 'I', '6235827872', 'MC-4', '11:00-11:25Am'),
            ('Fathiamath nafiya', 'Group Dance', 'III', '9747580616', 'MC-4', '11:00-11:25Am'),
            ('Aakil P P', 'Song', 'II', '9188294280', 'MC-4', '11:00-11:25Am'),
            ('Neha Sreejith', 'Group Dance', 'III', '7736502367', 'MC-4', '11:00-11:25Am'),
            
            # MC-5 (11:25-12:00PM)
            ('Mohammed Rafi T A', 'Group Dance', 'I', '6235154329', 'MC-5', '11:25-12:00PM'),
            ('Alona', 'Group Dance', 'II', '7025912439', 'MC-5', '11:25-12:00PM'),
            ('DevaSurya', 'Group Dance', 'II', '9400716943', 'MC-5', '11:25-12:00PM'),
            ('Niya', 'Group Dance', 'I', '7736534948', 'MC-5', '11:25-12:00PM'),
            ('Mohammed Nazim', 'Group Dance', 'III', '9037018545', 'MC-5', '11:25-12:00PM'),
            ('Rania', 'Group Dance', 'II', None, 'MC-5', '11:25-12:00PM'),
            ('Rajid', 'Group Dance', 'III', '8129282290', 'MC-5', '11:25-12:00PM'),
            ('Gourav', 'Group Dance', 'II', '7994470146', 'MC-5', '11:25-12:00PM'),
            
            # MC-6 (12:00PM-12:30PM)
            ('Surya Priya', 'Dance', 'III', '8590153302', 'MC-6', '12:00PM-12:30PM'),
            ('Amna', 'Group Dance', 'I', '8129546675', 'MC-6', '12:00PM-12:30PM'),
            ('Zia', 'Solo Dance', 'I', '9037866766', 'MC-6', '12:00PM-12:30PM'),
            ('Mazin', 'Group Dance', 'II', '7306654922', 'MC-6', '12:00PM-12:30PM'),
            ('Sillambazhagi', 'Martial Arts', 'III', '9043571145', 'MC-6', '10:35-11:00Am'),
            
            # MC-7 - Ramp Walk (12:30-1:00PM)
            ('Second years', 'Ramp Walk', 'II', None, 'MC-7', '12:30-1:00PM'),
            ('First years', 'Ramp Walk', 'I', None, 'MC-7', '12:30-1:00PM'),
            
            # Band (1:10-1:30PM)
            ('Shivaganga', 'Song', 'Band', '6235182816', 'Band', '1:10-1:30PM'),
            ('Zaied', 'Song', 'Band', '9495840773', 'Band', '1:10-1:30PM'),
            ('Mohammed Ubaid', 'Song', 'Band', '9663661357', 'Band', '1:10-1:30PM'),
        ]
        
        for performer_name, performance_type, year, contact_number, mc_session, time_slot in performances_data:
            performance = Performance(
                performer_name=performer_name,
                performance_type=performance_type,
                year=year,
                contact_number=contact_number,
                mc_session=mc_session,
                time_slot=time_slot
            )
            db.session.add(performance)
        
        db.session.commit()
        logging.info("Created performance schedule data")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

