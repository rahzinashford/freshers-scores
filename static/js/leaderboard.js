// Leaderboard functionality
class Leaderboard {
    constructor() {
        this.refreshInterval = null;
        this.init();
    }

    init() {
        this.bindEvents();
        this.startAutoRefresh();
    }

    bindEvents() {
        // Manual refresh button
        document.getElementById('refreshBtn').addEventListener('click', () => {
            this.refreshData();
        });
    }

    startAutoRefresh() {
        // Refresh every 5 seconds
        this.refreshInterval = setInterval(() => {
            this.refreshData();
        }, 5000);
    }

    stopAutoRefresh() {
        if (this.refreshInterval) {
            clearInterval(this.refreshInterval);
            this.refreshInterval = null;
        }
    }

    async refreshData() {
        try {
            const response = await fetch('/api/teams');
            if (!response.ok) {
                throw new Error('Failed to fetch teams data');
            }

            const teams = await response.json();
            this.updateLeaderboard(teams);
            this.updateRankingStyles(teams);
            
        } catch (error) {
            console.error('Error refreshing data:', error);
        }
    }

    updateLeaderboard(teams) {
        const grid = document.getElementById('leaderboardGrid');
        
        teams.forEach((team, index) => {
            const teamCard = document.querySelector(`[data-team-id="${team.id}"]`);
            if (!teamCard) return;

            // Update team name
            const nameElement = teamCard.querySelector('.card-title');
            if (nameElement) nameElement.textContent = team.name;

            // Update photo if changed
            const photoElement = teamCard.querySelector('.team-photo-display');
            if (photoElement && team.photo_url) {
                photoElement.src = team.photo_url;
            }

            // Update individual scores
            const danceScore = teamCard.querySelector('.dance-score');
            const songScore = teamCard.querySelector('.song-score');
            const rampWalkScore = teamCard.querySelector('.ramp-walk-score');
            const gameScore = teamCard.querySelector('.game-score');
            const totalScore = teamCard.querySelector('.total-score');

            if (danceScore) danceScore.textContent = team.dance_score.toFixed(1);
            if (songScore) songScore.textContent = team.song_score.toFixed(1);
            if (rampWalkScore) rampWalkScore.textContent = team.ramp_walk_score.toFixed(1);
            if (gameScore) gameScore.textContent = team.game_score.toFixed(1);
            if (totalScore) totalScore.textContent = team.total_score.toFixed(1);

            // Reorder cards based on ranking
            const cardCol = teamCard.closest('.col-lg-4');
            grid.appendChild(cardCol);
        });
    }

    updateRankingStyles(teams) {
        // Remove all ranking classes first
        const allCards = document.querySelectorAll('.team-card');
        allCards.forEach(card => {
            card.classList.remove('winner', 'runner-up', 'third-place');
        });

        // Apply ranking styles to top 3
        if (teams.length >= 1) {
            const winnerCard = document.querySelector(`[data-team-id="${teams[0].id}"]`);
            if (winnerCard) winnerCard.classList.add('winner');
        }

        if (teams.length >= 2) {
            const runnerUpCard = document.querySelector(`[data-team-id="${teams[1].id}"]`);
            if (runnerUpCard) runnerUpCard.classList.add('runner-up');
        }

        if (teams.length >= 3) {
            const thirdPlaceCard = document.querySelector(`[data-team-id="${teams[2].id}"]`);
            if (thirdPlaceCard) thirdPlaceCard.classList.add('third-place');
        }
    }

    triggerCelebration() {
        // Trigger confetti effect
        if (window.Confetti) {
            window.Confetti.create();
        }

        // Add celebration class to top teams
        const topCards = document.querySelectorAll('.winner, .runner-up, .third-place');
        topCards.forEach(card => {
            card.classList.add('success-pulse');
            setTimeout(() => {
                card.classList.remove('success-pulse');
            }, 2000);
        });
    }
}

// Check for celebration trigger from URL params or localStorage
function checkForCelebration() {
    const urlParams = new URLSearchParams(window.location.search);
    const celebrate = urlParams.get('celebrate') || localStorage.getItem('celebrate');
    
    if (celebrate === 'true') {
        setTimeout(() => {
            if (window.leaderboard) {
                window.leaderboard.triggerCelebration();
            }
        }, 1000);
        
        // Clear the celebration flag
        localStorage.removeItem('celebrate');
        
        // Clean URL
        if (urlParams.get('celebrate')) {
            const newUrl = window.location.pathname;
            window.history.replaceState({}, document.title, newUrl);
        }
    }
}

// Initialize leaderboard when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.leaderboard = new Leaderboard();
    checkForCelebration();
});

// Clean up interval when page is unloaded
window.addEventListener('beforeunload', () => {
    if (window.leaderboard) {
        window.leaderboard.stopAutoRefresh();
    }
});
