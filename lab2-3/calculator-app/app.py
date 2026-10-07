from flask import Flask, render_template_string, request

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Калькулятор</title>
</head>
<body>
    <h1>🧮 Калькулятор</h1>

    <form method="POST">
        <input type="number" name="num1" step="any" required>

        <select name="operation">
            <option value="add">+</option>
            <option value="subtract">-</option>
            <option value="multiply">×</option>
            <option value="divide">÷</option>
        </select>

        <input type="number" name="num2" step="any" required>

        <button type="submit">Вычислить</button>
    </form>

    {% if result is not none %}
        <h2>Результат: {{ result }}</h2>
    {% endif %}
</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def calculator():
    result = None

    if request.method == "POST":
        num1 = float(request.form["num1"])
        num2 = float(request.form["num2"])
        operation = request.form["operation"]

        if operation == "add":
            result = num1 + num2

        elif operation == "subtract":
            result = num1 - num2

        elif operation == "multiply":
            result = num1 * num2

        elif operation == "divide":
            result = num1 / num2 if num2 != 0 else "Ошибка: деление на 0"

    return render_template_string(HTML, result=result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


