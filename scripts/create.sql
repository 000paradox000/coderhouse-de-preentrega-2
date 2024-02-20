CREATE TABLE IF NOT EXISTS repos2 (
    id INTEGER PRIMARY KEY,
    name VARCHAR(500),
    description VARCHAR(500) NULL,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    html_url VARCHAR(500)
);
