-- Minimal MySQL schema. Django migrations will build out the rest.
CREATE TABLE IF NOT EXISTS eventCategories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(32) NOT NULL UNIQUE
);

-- Add more tables if wanting to pre-seed, otherwise let Django manage.