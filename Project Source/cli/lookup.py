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


def call_api(endpoint, params):
    try:
        response = requests.get(
            f"{API_BASE_URL}{endpoint}",
            params=params,
            timeout=30,
        )

        response.raise_for_status()
        return response.json()

    except requests.exceptions.HTTPError:
        print("API lỗi:")
        print("Status:", response.status_code)
        print("Response:", response.text)
        return None

    except requests.exceptions.ConnectionError:
        print("Không kết nối được API.")
        print("Hãy chạy server trước:")
        print("python -m api.app")
        return None

    except requests.exceptions.Timeout:
        print("API phản hồi quá lâu.")
        return None


def lookup(name=None, club=None):
    if name:
        result = call_api("/api/player", {"name": name})
        output_file = f"player_{safe_filename(name)}.csv"
    else:
        result = call_api("/api/club", {"club": club})
        output_file = f"club_{safe_filename(club)}.csv"

    if result is None:
        return

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

    if args.name and args.club:
        print("Chỉ nhập một trong hai: --name hoặc --club")
        return

    lookup(name=args.name, club=args.club)


if __name__ == "__main__":
    main()