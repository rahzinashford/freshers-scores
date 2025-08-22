// Confetti animation system
class Confetti {
    constructor() {
        this.container = null;
        this.pieces = [];
        this.colors = ['#ffd700', '#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4', '#feca57'];
        this.isActive = false;
    }

    static create() {
        const confetti = new Confetti();
        confetti.init();
        return confetti;
    }

    init() {
        this.createContainer();
        this.startAnimation();
    }

    createContainer() {
        this.container = document.getElementById('confettiContainer');
        if (!this.container) {
            this.container = document.createElement('div');
            this.container.id = 'confettiContainer';
            this.container.style.cssText = `
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                pointer-events: none;
                z-index: 9999;
                overflow: hidden;
            `;
            document.body.appendChild(this.container);
        }
    }

    createPiece() {
        const piece = document.createElement('div');
        piece.className = 'confetti-piece';
        
        const color = this.colors[Math.floor(Math.random() * this.colors.length)];
        const size = Math.random() * 8 + 4; // 4-12px
        const startX = Math.random() * window.innerWidth;
        const animationDuration = Math.random() * 2 + 2; // 2-4 seconds
        const animationDelay = Math.random() * 2; // 0-2 seconds delay
        
        piece.style.cssText = `
            position: absolute;
            width: ${size}px;
            height: ${size}px;
            background: ${color};
            left: ${startX}px;
            top: -10px;
            border-radius: ${Math.random() > 0.5 ? '50%' : '0'};
            animation: confetti-fall ${animationDuration}s linear ${animationDelay}s forwards;
            transform: rotate(${Math.random() * 360}deg);
        `;
        
        return piece;
    }

    startAnimation() {
        if (this.isActive) return;
        
        this.isActive = true;
        const pieceCount = 100;
        
        // Create initial burst
        for (let i = 0; i < pieceCount; i++) {
            const piece = this.createPiece();
            this.container.appendChild(piece);
            this.pieces.push(piece);
        }
        
        // Continue creating pieces for 3 seconds
        const interval = setInterval(() => {
            if (!this.isActive) {
                clearInterval(interval);
                return;
            }
            
            for (let i = 0; i < 10; i++) {
                const piece = this.createPiece();
                this.container.appendChild(piece);
                this.pieces.push(piece);
            }
        }, 200);
        
        // Stop after 3 seconds
        setTimeout(() => {
            clearInterval(interval);
            this.stopAnimation();
        }, 3000);
        
        // Clean up pieces after animation completes
        setTimeout(() => {
            this.cleanup();
        }, 6000);
    }

    stopAnimation() {
        this.isActive = false;
    }

    cleanup() {
        this.pieces.forEach(piece => {
            if (piece.parentNode) {
                piece.parentNode.removeChild(piece);
            }
        });
        this.pieces = [];
    }

    destroy() {
        this.cleanup();
        if (this.container && this.container.parentNode) {
            this.container.parentNode.removeChild(this.container);
        }
    }
}

// Make Confetti available globally
window.Confetti = Confetti;

// CSS animation keyframes (fallback if not in CSS file)
if (!document.querySelector('#confetti-styles')) {
    const style = document.createElement('style');
    style.id = 'confetti-styles';
    style.textContent = `
        @keyframes confetti-fall {
            0% {
                transform: translateY(-100vh) rotate(0deg);
                opacity: 1;
            }
            100% {
                transform: translateY(100vh) rotate(720deg);
                opacity: 0;
            }
        }
    `;
    document.head.appendChild(style);
}
