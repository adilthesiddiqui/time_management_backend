-- =========================
-- DUMMY DATA FOR USERS TABLE
-- =========================
-- NOTE: This SQL file is for reference only.
-- To properly seed the database with hashed passwords, use the Python script:
--   python db/seed_database.py
--
-- The Python script will:
--   - Create 5 test users (all with password: "password123")
--   - Create 15 tasks distributed across the users
--   - Handle password hashing correctly using bcrypt

INSERT OR IGNORE INTO users (email, password_hash, created_at) VALUES
('john.doe@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYq5q5q5q5q', datetime('now', '-30 days')),
('jane.smith@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYq5q5q5q5q', datetime('now', '-25 days')),
('bob.johnson@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYq5q5q5q5q', datetime('now', '-20 days')),
('alice.williams@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYq5q5q5q5q', datetime('now', '-15 days')),
('charlie.brown@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYq5q5q5q5q', datetime('now', '-10 days'));

-- =========================
-- DUMMY DATA FOR TASKS TABLE
-- =========================
-- Note: user_id references the users table. Adjust based on actual user IDs after insertion.

INSERT OR IGNORE INTO tasks (title, description, user_id, is_completed, created_at) VALUES
('Complete project documentation', 'Write comprehensive documentation for the API endpoints and database schema', 1, 0, datetime('now', '-5 days')),
('Review code changes', 'Review pull requests and provide feedback to team members', 1, 1, datetime('now', '-4 days')),
('Setup CI/CD pipeline', 'Configure continuous integration and deployment for the project', 1, 0, datetime('now', '-3 days')),
('Design user interface', 'Create mockups and wireframes for the frontend application', 2, 0, datetime('now', '-6 days')),
('Implement authentication', 'Add JWT-based authentication system to the backend', 2, 1, datetime('now', '-5 days')),
('Write unit tests', 'Create comprehensive unit tests for all API endpoints', 2, 0, datetime('now', '-2 days')),
('Database optimization', 'Analyze and optimize database queries for better performance', 3, 0, datetime('now', '-7 days')),
('Security audit', 'Review security practices and implement necessary improvements', 3, 1, datetime('now', '-6 days')),
('API documentation', 'Generate and publish API documentation using Swagger/OpenAPI', 3, 0, datetime('now', '-1 days')),
('User feedback collection', 'Set up system to collect and analyze user feedback', 4, 0, datetime('now', '-8 days')),
('Performance monitoring', 'Implement monitoring tools to track application performance', 4, 1, datetime('now', '-4 days')),
('Bug fixes', 'Fix critical bugs reported in the issue tracker', 4, 0, datetime('now', '-3 days')),
('Feature implementation', 'Implement new feature requests from product backlog', 5, 0, datetime('now', '-9 days')),
('Code refactoring', 'Refactor legacy code to improve maintainability', 5, 1, datetime('now', '-5 days')),
('Deployment preparation', 'Prepare application for production deployment', 5, 0, datetime('now', '-2 days'));
