require('dotenv').config();

module.exports = {
    PORT: process.env.PORT || 3000,
    TICK_RATE: parseInt(process.env.TICK_RATE) || 60,
    WIN_SCORE: parseInt(process.env.WIN_SCORE) || 7
};
