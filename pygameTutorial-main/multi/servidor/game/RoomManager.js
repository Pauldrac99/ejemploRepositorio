const crypto = require('crypto');
const GameEngine = require('./GameEngine');

class RoomManager {
    constructor() {
        this.rooms = {};
        this.engine = new GameEngine();
    }

    createRoom(hostSocket) {
        let id = crypto.randomBytes(2).toString('hex').toUpperCase();
        while (this.rooms[id]) id = crypto.randomBytes(2).toString('hex').toUpperCase();
        this.rooms[id] = {
            id, players: [hostSocket, null],
            gameState: this.engine.createInitialState(),
            inputs: { 1: {up:false, down:false}, 2: {up:false, down:false} },
            rematch: { 1: false, 2: false }, loopInterval: null
        };
        return id;
    }

    joinRoom(roomId, guestSocket) {
        const room = this.rooms[roomId];
        if (!room || room.players[1] !== null) return false;
        room.players[1] = guestSocket;
        return true;
    }

    resetRoom(roomId) {
        const room = this.rooms[roomId]; if(!room) return;
        room.gameState = this.engine.createInitialState();
        room.inputs = { 1: {up:false, down:false}, 2: {up:false, down:false} };
        room.rematch = { 1: false, 2: false };
    }

    destroyRoom(roomId) {
        if (this.rooms[roomId]?.loopInterval) clearInterval(this.rooms[roomId].loopInterval);
        delete this.rooms[roomId];
    }

    startGameLoop(roomId, onTick) {
        const config = require('../config');
        const room = this.rooms[roomId]; if (room.loopInterval) return;
        room.loopInterval = setInterval(() => {
            if (!this.rooms[roomId]) return clearInterval(room.loopInterval);
            const result = this.engine.update(room.gameState, room.inputs);
            room.gameState = result.state;
            if (result.event === 'paddle') this.engine.applyPaddlePhysics(room.gameState, room.gameState['paddle'+result.side], result.side === 1 ? 1 : -1);
            onTick(room, result);
        }, 1000 / config.TICK_RATE);
    }

    stopGameLoop(roomId) {
        if (this.rooms[roomId]?.loopInterval) clearInterval(this.rooms[roomId].loopInterval);
    }
}
module.exports = RoomManager;