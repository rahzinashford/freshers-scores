// Admin dashboard functionality
class AdminDashboard {
    constructor() {
        this.init();
    }

    init() {
        this.bindEvents();
        this.updateTotalScores();
    }

    bindEvents() {
        // Score input changes
        document.addEventListener('input', (e) => {
            if (e.target.classList.contains('score-input')) {
                this.updateTotalScore(e.target.closest('tr'));
            }
        });

        // Individual team update buttons
        document.addEventListener('click', (e) => {
            if (e.target.closest('.update-team-btn')) {
                const teamId = e.target.closest('.update-team-btn').dataset.teamId;
                this.updateTeam(teamId);
            }
        });

        // Save all button
        document.getElementById('saveAllBtn').addEventListener('click', () => {
            this.saveAllTeams();
        });

        // Photo upload
        document.addEventListener('change', (e) => {
            if (e.target.classList.contains('photo-upload')) {
                const teamId = e.target.dataset.teamId;
                this.uploadPhoto(teamId, e.target.files[0]);
            }
        });

        // Finalize results button
        document.getElementById('finalizeBtn').addEventListener('click', () => {
            this.finalizeResults();
        });
    }

    updateTotalScore(row) {
        const scoreInputs = row.querySelectorAll('.score-input');
        let total = 0;
        
        scoreInputs.forEach(input => {
            const value = parseFloat(input.value) || 0;
            total += value;
        });

        const totalScoreElement = row.querySelector('.total-score');
        totalScoreElement.textContent = total.toFixed(1);
        
        // Add visual feedback
        totalScoreElement.classList.add('success-pulse');
        setTimeout(() => {
            totalScoreElement.classList.remove('success-pulse');
        }, 600);
    }

    updateTotalScores() {
        const rows = document.querySelectorAll('tbody tr');
        rows.forEach(row => this.updateTotalScore(row));
    }

    async updateTeam(teamId) {
        const row = document.querySelector(`tr[data-team-id="${teamId}"]`);
        const teamData = this.getTeamDataFromRow(row);

        try {
            this.showLoading();
            
            const response = await fetch(`/api/teams/${teamId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(teamData)
            });

            if (!response.ok) {
                throw new Error('Failed to update team');
            }

            const updatedTeam = await response.json();
            this.showSuccess(row);
            
        } catch (error) {
            console.error('Error updating team:', error);
            this.showError('Failed to update team');
        } finally {
            this.hideLoading();
        }
    }

    async saveAllTeams() {
        const rows = document.querySelectorAll('tbody tr');
        const promises = [];

        for (const row of rows) {
            const teamId = row.dataset.teamId;
            const teamData = this.getTeamDataFromRow(row);
            
            promises.push(
                fetch(`/api/teams/${teamId}`, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(teamData)
                })
            );
        }

        try {
            this.showLoading();
            
            const responses = await Promise.all(promises);
            const failed = responses.filter(r => !r.ok);
            
            if (failed.length > 0) {
                throw new Error(`Failed to update ${failed.length} teams`);
            }

            this.showSuccess();
            
        } catch (error) {
            console.error('Error saving all teams:', error);
            this.showError('Failed to save all teams');
        } finally {
            this.hideLoading();
        }
    }

    async uploadPhoto(teamId, file) {
        if (!file) return;

        const formData = new FormData();
        formData.append('photo', file);

        try {
            this.showLoading();
            
            const response = await fetch(`/api/teams/${teamId}/upload_photo`, {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error('Failed to upload photo');
            }

            const result = await response.json();
            
            // Update the photo display
            const row = document.querySelector(`tr[data-team-id="${teamId}"]`);
            const img = row.querySelector('.team-photo-thumb');
            img.src = result.photo_url;
            
            this.showSuccess(row);
            
        } catch (error) {
            console.error('Error uploading photo:', error);
            this.showError('Failed to upload photo');
        } finally {
            this.hideLoading();
        }
    }

    async finalizeResults() {
        if (!confirm('Are you sure you want to finalize the results? This will trigger the celebration display.')) {
            return;
        }

        try {
            const response = await fetch('/api/finalize_results', {
                method: 'POST'
            });

            if (!response.ok) {
                throw new Error('Failed to finalize results');
            }

            const result = await response.json();
            alert('Results finalized! Check the leaderboard for celebration effects.');
            
        } catch (error) {
            console.error('Error finalizing results:', error);
            this.showError('Failed to finalize results');
        }
    }

    getTeamDataFromRow(row) {
        return {
            name: row.querySelector('.team-name').value,
            dance_score: parseFloat(row.querySelector('[data-score-type="dance_score"]').value) || 0,
            song_score: parseFloat(row.querySelector('[data-score-type="song_score"]').value) || 0,
            ramp_walk_score: parseFloat(row.querySelector('[data-score-type="ramp_walk_score"]').value) || 0,
            game_score: parseFloat(row.querySelector('[data-score-type="game_score"]').value) || 0
        };
    }

    showLoading() {
        document.getElementById('loadingSpinner').classList.remove('d-none');
        document.body.classList.add('loading');
    }

    hideLoading() {
        document.getElementById('loadingSpinner').classList.add('d-none');
        document.body.classList.remove('loading');
    }

    showSuccess(element = null) {
        if (element) {
            element.classList.add('success-pulse');
            setTimeout(() => {
                element.classList.remove('success-pulse');
            }, 600);
        }
    }

    showError(message) {
        alert(message); // Simple error display - could be enhanced with toasts
    }
}

// Initialize admin dashboard when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new AdminDashboard();
});
