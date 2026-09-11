const WebSocket = require('ws');
const RoomManager = require('../game/RoomManager');
const Protocol = require('../utils/protocol');

class WebSocketHandler {
    constructor() {
        this.roomManager = new RoomManager();
        this.wss = null;
    }

    init(port) {
        // ¡Sin HTTP! Servidor WebSocket puro.
        this.wss = new WebSocket.Server({ port });
        
        this.wss.on('connection', (ws) => {
            ws.roomId = null;
            ws.playerNum = 0;

            ws.on('message', (raw) => this.handleMessage(ws, JSON.parse(raw)));
            ws.on('close', () => this.handleDisconnect(ws));
        });

        console.log(`Servidor WebSocket puro escuchando en ws://localhost:${port}`);
    }

    handleMessage(ws, msg) {
        switch (msg.type) {
            case Protocol.CREATE:
                const id = this.roomManager.createRoom(ws);
                ws.roomId = id; ws.playerNum = 1;
                // CORRECCIÓN: Cambiado de Protocol.CREATE a 'created'
                this.send(ws, { type: 'created', roomId: id });
                break;

            case Protocol.JOIN:
                if (this.roomManager.joinRoom(msg.roomId, ws)) {
                    ws.roomId = msg.roomId; ws.playerNum = 2;
                    // CORRECCIÓN: Cambiado de Protocol.JOIN a 'joined'
                    this.send(ws, { type: 'joined', roomId: msg.roomId });
                    const room = this.roomManager.rooms[msg.roomId];
                    this.send(room.players[0], { type: Protocol.OPPONENT_JOINED });
                    this.startCountdown(msg.roomId);
                } else {
                    this.send(ws, { type: Protocol.ERROR, message: 'Sala llena o inexistente' });
                }
                break;

            case Protocol.INPUT:
                const r = this.roomManager.rooms[ws.roomId];
                if (r) r.inputs[ws.playerNum][msg.key] = !!msg.pressed;
                break;
        }
    }

    startCountdown(roomId) {
        const steps = [3, 2, 1, 'GO'];
        steps.forEach((val, i) => {
            setTimeout(() => {
                const room = this.roomManager.rooms[roomId];
                if (!room) return;
                this.broadcast(room, { type: Protocol.COUNTDOWN, value: val });
                if (val === 'GO') {
                    room.gameState.running = true;
                    this.roomManager.startGameLoop(roomId, (r, result) => {
                        this.broadcast(r, { type: Protocol.STATE, state: r.gameState });
                        if (result.event === 'wall') this.broadcast(r, { type: Protocol.SOUND, name: 'wall' });
                        if (result.event === 'paddle') this.broadcast(r, { type: Protocol.SOUND, name: 'paddle' });
                        if (result.event === 'scored') {
                            this.broadcast(r, { type: Protocol.SCORED, player: result.player });
                            this.broadcast(r, { type: Protocol.SOUND, name: 'score' });
                        }
                        if (result.event === 'gameover') {
                            this.broadcast(r, { type: Protocol.GAMEOVER, winner: result.winner });
                            this.roomManager.stopGameLoop(roomId);
                        }
                    });
                }
            }, (i + 1) * 800);
        });
    }

    handleDisconnect(ws) {
        if (ws.roomId && this.roomManager.rooms[ws.roomId]) {
            const room = this.roomManager.rooms[ws.roomId];
            const otherIdx = ws.playerNum === 1 ? 1 : 0;
            if (room.players[otherIdx]?.readyState === 1) {
                this.send(room.players[otherIdx], { type: 'opponentLeft' });
            }
            this.roomManager.destroyRoom(ws.roomId);
        }
    }

    send(ws, data) { if (ws.readyState === 1) ws.send(JSON.stringify(data)); }

    broadcast(room, data) {
        const msg = JSON.stringify(data);
        room.players.forEach(p => { if (p?.readyState === 1) p.send(msg); });
    }
}

// CORRECCIÓN PREVIA: Exportar la clase para que server.js pueda usarla
module.exports = WebSocketHandler;