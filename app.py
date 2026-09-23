from flask import Flask, render_template, request, jsonify, send_file
from crypto import encrypt_text, decrypt_text
import io


app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/encrypt", methods=["POST"])
def encrypt():
    try:
        data = request.get_json()

        text = data.get("text", "")
        password = data.get("password", "")

        if not text or not password:
            return jsonify({
                "success": False,
                "message": "Please enter text and password."
            }), 400

        result = encrypt_text(text, password)

        return jsonify({
            "success": True,
            "result": result
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


@app.route("/decrypt", methods=["POST"])
def decrypt():
    try:
        data = request.get_json()

        text = data.get("text", "")
        password = data.get("password", "")

        if not text or not password:
            return jsonify({
                "success": False,
                "message": "Please enter encrypted text and password."
            }), 400

        result = decrypt_text(text, password)

        return jsonify({
            "success": True,
            "result": result
        })

    except Exception:
        return jsonify({
            "success": False,
            "message": "Integrity verification failed. The password may be incorrect or the encrypted data may have been modified."
        }), 400


@app.route("/download", methods=["POST"])
def download():
    try:
        data = request.get_json()

        text = data.get("text", "")
        filename = data.get(
            "filename",
            "encrypted_text.enc"
        )

        if not text:
            return jsonify({
                "success": False,
                "message": "There is no result to save."
            }), 400

        allowed_filenames = [
            "encrypted_text.enc",
            "decrypted_text.txt"
        ]

        if filename not in allowed_filenames:
            filename = "encrypted_text.enc"

        file = io.BytesIO(
            text.encode("utf-8")
        )

        file.seek(0)

        return send_file(
            file,
            as_attachment=True,
            download_name=filename,
            mimetype="text/plain"
        )

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


if __name__ == "__main__":
    app.run(debug=True)