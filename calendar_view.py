import os
import sys
import calendar
from datetime import date
from linked_list import LinkedList
from models import Session, Duration

MONTH_NAMES = [
    "", "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_key() -> str:
    import msvcrt
    key = msvcrt.getch()
    if key in (b'\x00', b'\xe0'):
        key2 = msvcrt.getch()
        mapping = {
            b'H': 'UP', b'P': 'DOWN', b'K': 'LEFT', b'M': 'RIGHT',
            b'I': 'PGUP', b'Q': 'PGDN', b'7': 'HOME', b'O': 'END'
        }
        return mapping.get(key2, '')
    elif key in (b'\r', b'\n'):
        return 'ENTER'
    elif key in (b'q', b'Q'):
        return 'Q'
    return key.decode('utf-8', errors='ignore').lower()

def render_calendar(year: int, month: int, selected_day: int):
    clear_screen()
    print(f"{MONTH_NAMES[month]} {year}")
    print("Mo Tu We Th Fr Sa Su")

    cal = calendar.Calendar(firstweekday=0)
    weeks = cal.monthdayscalendar(year, month)

    for week in weeks:
        line = ""
        for day in week:
            if day == 0:
                line += "   "
            elif day == selected_day:
                line += f"[{day:2d}]"
            else:
                line += f" {day:2d} "
            line += " "
        print(line.rstrip())

    print()
    print("<= => to navigate between days.")
    print("Page Up/Page Down to navigate between months.")
    print("Home/End to go to the first/last day of the month.")
    print("Enter to show, add or edit sessions for the selected day.")
    print("Q to exit the program.")

def handle_day_menu(diary: list[LinkedList], year: int, month: int, day: int,
                    get_month_idx, save_fn):
    #clear_screen()
    target_date = date(year, month, day)
    idx = get_month_idx(year, month)

    while True:
        print(f"=== Träningspass för {target_date} ===")
        sessions = diary[idx].get_sessions_by_date(target_date)

        if not sessions:
            print("Inga träningspass registrerade denna dag.")
        else:
            for i, s in enumerate(sessions, 1):
                print(f"  [{i}] {s}")

        print("\n1. Lägg till nytt träningspass")
        print("2. Ta bort ett träningspass")
        print("3. Redigera ett träningspass")
        print("4. Tillbaka till kalendern")

        choice = input("\nVälj alternativ (1-4): ").strip()

        if choice == "1":
            try:
                desc = input("Beskrivning: ")
                dist = float(input("Sträcka (km): "))
                h = int(input("Timmar: "))
                m = int(input("Minuter: "))
                s = int(input("Sekunder: "))

                new_session = Session(
                    description=desc,
                    session_date=target_date,
                    distance=dist,
                    duration=Duration(h, m, s)
                )
                diary[idx].insert_sorted(new_session)
                save_fn(year, month, diary[idx])
                print(">> Träningspass tillagt och sparat!")
            except ValueError:
                print(">> Felaktig inmatning.")

        elif choice == "2":
            all_month_sessions = diary[idx].to_list()
            day_indices = [
                i for i, s in enumerate(all_month_sessions)
                if s.session_date == target_date
            ]
            if not day_indices:
                print(">> Inga pass finns att ta bort.")
                continue

            try:
                sub_idx = int(input("Ange nummer på passet som ska tas bort: ")) - 1
                if 0 <= sub_idx < len(day_indices):
                    global_idx = day_indices[sub_idx]
                    diary[idx].delete_by_index(global_idx)
                    save_fn(year, month, diary[idx])
                    print(">> Träningspass borttaget!")
                else:
                    print(">> Ogiltigt nummer.")
            except ValueError:
                print(">> Ogiltig inmatning.")
        elif choice == "3":
            all_month_sessions = diary[idx].to_list()
            day_indices = [
                i for i, s in enumerate(all_month_sessions)
                if s.session_date == target_date
            ]
            if not day_indices:
                print(">> Inga pass finns att redigera.")
                continue

            try:
                sub_idx = int(input("Ange nummer på passet som ska redigeras: ")) - 1
                if 0 <= sub_idx < len(day_indices):
                    global_idx = day_indices[sub_idx]
                    session_to_edit = all_month_sessions[global_idx]

                    print(f"Redigerar: {session_to_edit}")
                    new_desc = input(f"Ny beskrivning (nuvarande: {session_to_edit.description}): ") or session_to_edit.description
                    new_dist = input(f"Ny sträcka (nuvarande: {session_to_edit.distance} km): ")
                    new_h = input(f"Nya timmar (nuvarande: {session_to_edit.duration.hours}): ")
                    new_m = input(f"Nya minuter (nuvarande: {session_to_edit.duration.minutes}): ")
                    new_s = input(f"Nya sekunder (nuvarande: {session_to_edit.duration.seconds}): ")

                    session_to_edit.description = new_desc
                    if new_dist:
                        session_to_edit.distance = float(new_dist)
                    if new_h:
                        session_to_edit.duration.hours = int(new_h)
                    if new_m:
                        session_to_edit.duration.minutes = int(new_m)
                    if new_s:
                        session_to_edit.duration.seconds = int(new_s)

                    save_fn(year, month, diary[idx])
                    print(">> Träningspass uppdaterat!")
                else:
                    print(">> Ogiltigt nummer.")
            except ValueError:
                print(">> Ogiltig inmatning.")

        elif choice == "4":
            break

def run_calendar_app(diary: list[LinkedList], start_year: int, end_year: int,
                     get_month_idx, save_fn):
    current_year = 2026
    current_month = 8
    current_day = 28

    while True:
        max_days = calendar.monthrange(current_year, current_month)[1]
        current_day = min(current_day, max_days)

        render_calendar(current_year, current_month, current_day)
        key = get_key()

        if key == 'Q':
            clear_screen()
            print("Programmet avslutas.")
            break

        elif key == 'LEFT':
            if current_day > 1:
                current_day -= 1
            elif current_month > 1:
                current_month -= 1
                current_day = calendar.monthrange(current_year, current_month)[1]
            elif current_year > start_year:
                current_year -= 1
                current_month = 12
                current_day = 31

        elif key == 'RIGHT':
            if current_day < max_days:
                current_day += 1
            elif current_month < 12:
                current_month += 1
                current_day = 1
            elif current_year < end_year:
                current_year += 1
                current_month = 1
                current_day = 1

        elif key == 'UP':
            if current_day - 7 >= 1:
                current_day -= 7

        elif key == 'DOWN':
            if current_day + 7 <= max_days:
                current_day += 7

        elif key == 'PGUP':
            if current_month > 1:
                current_month -= 1
            elif current_year > start_year:
                current_year -= 1
                current_month = 12

        elif key == 'PGDN':
            if current_month < 12:
                current_month += 1
            elif current_year < end_year:
                current_year += 1
                current_month = 1

        elif key == 'HOME':
            current_day = 1

        elif key == 'END':
            current_day = max_days

        elif key == 'ENTER':
            handle_day_menu(diary, current_year, current_month, current_day,
                            get_month_idx, save_fn)