import sqlite3

# Connect to the database
conn = sqlite3.connect("trial1.db")
cursor = conn.cursor()

# Create the subjects table
cursor.execute('''
CREATE TABLE IF NOT EXISTS subjects (
    subject_id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject_name TEXT UNIQUE NOT NULL
)
''')

# Create the playlists table
cursor.execute('''
CREATE TABLE IF NOT EXISTS playlists (
    playlist_id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject_id INTEGER,
    url TEXT NOT NULL,
    FOREIGN KEY (subject_id) REFERENCES subjects(subject_id)
)
''')

# Define Subject class
class Subject:
    def __init__(self, subject_name):
        self.subject_name = subject_name

    def save_to_db(self, cursor):
        try:
            cursor.execute('''
                INSERT INTO subjects (subject_name)
                VALUES (?)
            ''', (self.subject_name,))
        except sqlite3.IntegrityError:
            print(f"Subject '{self.subject_name}' already exists, skipping insert.")

    def get_id(self, cursor):
        cursor.execute('''
            SELECT subject_id FROM subjects WHERE subject_name = ?
        ''', (self.subject_name,))
        return cursor.fetchone()[0]

# Define Playlist class
class Playlist:
    def __init__(self, subject_id, url):
        self.subject_id = subject_id
        self.url = url

    def save_to_db(self, cursor):
        cursor.execute('''
            INSERT INTO playlists (subject_id, url)
            VALUES (?, ?)
        ''', (self.subject_id, self.url))

# Insert subjects
subjects = [
    Subject("DAA"),
    Subject("DSA"),
    Subject("Operating System"),
    Subject("Automata and Compiler Design"),
    Subject("Java OOPs")
]

for subject in subjects:
    subject.save_to_db(cursor)

# Define playlist data (replace URLs with real ones)

playlist_data = {
    "DAA": [
        "https://youtube.com/playlist?list=PLDN4rrl48XKpZkf03iYFl-O29szjTrs_O&si=IYYZPcWDE1azkUj2",
        "https://youtube.com/playlist?list=PLXj4XH7LcRfAG09GbFgMOLACfvbMplHsW&si=0HpH_0m-IuUTY4ss"
    ],
    "DSA": [
        "https://youtube.com/playlist?list=PLdo5W4Nhv31bbKJzrsKfMpo_grxuLl8LU&si=UQc6cVvXZpwPNi6z",
        "https://youtube.com/playlist?list=PLAXnLdrLnQpRcveZTtD644gM9uzYqJCwr&si=rZx6fSoQH9r1M2HB"
    ],
    "Operating System": [
        "https://youtube.com/playlist?list=PLxCzCOWd7aiGz9donHRrE9I3Mwn6XdP8p&si=cmgN5dM9XMwURd25",
        "https://youtube.com/playlist?list=PLmXKhU9FNesSFvj6gASuWmQd23Ul5omtD&si=vT6D_TS0lX187yqd"
    ],
    "Automata and Compiler Design": [
        "https://youtube.com/playlist?list=PLBlnK6fEyqRgp46KUv4ZY69yXmpwKOIev&si=0Psb880SRQrmLpPw",
        "https://youtube.com/playlist?list=PLmXKhU9FNesSdCsn6YQqu9DmXRMsYdZ2T&si=V-hEwpy81cfXI7zO"
    ],
    "Java OOPs": [
        "https://youtube.com/playlist?list=PLqleLpAMfxGCbdaJ6SoExDfHrTfRDeWeG&si=5HNlINs84afwe1kw",
        "https://youtube.com/playlist?list=PL9gnSGHSqcno1G3XjUbwzXHL8_EttOuKk&si=7VLCZIDbr0yGyKHK"
    ]
}

# Insert playlists
for subject_name, urls in playlist_data.items():
    subject = Subject(subject_name)
    subject_id = subject.get_id(cursor)
    for url in urls:
        playlist = Playlist(subject_id, url)
        playlist.save_to_db(cursor)

# Commit and close
conn.commit()
conn.close()

print("Subjects and playlists inserted successfully.")
