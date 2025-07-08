from fastapi import FastAPI, Request
from pydantic import BaseModel
import aiofiles
import json
from datetime import datetime

app = FastAPI()


class AnswerSubmission(BaseModel):
    answers: dict
    studentId: str


class ScoreSubmission(BaseModel):
    studentId: str
    score: int


# 📝 Save answers asynchronously
@router.post("/submit")
async def submit_answers(payload: AnswerSubmission):
    record = {
        "timestamp": datetime.utcnow().isoformat(),
        "studentId": payload.studentId,
        "answers": payload.answers
    }

    async with aiofiles.open("answers.jsonl", mode="a") as f:
        await f.write(json.dumps(record) + "\n")

    return {"message": "Answers submitted successfully"}


# 📝 Save score asynchronously
@router.post("/api/submit-scores")
async def submit_score(payload: ScoreSubmission):
    record = {
        "timestamp": datetime.utcnow().isoformat(),
        "studentId": payload.studentId,
        "score": payload.score
    }

    async with aiofiles.open("scores.jsonl", mode="a") as f:
        await f.write(json.dumps(record) + "\n")

    return {"message": "Score submitted successfully"}
