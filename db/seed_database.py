"""
Script to seed the database with dummy data.
Run this script to populate your database with test users and tasks.
"""
import sqlite3
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

import bcrypt

DB_PATH = BASE_DIR / 'db' / 'app.db'


def hash_password(password: str) -> str:
    """Hash password using bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def seed_database():
    """Seed the database with dummy data"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Clear existing data (optional - comment out if you want to keep existing data)
    # cursor.execute("DELETE FROM tasks")
    # cursor.execute("DELETE FROM users")
    
    # Insert users with hashed passwords
    # Default password for all users: "password123"
    default_password = "password123"
    password_hash = hash_password(default_password)
    
    users_data = [
        ('john.doe@example.com', password_hash),
        ('jane.smith@example.com', password_hash),
        ('bob.johnson@example.com', password_hash),
        ('alice.williams@example.com', password_hash),
        ('charlie.brown@example.com', password_hash),
    ]
    
    user_ids = []
    for email, pwd_hash in users_data:
        try:
            cursor.execute(
                "INSERT INTO users (email, password_hash) VALUES (?, ?)",
                (email, pwd_hash)
            )
            user_ids.append(cursor.lastrowid)
            print(f"[OK] Created user: {email} (ID: {cursor.lastrowid})")
        except sqlite3.IntegrityError:
            # User already exists, get their ID
            existing_user = cursor.execute(
                "SELECT id FROM users WHERE email = ?", (email,)
            ).fetchone()
            if existing_user:
                user_ids.append(existing_user[0])
                print(f"[EXISTS] User already exists: {email} (ID: {existing_user[0]})")
    
    conn.commit()
    
    # Insert tasks
    tasks_data = [
        ('Complete project documentation', 'Write comprehensive documentation for the API endpoints and database schema', user_ids[0], 0),
        ('Review code changes', 'Review pull requests and provide feedback to team members', user_ids[0], 1),
        ('Setup CI/CD pipeline', 'Configure continuous integration and deployment for the project', user_ids[0], 0),
        ('Design user interface', 'Create mockups and wireframes for the frontend application', user_ids[1], 0),
        ('Implement authentication', 'Add JWT-based authentication system to the backend', user_ids[1], 1),
        ('Write unit tests', 'Create comprehensive unit tests for all API endpoints', user_ids[1], 0),
        ('Database optimization', 'Analyze and optimize database queries for better performance', user_ids[2], 0),
        ('Security audit', 'Review security practices and implement necessary improvements', user_ids[2], 1),
        ('API documentation', 'Generate and publish API documentation using Swagger/OpenAPI', user_ids[2], 0),
        ('User feedback collection', 'Set up system to collect and analyze user feedback', user_ids[3], 0),
        ('Performance monitoring', 'Implement monitoring tools to track application performance', user_ids[3], 1),
        ('Bug fixes', 'Fix critical bugs reported in the issue tracker', user_ids[3], 0),
        ('Feature implementation', 'Implement new feature requests from product backlog', user_ids[4], 0),
        ('Code refactoring', 'Refactor legacy code to improve maintainability', user_ids[4], 1),
        ('Deployment preparation', 'Prepare application for production deployment', user_ids[4], 0),
    ]
    
    for title, description, user_id, is_completed in tasks_data:
        try:
            cursor.execute(
                "INSERT INTO tasks (title, description, user_id, is_completed) VALUES (?, ?, ?, ?)",
                (title, description, user_id, is_completed)
            )
            print(f"[OK] Created task: {title} (User ID: {user_id})")
        except sqlite3.IntegrityError:
            print(f"[EXISTS] Task already exists: {title}")
    
    conn.commit()
    conn.close()
    
    print("\n[SUCCESS] Database seeding completed!")
    print(f"\n[INFO] Test credentials:")
    print(f"   Email: john.doe@example.com")
    print(f"   Password: {default_password}")
    print(f"\n   (All users have the same password: {default_password})")


if __name__ == "__main__":
    seed_database()
