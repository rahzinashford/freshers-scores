from app import db

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
