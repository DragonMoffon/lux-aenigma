from typing import TypedDict
from lux.data import get_config

ConstsDict = TypedDict(
    "ConstsDict",
    {
        "PLAYER_SPEED": float,
        "LEVEL_TRANSITION_SPEED": float,
        "DEBUG_POINT_RADIUS": int
    }
)

CONSTS: ConstsDict = get_config("consts").unwrap()
