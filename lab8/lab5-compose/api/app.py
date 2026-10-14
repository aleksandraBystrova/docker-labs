from flask import Flask, jsonify, request
import psycopg2
import redis
import os
import json

app = Flask(__name__)

# Конфигурация из env vars
from config import Config

DB_CONFIG = Config.DB_CONFIG

redis_client = redis.Redis(
    host=Config.REDIS_HOST,
    port=Config.REDIS_PORT,
    decode_responses=True
)


@app.route("/")
def home():
    return jsonify({
        "app": "Lab5 API",
        "status": "running"
    })


@app.route("/health")
def health():
    return jsonify({
        "status": "healthy"
    })


@app.route("/db-test")
def db_test():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        cur.execute("SELECT version();")
        version = cur.fetchone()[0]

        cur.close()
        conn.close()

        return jsonify({
            "status": "success",
            "database": version
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500


@app.route("/cache-test")
def cache_test():
    try:
        redis_client.set("test_key", "test_value", ex=60)
        value = redis_client.get("test_key")

        return jsonify({
            "status": "success",
            "redis": "connected",
            "test_value": value
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500
@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()

    if not data or not data.get("name") or not data.get("email"):
        return jsonify({
            "status": "error",
            "message": "Name and email are required"
        }), 400

    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL
            )
        """)

        cur.execute(
            "INSERT INTO users (name, email) VALUES (%s, %s) RETURNING id",
            (data["name"], data["email"])
        )

        user_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()

        return jsonify({
            "status": "success",
            "user": {
                "id": user_id,
                "name": data["name"],
                "email": data["email"]
            }
        }), 201

    except psycopg2.IntegrityError:
        conn.rollback()
        conn.close()
        return jsonify({
            "status": "error",
            "message": "This email already exists"
        }), 409

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route("/users", methods=["GET"])
def get_users():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        cur.execute("SELECT id, name, email FROM users ORDER BY id")
        rows = cur.fetchall()

        cur.close()
        conn.close()

        users = [
            {"id": row[0], "name": row[1], "email": row[2]}
            for row in rows
        ]

        return jsonify({
            "status": "success",
            "users": users
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

