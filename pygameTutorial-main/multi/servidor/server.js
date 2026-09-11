const config = require('./config');
const WebSocketHandler = require('./network/WebSocketHandler');

const wsHandler = new WebSocketHandler();
wsHandler.init(config.PORT);