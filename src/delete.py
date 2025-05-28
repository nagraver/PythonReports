import argparse
from itertools import groupby
from operator import itemgetter
from typing import List


def print_payout(data: List) -> None:   
    data.sort(key=itemgetter("department"))

    print(f"{'':<15} {'Name':<15} {'Hours':<6} {'Rate':<6} {'Total':<7}")
    print("-" * 55)

    for dept, items in groupby(data, key=itemgetter("department")):
        print(dept)
        d_hours, d_total = 0, 0
        for item in items:
            name = item.get("name", "")
            rate = int(item.get("rate", 0))
            hours = int(item.get("hours", 0))
            total = rate * hours
            print(f"{'':-<15} {name:<15} {hours:<6} {rate:<6} ${total:<7}")
            d_hours += hours
            d_total += total
        print(f"{'':-<15} {'Total':<15} {d_hours:<6} {'':<6} ${d_total:<7}")
        print()


def normalize_field(field: str) -> str:
    normalized = field.strip().lower()
    for key, aliases in FIELD_ALIASES.items():
        if normalized in aliases:
            return key
    return normalized


def load_data(files: List[str]) -> List:
    data = []
    for file in files:
        try:
            with open(file, "r", encoding="utf-8") as f:
                lines = f.readlines()
                if not lines:
                    print(f"Warning: File '{file}' is empty.")
                    continue

                raw_header = lines[0].strip().split(",")
                header = [normalize_field(item) for item in raw_header]

                for line in lines[1:]:
                    raw_data = line.strip().split(",")
                    if len(raw_data) != len(header):
                        print(f"Warning: Skipping malformed line in file '{file}': {line.strip()}")
                        continue
                    data.append(dict(zip(header, raw_data)))
        except FileNotFoundError:
            print(f"Error: File '{file}' not found.")
        except Exception as e:
            print(f"Error reading file '{file}': {e}")
    return data


FIELD_ALIASES = {
    "name": {"name"},
    "department": {"department"},
    "email": {"email"},
    "id": {"id"},
    "hours": {"hours_worked", "hours"},
    "rate": {"salary", "rate", "hourly_rate"},
}


REPORTS = {"payout": print_payout}


def main() -> None:
    parser = argparse.ArgumentParser(description="Process employee data and generate reports.")
    parser.add_argument("--report", required=True, choices=REPORTS.keys(), help="Type of report to generate.")
    parser.add_argument("files", nargs="+", help="CSV files with employee data.")
    args = parser.parse_args()

    data = load_data(args.files)
    if not data:
        print("No valid data to process. Exiting.")
        return

    report_function = REPORTS.get(args.report)
    if report_function:
        report_function(data)
    else:
        print(f"Report type '{args.report}' is not supported.")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
