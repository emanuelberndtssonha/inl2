from dataclasses import dataclass
from datetime import date
from typing import Optional

@dataclass
class Duration:
    hours: int
    minutes: int
    seconds: int

    def __str__(self) -> str:
        return f"{self.hours:02d}:{self.minutes:02d}:{self.seconds:02d}"

@dataclass
class Session:
    description: str
    session_date: date
    distance: float
    duration: Duration

    def __str__(self) -> str:
        return (f"[{self.session_date}] {self.description} | "
                f"Sträcka: {self.distance:.2f} km | Tid: {self.duration}")

@dataclass
class Node:
    data: Session
    next: Optional['Node'] = None