
const express = require("express");
const QRCode = require("qrcode");

const app = express();
const PORT = 3000;

app.use(express.json());
app.use(express.urlencoded({ extended: true }));

const HTML = `
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>QR Code Generator</title>
</head>
<body>
    <h1>📱 QR Code Generator</h1>

    <p>Введите текст для генерации QR-кода</p>

    <form action="/generate" method="POST">
        <input type="text" name="text" required>
        <button type="submit">Генерировать QR</button>
    </form>
</body>
</html>
`;

app.get("/", (req, res) => {
    res.send(HTML);
});

app.post("/generate", async (req, res) => {
    const text = req.body.text;

    try {
        const qrCode = await QRCode.toDataURL(text);

        res.send(`
            <!DOCTYPE html>
            <html lang="ru">
            <head>
                <meta charset="UTF-8">
                <title>QR-код</title>
            </head>
            <body>
                <h1>Ваш QR-код</h1>

                <img src="${qrCode}" alt="QR-код">

                <br><br>

                <a href="${qrCode}" download="qrcode.png">
                    Скачать QR-код
                </a>

                <br><br>

                <a href="/">Создать новый QR-код</a>
            </body>
            </html>
        `);
    } catch (err) {
        res.status(500).send("Ошибка генерации QR-кода");
    }
});

app.listen(PORT, () => {
    console.log(`Сервер запущен на http://localhost:${PORT}`);
});


