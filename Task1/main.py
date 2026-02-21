import sqlite3
from multiprocessing import Pool
from rule_engine import apply_rules

def setup_database():
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chunk_results(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        word_count INTEGER,
        status TEXT
    )
    """)

    conn.commit()
    conn.close()
    print("Database ready")

def load_file():
    try:
        with open("sample.txt", "r") as file:
            text = file.read()
        print("File loaded")
        return text
    except FileNotFoundError:
        print("sample.txt not found")
        return ""


def process_chunk(chunk):
    return apply_rules(chunk)


def save_to_db(results):
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()

    for r in results:
        cursor.execute(
            "INSERT INTO chunk_results(word_count,status) VALUES(?,?)",
            (r["words"], r["status"])
        )

    conn.commit()
    conn.close()
    print("Results stored in database")


if __name__ == "__main__":

    setup_database()

    text = load_file()

    if not text:
        print("No data to process")
        exit()

    text = text.lower()
    lines = text.split("\n")
    words = text.split()

    print("Total lines:", len(lines))
    print("Total words:", len(words))

    chunk_size = 10
    chunks = [lines[i:i + chunk_size] for i in range(0, len(lines), chunk_size)]

    print("Total chunks:", len(chunks))

    with Pool(2) as p:
        result = p.map(process_chunk, chunks)

    print("\n===== Chunk Processing Summary =====")

    large_count = 0
    small_count = 0

    for i, r in enumerate(result, 1):
        print(f"Chunk {i:02d} | Words: {r['words']:4d} | Status: {r['status']}")

        if r["status"] == "LARGE":
            large_count += 1
        elif r["status"] == "SMALL":
            small_count += 1

    print("====================================")

    print(f"Total LARGE chunks : {large_count}")
    print(f"Total SMALL chunks : {small_count}\n")

    save_to_db(result)

