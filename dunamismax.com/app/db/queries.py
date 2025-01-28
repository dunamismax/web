CREATE_CONTACT_TABLE = """
CREATE TABLE IF NOT EXISTS contacts (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    message TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);
"""

INSERT_CONTACT = """
INSERT INTO contacts (name, email, message)
VALUES ($1, $2, $3);
"""
