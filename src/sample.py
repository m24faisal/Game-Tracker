from dataclasses import dataclass

@dataclass

class dataSnap:
    fps: float
    plyrHealth: int
    plyrInventory: list[int]
    plyrStatus: list[int]
    plyrHunger: int
    plyrSat: int
    