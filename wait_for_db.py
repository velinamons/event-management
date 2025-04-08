import time
import socket
import os
import sys

DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_PORT = int(os.environ.get("DB_PORT", 5432))
TIMEOUT = int(os.environ.get("DB_TIMEOUT", 30))


def wait_for_db():
    start = time.time()
    while True:
        try:
            with socket.create_connection((DB_HOST, DB_PORT), timeout=2):
                print(f"[wait_for_db] DB is up at {DB_HOST}:{DB_PORT}")
                return
        except OSError as e:
            elapsed = time.time() - start
            if elapsed > TIMEOUT:
                print(f"[wait_for_db] Timeout after {TIMEOUT}s waiting for DB.")
                sys.exit(1)
            print(f"[wait_for_db] Waiting for DB... ({e})")
            time.sleep(1)


if __name__ == "main":
    wait_for_db()
