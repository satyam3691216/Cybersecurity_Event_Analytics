CREATE TABLE users (
    user_id INTEGER PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    department VARCHAR(100),
    role VARCHAR(50),
    account_status VARCHAR(20) DEFAULT 'Active',
    created_at TIMESTAMP NOT NULL
);