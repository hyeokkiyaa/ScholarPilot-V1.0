import sqlite3
import os

# Path to the database file
db_path = "backend/data/scholarpilot.db"
if not os.path.exists(db_path):
    print(f"Database file NOT found at {db_path}")
    if os.path.exists("data/scholarpilot.db"):
        db_path = "data/scholarpilot.db"
        print(f"Found at {db_path}")
    else:
        # Check current dir
        if os.path.exists("scholarpilot.db"):
            db_path = "scholarpilot.db"
        else:
            print("Could not find database file recursively.")
            # List files to be sure
            print(f"Listing backend/data: {os.listdir('backend/data') if os.path.exists('backend/data') else 'Not found'}")
            exit(1)

print(f"Checking database at: {db_path}")

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("Tables found:", [t[0] for t in tables])

    if ('papers',) in tables:
        cursor.execute("SELECT id, title, status FROM papers")
        papers = cursor.fetchall()
        print(f"\nFound {len(papers)} papers in DB:")
        for paper in papers:
            print(f"- {paper[1]} (ID: {paper[0]}, Status: {paper[2]})")
            
        if len(papers) == 0:
            print("No papers found. The upload process is likely failing before DB commit.")
    else:
        print("Table 'papers' does not exist.")

    if ('projects',) in tables:
        cursor.execute("SELECT id, name FROM projects")
        projects = cursor.fetchall()
        print(f"\nProjects: {[p[1] for p in projects]}")

    conn.close()

except Exception as e:
    print(f"Error querying database: {e}")
