import json
import os
from datetime import datetime
from models import Session, Duration
from linked_list import LinkedList

DATA_DIR = "träningsdata"

def ensure_data_dir_exists() -> None:
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

def get_filename(year: int, month: int) -> str:
    ensure_data_dir_exists()
    return f"{DATA_DIR}/sessions_{year}_{month:02d}.json"

def save_month_to_file(year: int, month: int, linked_list: LinkedList) -> None:
    filename = get_filename(year, month)
    sessions = linked_list.to_list()
    
    data = []
    for s in sessions:
        data.append({
            "description": s.description,
            "date": s.session_date.strftime("%Y-%m-%d"),
            "distance": s.distance,
            "duration": {
                "hours": s.duration.hours,
                "minutes": s.duration.minutes,
                "seconds": s.duration.seconds
            }
        })
    
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def load_month_from_file(year: int, month: int) -> LinkedList:
    linked_list = LinkedList()
    filename = get_filename(year, month)

    if not os.path.exists(filename):
        return linked_list

    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
            for item in data:
                d_parts = [int(x) for x in item["date"].split("-")]
                session_date = datetime(d_parts[0], d_parts[1], d_parts[2]).date()
                duration = Duration(**item["duration"])
                
                session = Session(
                    description=item["description"],
                    session_date=session_date,
                    distance=float(item["distance"]),
                    duration=duration
                )
                linked_list.insert_sorted(session)
    except Exception as e:
        print(f"Fel vid inläsning av {filename}: {e}")

    return linked_list