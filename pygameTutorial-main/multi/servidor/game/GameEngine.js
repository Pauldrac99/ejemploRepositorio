const config = require('../config');

class GameEngine {
    constructor() {
        this.W = 800;
        this.H = 500;
    }

    createInitialState() {
        return {
            ball: { x: this.W / 2, y: this.H / 2, vx: 0, vy: 0, radius: 8 },
            paddle1: { x: 22, y: this.H / 2 - 40, width: 14, height: 80 },
            paddle2: { x: this.W - 22 - 14, y: this.H / 2 - 40, width: 14, height: 80 },
            score: { p1: 0, p2: 0 },
            running: false,
            resetTimer: 0
        };
    }

    update(state, inputs) {
        // CORRECCIÓN 1: Devolver objeto, no solo el estado
        if (!state.running) return { state, event: null };
        
        if (state.ball.vx === 0 && state.ball.vy === 0 && state.resetTimer <= 0) {
            this.launchBall(state);
        }

        const speed = 6;
        if (inputs[1].up) state.paddle1.y -= speed;
        if (inputs[1].down) state.paddle1.y += speed;
        if (inputs[2].up) state.paddle2.y -= speed;
        if (inputs[2].down) state.paddle2.y += speed;

        state.paddle1.y = Math.max(0, Math.min(this.H - state.paddle1.height, state.paddle1.y));
        state.paddle2.y = Math.max(0, Math.min(this.H - state.paddle2.height, state.paddle2.y));

        if (state.resetTimer > 0) {
            state.resetTimer--;
            if (state.resetTimer === 0) this.launchBall(state);
            // CORRECCIÓN 2: Devolver objeto, no solo el estado
            return { state, event: null };
        }

        state.ball.x += state.ball.vx;
        state.ball.y += state.ball.vy;

        if (state.ball.y - state.ball.radius <= 0 || state.ball.y + state.ball.radius >= this.H) {
            state.ball.vy *= -1;
            return { state, event: 'wall' };
        }

        if (this.checkPaddleHit(state.ball, state.paddle1, 1)) return { state, event: 'paddle', side: 1 };
        if (this.checkPaddleHit(state.ball, state.paddle2, -1)) return { state, event: 'paddle', side: 2 };

        if (state.ball.x < -30) return this.handleScore(state, 2);
        if (state.ball.x > this.W + 30) return this.handleScore(state, 1);

        return { state, event: null };
    }

    checkPaddleHit(ball, paddle, dir) {
        return ball.vx * dir < 0 &&
               ball.x - ball.radius <= paddle.x + paddle.width &&
               ball.x + ball.radius >= paddle.x &&
               ball.y >= paddle.y && ball.y <= paddle.y + paddle.height;
    }

    handleScore(state, player) {
        state.score['p' + player]++;
        if (state.score['p' + player] >= config.WIN_SCORE) {
            state.running = false;
            return { state, event: 'gameover', winner: player };
        }
        this.resetBall(state);
        return { state, event: 'scored', player };
    }

    resetBall(state) {
        state.ball.x = this.W / 2;
        state.ball.y = this.H / 2;
        state.ball.vx = 0; state.ball.vy = 0;
        state.resetTimer = 50;
    }

    launchBall(state) {
        const dir = Math.random() > 0.5 ? 1 : -1;
        state.ball.vx = dir * 5;
        state.ball.vy = (Math.random() - 0.5) * 4;
    }

    applyPaddlePhysics(state, paddle, dir) {
        const ball = state.ball;
        let hitPos = (ball.y - (paddle.y + paddle.height / 2)) / (paddle.height / 2);
        hitPos = Math.max(-1, Math.min(1, hitPos));
        let speed = Math.sqrt(ball.vx * ball.vx + ball.vy * ball.vy);
        speed = Math.min(speed * 1.05, 12);
        const angle = hitPos * (Math.PI / 3);
        ball.vx = Math.cos(angle) * speed * dir;
        ball.vy = Math.sin(angle) * speed;
        ball.x = dir > 0 ? paddle.x + paddle.width + ball.radius + 1 : paddle.x - ball.radius - 1;
    }
}

module.exports = GameEngine;