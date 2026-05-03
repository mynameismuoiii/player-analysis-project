import random
import time

import requests


def request_with_retry(
    url: str,
    headers: dict,
    max_retries: int = 3,
    timeout: int = 30,
    min_sleep: float = 3,
    max_sleep: float = 7,
) -> str:
    last_error = None

    for attempt in range(1, max_retries + 1):
        try:
            response = requests.get(
                url,
                headers=headers,
                timeout=timeout,
            )

            if response.status_code in [403, 429, 503]:
                sleep_time = random.uniform(min_sleep, max_sleep)
                print(
                    f"Bị chặn/rate-limit status={response.status_code}, "
                    f"sleep {sleep_time:.1f}s rồi thử lại..."
                )
                time.sleep(sleep_time)
                continue

            response.raise_for_status()

            return response.text

        except Exception as e:
            last_error = e
            sleep_time = random.uniform(min_sleep, max_sleep)
            print(f"Lỗi request attempt {attempt}: {e}")
            time.sleep(sleep_time)

    raise Exception(f"Request thất bại sau {max_retries} lần: {last_error}")