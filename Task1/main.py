import sqlite3
conn = sqlite3.connect("data.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS sample_table(
id INTEGER PRIMARY KEY,
name TEXT
)
""")
cursor.execute("INSERT INTO sample_table(name) VALUES('Madhu')")
cursor.execute("INSERT INTO sample_table(name) VALUES('Python')")
cursor.execute("INSERT INTO sample_table(name) VALUES('Parallel')")
cursor.execute("INSERT INTO sample_table(name) VALUES('Text')")
cursor.execute("INSERT INTO sample_table(name) VALUES('Processor')")

conn.commit()
conn.close()

with open("sample.txt", "r") as file:
    text = file.read()

print("File loaded")
lines = text.split("\n")
text = text.lower()
words = text.split()

print("Total lines:", len(lines))
chunk_size = 100
chunks = [lines[i:i+chunk_size] for i in range(0, len(lines), chunk_size)]

print("Total chunks:", len(chunks))
from multiprocessing import Pool

def process_chunk(chunk):
    return len(chunk)

if __name__ == "__main__":
    with Pool(2) as p:
        result = p.map(process_chunk, chunks)

    print("Parallel output:", result)
