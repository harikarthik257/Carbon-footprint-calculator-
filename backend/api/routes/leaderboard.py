from fastapi import APIRouter
from data.seed_leaderboard import SEED_LEADERBOARD

router = APIRouter()


@router.get("/leaderboard")
def leaderboard():
    return SEED_LEADERBOARD
