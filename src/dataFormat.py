from dataclasses import dataclass

@dataclass

class DataSnap:
    fps: float
    time: float
    date: str

    plyrName: str
    plyrLocation: list[float]
    plyrHealth: int
    plyrInventory: list[int]
    plyrStatus: list[int]
    plyrHunger: int
    plyrSat: int

    