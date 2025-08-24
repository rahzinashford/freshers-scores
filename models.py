from app import db
from datetime import datetime

class Performance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    performer_name = db.Column(db.String(100), nullable=False)
    performance_type = db.Column(db.String(50), nullable=False)  # Group Dance, Solo Dance, Song, etc.
    year = db.Column(db.String(10), nullable=False)  # I, II, III
    contact_number = db.Column(db.String(15), nullable=True)
    mc_session = db.Column(db.String(20), nullable=True)  # MC-1, MC-2, etc.
    time_slot = db.Column(db.String(50), nullable=True)  # 9:15-9:45Am, etc.
    is_completed = db.Column(db.Boolean, default=False)
    completed_at = db.Column(db.DateTime, nullable=True)
    notes = db.Column(db.Text, nullable=True)
    
    def to_dict(self):
        """Convert performance object to dictionary for JSON responses"""
        return {
            'id': self.id,
            'performer_name': self.performer_name,
            'performance_type': self.performance_type,
            'year': self.year,
            'contact_number': self.contact_number,
            'mc_session': self.mc_session,
            'time_slot': self.time_slot,
            'is_completed': self.is_completed,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'notes': self.notes
        }
    
    def mark_completed(self):
        """Mark performance as completed"""
        self.is_completed = True
        self.completed_at = datetime.utcnow()

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    photo_url = db.Column(db.String(200), nullable=True)
    dance_score = db.Column(db.Float, default=0.0)
    song_score = db.Column(db.Float, default=0.0)
    ramp_walk_score = db.Column(db.Float, default=0.0)
    game_score = db.Column(db.Float, default=0.0)
    
    @property
    def total_score(self):
        """Calculate total score from all rounds"""
        return self.dance_score + self.song_score + self.ramp_walk_score + self.game_score
    
    def to_dict(self):
        """Convert team object to dictionary for JSON responses"""
        return {
            'id': self.id,
            'name': self.name,
            'photo_url': self.photo_url,
            'dance_score': self.dance_score,
            'song_score': self.song_score,
            'ramp_walk_score': self.ramp_walk_score,
            'game_score': self.game_score,
            'total_score': self.total_score
        }
