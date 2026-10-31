CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    created_at TIMESTAMP DEFAULT NOW()
);

INSERT INTO users (name, email)
VALUES
('John', 'john@example.com'),
('Doe', 'doe@example.com'),
('Alice', 'alice@example.com'),
('Bob', 'bob@example.com');

-- Simple function to simulate read load
CREATE OR REPLACE FUNCTION simulate_load() RETURNS void AS $$
DECLARE
    i INT;
BEGIN
    FOR i IN 1..50 LOOP
        PERFORM * FROM users WHERE id = (RANDOM() * 4)::INT + 1;
    END LOOP;
END;
$$ LANGUAGE plpgsql;