# main.py — FastAPI app, routes, startup

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

from jd_parser import parse_jd
from ranker import rank_candidates
from data.candidates import CANDIDATES

app = FastAPI(title="Talent Scout Agent", version="1.0.0")

# CORS for local dev — allow everything on localhost
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# serve static files (the frontend)
app.mount("/static", StaticFiles(directory="static"), name="static")


class JDRequest(BaseModel):
    jd_text: str


@app.get("/")
def serve_frontend():
    return FileResponse("static/index.html")


@app.post("/analyze")
def analyze_jd(req: JDRequest):
    parsed = parse_jd(req.jd_text)
    ranked = rank_candidates(CANDIDATES, parsed)
    return {"parsed_jd": parsed, "ranked_candidates": ranked}


@app.get("/candidates")
def list_candidates():
    return {"candidates": CANDIDATES}
