import sqlite3
from multiprocessing import Pool

def setup_database():
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sample_table(
        id INTEGER PRIMARY KEY,
        name TEXT
    )
    """)

    data = ['Madhu', 'Python', 'Parallel', 'Text', 'Processor']

    for item in data:
        cursor.execute("INSERT INTO sample_table(name) VALUES(?)", (item,))

    conn.commit()
    conn.close()
    print("Database setup completed")

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
    return len(chunk)


if __name__ == "__main__":
    setup_database()
    text = load_file()

    lines = text.split("\n")
    text = text.lower()
    words = text.split()

    print("Total lines:", len(lines))
    print("Total words:", len(words))

    chunk_size = 100
    chunks = [lines[i:i + chunk_size] for i in range(0, len(lines), chunk_size)]

    print("Total chunks:", len(chunks))

    with Pool(2) as p:
        result = p.map(process_chunk, chunks)

    print("Parallel output:", result)

