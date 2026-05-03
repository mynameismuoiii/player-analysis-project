import time
import requests


def get_with_retry(url, headers=None, retries=3, sleep_seconds=3, timeout=20):
    for attempt in range(1, retries + 1):
        try:
            response = requests.get(url, headers=headers, timeout=timeout)

            if response.status_code == 200:
                return response

            print(f"Attempt {attempt}: status={response.status_code}")

        except requests.RequestException as e:
            print(f"Attempt {attempt}: {e}")

        time.sleep(sleep_seconds)

    return None