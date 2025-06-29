import sqlite3
import os

def create_tables():
    os.makedirs("database", exist_ok=True)
    conn = sqlite3.connect("database/data.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS edukasi (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        judul TEXT NOT NULL,
        isi TEXT NOT NULL
    )""")
    conn.commit()
    conn.close()

def buat_tabel_kuis():
    conn = sqlite3.connect("database/data.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS kuis (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pertanyaan TEXT,
        pilihan_a TEXT,
        pilihan_b TEXT,
        pilihan_c TEXT,
        pilihan_d TEXT,
        jawaban TEXT
    )""")
    conn.commit()
    conn.close()

def buat_tabel_curhat():
    conn = sqlite3.connect("database/data.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS curhat (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        isi TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )""")
    conn.commit()
    conn.close()
