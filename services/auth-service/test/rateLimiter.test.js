const express = require('express');
const request = require('supertest');
const { createRateLimiter } = require('../src/middleware/rateLimiter');

describe('Authentication rate limiter', () => {
  it('allows 10 requests per 15 minutes and rejects the 11th', async () => {
    const app = express();
    app.post('/auth/login', createRateLimiter(), (_req, res) => res.sendStatus(200));

    for (let attempt = 0; attempt < 10; attempt += 1) {
      const response = await request(app).post('/auth/login');
      expect(response.statusCode).toBe(200);
    }

    const limitedResponse = await request(app).post('/auth/login');
    expect(limitedResponse.statusCode).toBe(429);
    expect(limitedResponse.body).toEqual({
      error: 'Too many attempts, please try again later'
    });
  });
});
