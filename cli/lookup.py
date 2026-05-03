import argparse
import os
import re
import pandas as pd
import requests

API_BASE_URL = "http://127.0.0.1:5000"


def safe_filename(value):
    value = str(value).lower().strip()
    value = re.sub(r"[^a-z0-9]+", "_", value)
    return value.strip("_")


def print_table(df):
    if df.empty:
        print("Không tìm thấy dữ liệu.")
        return

    print(df.to_string(index=False))


def lookup(name=None, club=None):
    if name:
        response = requests.get(
            f"{API_BASE_URL}/api/player",
            params={"name": name},
            timeout=30,
        )
        output_file = f"player_{safe_filename(name)}.csv"
    else:
        response = requests.get(
            f"{API_BASE_URL}/api/club",
            params={"club": club},
            timeout=30,
        )
        output_file = f"club_{safe_filename(club)}.csv"

    response.raise_for_status()

    result = response.json()
    data = result.get("data", [])

    if not data:
        print("Không tìm thấy dữ liệu.")
        return

    df = pd.DataFrame(data)

    print_table(df)

    os.makedirs("data/processed", exist_ok=True)

    output_path = os.path.join("data", "processed", output_file)
    df.to_csv(output_path, index=False, encoding="utf-8-sig")

    print(f"\nĐã xuất CSV: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Tra cứu dữ liệu cầu thủ")

    parser.add_argument("--name", help="Tên cầu thủ")
    parser.add_argument("--club", help="Tên câu lạc bộ")

    args = parser.parse_args()

    if not args.name and not args.club:
        print("Vui lòng nhập --name hoặc --club")
        return

    lookup(name=args.name, club=args.club)


if __name__ == "__main__":
    main()