const rateLimit = require("express-rate-limit");

function createRateLimiter() {
  return rateLimit({
    windowMs: 15 * 60 * 1000,
    max: 10,
    standardHeaders: true,
    legacyHeaders: false,
    message: { error: "Too many attempts, please try again later" }
  });
}

const rateLimiter = createRateLimiter();

module.exports = { createRateLimiter, rateLimiter };
