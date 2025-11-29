from flask import Flask, request, jsonify
import os, json, threading, subprocess, sys, shlex, tempfile

app = Flask(__name__)

EXPECTED_SECRET = os.environ.get("QUIZ_SECRET", "CHANGE_THIS_SECRET")

def run_quiz_solver(payload):
    """Runs quiz solver as a subprocess with timeout."""
    
    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as f:
        json.dump(payload, f)
        tmpfile = f.name

    cmd = f"{sys.executable} quiz_solver.py {shlex.quote(tmpfile)}"

    try:
        subprocess.run(cmd, shell=True, timeout=160, check=True)
    except subprocess.TimeoutExpired:
        print("❌ Solver timed out")
    except subprocess.CalledProcessError as e:
        print("❌ Solver error:", e)
    finally:
        try:
            os.remove(tmpfile)
        except:
            pass


@app.route("/api/quiz", methods=["POST"])
def quiz_handler():
    # Validate JSON
    try:
        payload = request.get_json(force=True)
    except:
        return jsonify({"error": "Invalid JSON"}), 400

    # Validate secret
    if payload.get("secret") != EXPECTED_SECRET:
        return jsonify({"error": "Invalid secret"}), 403

    # Extract required fields
    if "email" not in payload or "url" not in payload:
        return jsonify({"error": "Missing fields"}), 400

    # Accepted
    response = {
        "status": "accepted",
        "email": payload["email"]
    }

    # Start worker thread
    t = threading.Thread(target=run_quiz_solver, args=(payload,), daemon=True)
    t.start()

    return jsonify(response), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
