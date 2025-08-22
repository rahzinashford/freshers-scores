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
    from models import Team
    if Team.query.count() == 0:
        default_teams = [
            "Team Alpha", "Team Beta", "Team Gamma", "Team Delta", "Team Epsilon",
            "Team Zeta", "Team Eta", "Team Theta", "Team Iota", "Team Kappa", "Team Lambda"
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

