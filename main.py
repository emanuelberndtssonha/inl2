from linked_list import LinkedList
from storage import save_month_to_file, load_month_from_file
from calendar_view import run_calendar_app

START_YEAR = 2026
END_YEAR = 2035
TOTAL_MONTHS = (END_YEAR - START_YEAR + 1) * 12

def get_month_index(year: int, month: int) -> int:
    return (year - START_YEAR) * 12 + (month - 1)

def initialize_diary() -> list[LinkedList]:
    diary = []
    for index in range(TOTAL_MONTHS):
        year = START_YEAR + (index // 12)
        month = (index % 12) + 1
        linked_list = load_month_from_file(year, month)
        diary.append(linked_list)
    return diary

def main():
    diary = initialize_diary()
    run_calendar_app(
        diary,
        START_YEAR,
        END_YEAR,
        get_month_index,
        save_month_to_file
    )

if __name__ == "__main__":
    main()