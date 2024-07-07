CREATE TABLE countries (
    code VARCHAR(36) PRIMARY KEY,
    name VARCHAR(128) NOT NULL,
    country_code VARCHAR(36),
    FOREIGN KEY (country_code) REFERENCES countries(code)
);