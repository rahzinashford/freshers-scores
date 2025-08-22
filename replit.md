# Overview

This is a Flask web application for managing and displaying scores for college event competitions. The application features a public leaderboard that displays team rankings and an admin dashboard for managing team information and scores. Teams compete in four different events: Dance, Song, Ramp Walk, and Game, with a combined total score determining their ranking.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Backend Architecture
- **Framework**: Flask web framework with SQLAlchemy ORM for database operations
- **Database**: SQLite as the default database with configurable DATABASE_URL for production deployments
- **Models**: Single Team model storing team information and scores for four event categories
- **API Design**: RESTful endpoints for team data retrieval and updates (`/api/teams`)
- **File Handling**: Image upload system for team photos with file type validation and size limits

## Frontend Architecture
- **Template Engine**: Jinja2 templating with base template inheritance
- **UI Framework**: Bootstrap 5 with dark theme for responsive design
- **JavaScript Architecture**: Modular class-based approach with separate files for admin dashboard, leaderboard, and confetti animations
- **Real-time Updates**: Auto-refresh functionality on leaderboard (5-second intervals)
- **Asset Management**: Static file serving for CSS, JavaScript, and uploaded images

## Data Storage
- **Primary Storage**: SQLite database with Team table containing scoring fields
- **File Storage**: Local filesystem storage for team photos in `static/uploads` directory
- **Session Management**: Flask sessions with configurable secret key
- **Data Validation**: Input validation for scores (0-100 range) and file uploads

## Authentication & Authorization
- **Security Model**: No authentication system implemented - open access to both admin and public views
- **File Security**: Secure filename handling for uploads with allowed file extension filtering
- **Environment Configuration**: Environment variable support for database URL and session secrets

# External Dependencies

## Third-party Services
- **CDN Resources**: Bootstrap CSS/JS and Font Awesome icons served from external CDNs
- **No External APIs**: Application operates independently without external service dependencies

## Python Dependencies
- **Flask**: Web framework and core functionality
- **Flask-SQLAlchemy**: Database ORM and model management
- **Werkzeug**: WSGI utilities including ProxyFix middleware and secure filename handling

## Frontend Libraries
- **Bootstrap 5**: UI framework with dark theme variant
- **Font Awesome 6**: Icon library for UI elements
- **Vanilla JavaScript**: No external JavaScript frameworks - uses native browser APIs

## Development Tools
- **Database**: SQLite for development, PostgreSQL-compatible for production
- **File Upload**: Built-in Flask file handling with configurable upload directory
- **Logging**: Python's built-in logging module configured for debug level