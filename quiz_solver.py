#!/usr/bin/env python3
"""
quiz_solver.py  (API-ONLY VERSION)

Usage:
    python quiz_solver.py sample_payload.json

Payload JSON must contain:
{
    "email": "...",
    "secret": "...",
    "url": "http://localhost:8080/api/quiz"
}
"""

import sys
import json
import os
import time
import requests


def log(*args):
    print("[solver]", *args)


def load_payload(path):
    """Load JSON payload file."""
    with open(path, "r") as f:
        return json.load(f)


def solve_quiz_api(payload):
    """
    Sends the payload directly to the API.
    No HTML, no Playwright, no parsing.
    """
    endpoint = payload["url"]

    data = {
        "email": payload["email"],
        "secret": payload["secret"],
        "url": payload["url"]
    }

    log("Sending payload to API:", endpoint)

    try:
        resp = requests.post(endpoint, json=data, timeout=30)
        resp.raise_for_status()
        json_resp = resp.json()
        log("API responded:", json_resp)
        return json_resp
    except Exception as e:
        log("API error:", e)
        return None


def main(payload_path):
    payload = load_payload(payload_path)

    email = payload.get("email")
    secret = payload.get("secret")
    url = payload.get("url")

    if not (email and secret and url):
        log("Payload missing required fields (email, secret, url). Exiting.")
        return 1

    start_time = time.time()

    # ---- API SOLVE ----
    result = solve_quiz_api(payload)

    # ---- LOGGING SECTION ----
    try:
        os.makedirs("logs", exist_ok=True)
        safe_email = email.replace("@", "_").replace(".", "_")
        log_path = f"logs/{safe_email}.json"

        with open(log_path, "w") as f:
            json.dump({
                "input": payload,
                "result": result
            }, f, indent=2)

        log("Saved log to:", log_path)

    except Exception as e:
        log("Error writing log file:", e)

    return 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python quiz_solver.py path/to/payload.json")
        sys.exit(2)

    payload_file = sys.argv[1]
    sys.exit(main(payload_file))
