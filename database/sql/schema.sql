CREATE TABLE users (
    user_id INTEGER PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    department VARCHAR(100),
    role VARCHAR(50),
    account_status VARCHAR(20) DEFAULT 'Active',
    created_at TIMESTAMP NOT NULL
);
CREATE TABLE devices (
    device_id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    device_type VARCHAR(50),
    operating_system VARCHAR(50),
    device_name VARCHAR(100),
    first_seen TIMESTAMP NOT NULL,
    last_seen TIMESTAMP,
    device_status VARCHAR(20) DEFAULT 'Active',

    CONSTRAINT fk_device_user
        FOREIGN KEY (user_id)
        REFERENCES users(user_id)
);
CREATE TABLE ip_addresses (
    ip_address VARCHAR(45) PRIMARY KEY,
    country VARCHAR(100),
    city VARCHAR(100),
    region VARCHAR(100),
    isp VARCHAR(150),
    ip_type VARCHAR(30),
    first_seen TIMESTAMP NOT NULL,
    last_seen TIMESTAMP
);
CREATE TABLE security_events (
    event_id BIGINT PRIMARY KEY,
    event_timestamp TIMESTAMP NOT NULL,
    event_type VARCHAR(50) NOT NULL,
    user_id INTEGER,
    device_id INTEGER,
    ip_address VARCHAR(45),
    location VARCHAR(100),
    device_type VARCHAR(50),
    operating_system VARCHAR(50),
    auth_status VARCHAR(20),
    user_agent TEXT,
    session_id VARCHAR(100),

    CONSTRAINT fk_event_user
        FOREIGN KEY (user_id)
        REFERENCES users(user_id),

    CONSTRAINT fk_event_device
        FOREIGN KEY (device_id)
        REFERENCES devices(device_id),

    CONSTRAINT fk_event_ip
        FOREIGN KEY (ip_address)
        REFERENCES ip_addresses(ip_address)
);