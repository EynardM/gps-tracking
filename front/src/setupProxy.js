const { createProxyMiddleware } = require('http-proxy-middleware');

module.exports = function(app) {
  app.use(
    '/ws',
    createProxyMiddleware({
      target: 'ws://localhost:8000',  // Adresse de votre serveur FastAPI
      changeOrigin: true,
      ws: true,
    })
  );
};
