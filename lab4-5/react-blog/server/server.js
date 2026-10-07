const express = require("express");
const path = require("path");

const app = express();
const PORT = 3000;

// Раздавать статику React
app.use(express.static(path.join(__dirname, "build")));

// Проверка сервера
app.get("/api/health", (req, res) => {
  res.json({
    status: "ok",
    message: "Server is running",
  });
});

// Все остальные запросы -> React
app.get("/{*splat}", (req, res) => {
  res.sendFile(path.join(__dirname, "build", "index.html"));
});

app.listen(PORT, "0.0.0.0", () => {
  console.log(`Server running on port ${PORT}`);
});

