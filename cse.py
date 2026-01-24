import sqlite3

# Connect to the database
conn = sqlite3.connect("trial1.db")
cursor = conn.cursor()

# Enable foreign keys
cursor.execute("PRAGMA foreign_keys = ON;")

# Create tables
cursor.execute("""
CREATE TABLE IF NOT EXISTS department (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS faculty (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    designation TEXT,
    department_id INTEGER,
    FOREIGN KEY (department_id) REFERENCES department(id) ON DELETE CASCADE
);
""")

# Insert the department (only once)
department_name = "Department of Computer Science & Engineering"
cursor.execute("INSERT OR IGNORE INTO department (name) VALUES (?);", (department_name,))

# Get the department_id for foreign key use
cursor.execute("SELECT id FROM department WHERE name = ?;", (department_name,))
department_id = cursor.fetchone()[0]

# Faculty data (same as before)
faculty_data = [
    ("Dr. Chhatar Singh Lamba", "Professor & Associate Dean"),
    ("Dr. Roheet Bhatnagar", "Professor & Associate Dean"),
    ("Dr. Neha Chaudhary", "Professor & HoD"),
    ("Dr. Mahesh Jangid", "Associate Professor & Deputy HoD"),
    ("Mr. Abhay Singh Bisht", "Assistant Professor (Adhoc)"),
    ("Dr. Aditya Sinha", "Assistant Professor"),
    ("Dr. Ajay Kumar", "Assistant Professor (Selection Grade)"),
    ("Dr. Ajay Kumar", "Assistant Professor"),
    ("Dr. Ajit Noonia", "Assistant Professor (Selection Grade) & Assistant Director (CR &P)"),
    ("Ms. Akanksha Mrinali", "Assistant Professor"),
    ("Dr. Akshay Jadhav", "Assistant Professor"),
    ("Dr. Amit Garg", "Associate Professor"),
    ("Dr. Amit Kumar Gupta", "Associate Professor"),
    ("Dr. Anil Kumar", "Assistant Professor (Senior Scale)"),
    ("Ms. Anita Shrotriya", "Assistant Professor (Selection Grade)"),
    ("Dr. Ankit Shrivastava", "Assistant Professor (Senior Scale)"),
    ("Dr. Ankur Pandey", "Assistant Professor (Selection Grade)"),
    ("Dr. Arpita Banoria", "Assistant Professor"),
    ("Mr. Arvind Mehta", "Assistant Professor (Adhoc)"),
    ("Dr. Ashish Kumar", "Associate Professor"),
    ("Dr. Ashish Sharma", "Associate Professor"),
    ("Dr. Ashok Kumar Saini", "Assistant Professor (Senior Scale)"),
    ("Mr. Atul Kumar Verma", "Assistant Professor (Senior Scale) & Assistant Director, Directorate of Student Welfare"),
    ("Ms. Babita Tiwari", "Assistant Professor (Senior Scale)"),
    ("Ms. Bali Devi", "Assistant Professor"),
    ("Mr. Bhawani Singh Rathore", "Assistant Professor (Adhoc)"),
    ("Dr. Dibakar Sinha", "Assistant Professor (Senior Scale)"),
    ("Dr. Divya Thakur", "Assistant Professor"),
    ("Dr. Gireesh Kumar", "Assistant Professor (Selection Grade)"),
    ("Mr. Girish Sharma", "Assistant Professor (Senior Scale)"),
    ("Mrs. Gunjan Pathak", "Assistant Professor (Contract)"),
    ("Mrs. Harshika Mathur", "Assistant Professor (Adhoc)"),
    ("Dr. Jay Prakash Singh", "Assistant Professor (Senior Scale)"),
    ("Mr. Jay Shankar Sharma", "Assistant Professor"),
    ("Dr. Jeyakrishnan V", "Associate Professor"),
    ("Dr. Juhi Singh", "Assistant Professor (Selection Grade)"),
    ("Ms. Kirti Paliwal", "Assistant Professor (Adhoc)"),
    ("Mr. Lav Upadhyay", "Assistant Professor (Senior Scale)"),
    ("Dr. Manmohan Sharma", "Assistant Professor (Selection Grade)"),
    ("Dr. Manu Shrivastava", "Assistant Professor (Senior Scale)"),
    ("Dr. Mayank Namdev", "Assistant Professor (Selection Grade)"),
    ("Mr. Mohit Kumar", "Assistant Professor (Contract)"),
    ("Dr. Mohit Kushwaha", "Assistant Professor"),
    ("Ms. Neha", "Assistant Professor (Adhoc)"),
    ("Dr. Neha Janu", "Associate Professor"),
    ("Dr. Neelam Chaplot", "Associate Professor"),
    ("Dr. Neetu Gupta", "Assistant Professor (Selection Grade)"),
    ("Ms. Nisha Kundu", "Assistant Professor"),
    ("Dr. Onkar Singh", "Assistant Professor (Senior Scale)"),
    ("Dr. Pallavi", "Assistant Professor"),
    ("Dr. Prakash Ramani", "Professor & Director (Admissions)"),
    ("Dr. Praneet Saurabh", "Associate Professor"),
    ("Dr. Prashant Vats", "Assistant Professor (Selection Grade)"),
    ("Dr. Rajat Goel", "Associate Professor"),
    ("Dr. Ridhi Arora", "Assistant Professor"),
    ("Dr. Rishav Dubey", "Assistant Professor (Senior Scale)"),
    ("Dr. Rishi Gupta", "Associate Professor"),
    ("Dr. Rishi Kumar Srivastva", "Assistant Professor"),
    ("Mr. Sachin Gupta", "Assistant Professor (Senior Scale)"),
    ("Dr. Sakshi Shringi", "Assistant Professor"),
    ("Dr. Sandeep Chaurasia", "Professor & Director (Corporate Relations & Placements)"),
    ("Ms. Santoshi Rudrakar", "Assistant Professor"),
    ("Dr. Satpal Singh Kushwaha", "Assistant Professor (Selection Grade)"),
    ("Dr. Satyabrata Roy", "Associate Professor"),
    ("Dr. Sayar Singh Shekhawat", "Associate Professor"),
    ("Dr. Shikha Mundra", "Assistant Professor (Senior Scale)"),
    ("Dr. Shishir Singh Chauhan", "Assistant Professor (Senior Scale)"),
    ("Mrs. Shweta Gangrade", "Assistant Professor"),
    ("Ms. Shweta Sharma", "Assistant Professor (Adhoc)"),
    ("Dr. Sonia", "Assistant Professor"),
    ("Ms. Soni Gupta", "Assistant Professor (Contract)"),
    ("Dr. Sunita Singhal", "Associate Professor (Senior Scale)"),
    ("Dr. Surbhi Sharma", "Assistant Professor (Senior Scale) & Assistant Director, E-Cell"),
    ("Dr. Sushama", "Assistant Professor (Senior Scale) & Assistant Director, Directorate of Student Welfare"),
    ("Dr. Susheela Vishnoi", "Assistant Professor (Selection Grade)"),
    ("Ms. Surbhi Syal", "Assistant Professor"),
    ("Mr. Tapan Kumar Dey", "Assistant Professor (Selection Grade)"),
    ("Mr. Tarun Jain", "Assistant Professor (Senior Scale)"),
    ("Mrs. Tripti Kulshrestha", "Assistant Professor (Adhoc)"),
    ("Dr. Umashankar Rawat", "Professor"),
    ("Dr. Usha Jain", "Assistant Professor"),
    ("Ms. Vaishali Chauhan", "Assistant Professor (Senior Scale)"),
    ("Ms. Varda Pareek", "Assistant Professor"),
    ("Mr. Vijay Hasan Puri", "Assistant Professor"),
    ("Ms. Vipasha Sharma", "Assistant Professor (Adhoc)"),
    ("Mr. Virendra Kumar Meghwal", "Assistant Professor"),
    ("Mr. Vivek Singh Sikarwar", "Assistant Professor (Selection Grade)"),
]

# Insert all faculty with department_id
cursor.executemany("""
INSERT INTO faculty (name, designation, department_id)
VALUES (?, ?, ?);
""", [(name, designation, department_id) for name, designation in faculty_data])

conn.commit()
conn.close()

print(f"✅ Inserted {len(faculty_data)} faculty linked to Department ID {department_id}")
