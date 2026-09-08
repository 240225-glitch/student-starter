"""ACIS Club Compass — Python matcher + tiny web server.

No Flask needed. Run this file, then open http://localhost:8000
HTML -> app.js -> POST /api/match -> matcher.py -> JSON results -> app.js -> HTML
"""

from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).parent
PORT = 8000


def load_clubs() -> list[dict]:
    """Load the club data from clubs.json."""
    return json.loads((ROOT / "clubs.json").read_text(encoding="utf-8"))


def score_club(club: dict, profile: dict) -> dict:
    """Give one club a score for one student profile."""
    matched = [item for item in profile["interests"] if item in club["interests"]]

    score = len(matched) * 5

    if profile["style"] in club["styles"]:
        score += 3
    if profile["day"] in club["days"]:
        score += 2
    if profile["grade_group"] in club["groups"]:
        score += 2

    reasons = []
    if matched:
        reasons.append("shared interests: " + ", ".join(matched[:3]))
    if profile["style"] in club["styles"]:
        reasons.append("fits how you like to " + profile["style"])
    if profile["day"] in club["days"]:
        reasons.append("meets on your preferred day")
    if not reasons:
        reasons.append("offers a new area to explore")

    return {**club, "score": score, "reasons": reasons}


def top_matches(clubs: list[dict], profile: dict, limit: int = 3) -> list[dict]:
    """Rank all clubs and return the best matches."""
    ranked = [score_club(club, profile) for club in clubs]
    ranked.sort(key=lambda item: (-item["score"], item["name"]))
    return ranked[:limit]


class ClubCompassServer(BaseHTTPRequestHandler):
    """Very small server for the classroom project."""

    def do_GET(self) -> None:
        path = unquote(self.path.split("?", 1)[0])
        if path == "/":
            path = "/index.html"

        safe_files = {
            "/index.html": "text/html; charset=utf-8",
            "/styles.css": "text/css; charset=utf-8",
            "/app.js": "application/javascript; charset=utf-8",
            "/clubs.json": "application/json; charset=utf-8",
        }

        if path not in safe_files:
            self.send_error(404, "File not found")
            return

        content = (ROOT / path.lstrip("/")).read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", safe_files[path])
        self.end_headers()
        self.wfile.write(content)

    def do_POST(self) -> None:
        if self.path != "/api/match":
            self.send_error(404, "API route not found")
            return

        length = int(self.headers.get("Content-Length", 0))
        raw_body = self.rfile.read(length).decode("utf-8")
        profile = json.loads(raw_body)

        result = {
            "profile": {
                "name": profile.get("name", "Student"),
                "grade": profile.get("grade"),
                "grade_group": profile.get("grade_group"),
                "house": profile.get("house"),
            },
            "checked_clubs": len(load_clubs()),
            "matches": top_matches(load_clubs(), profile),
        }

        body = json.dumps(result, ensure_ascii=False).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args) -> None:
        # Keep classroom output clean.
        return


def run_server() -> None:
    print("ACIS Club Compass is running")
    print(f"Open: http://localhost:{PORT}")
    print("Press Ctrl+C to stop the server.")
    server = ThreadingHTTPServer(("localhost", PORT), ClubCompassServer)
    server.serve_forever()


def demo() -> None:
    """Quick test without opening the website."""
    profile = {
        "name": "Mina",
        "grade": 10,
        "grade_group": "High School",
        "house": "Aqua",
        "day": "Wednesday",
        "style": "build",
        "interests": ["technology", "games", "problem-solving"],
    }
    for rank, club in enumerate(top_matches(load_clubs(), profile), start=1):
        print(f"{rank}. {club['symbol']} {club['name']} — {club['score']} points")


if __name__ == "__main__":
    run_server()
