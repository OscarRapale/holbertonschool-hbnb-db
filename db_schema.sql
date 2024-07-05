-- Create Users table
CREATE TABLE IF NOT EXISTS users (
    id VARCHAR(36) PRIMARY KEY,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(128) NOT NULL,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    is_admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
INSERT INTO users (id, email, password_hash, first_name, last_name, is_admin)
VALUES ('4e7e4f43-0132-43d7-bfef-518e9ed70310','testing@example.com', 'password123', 'Testing', 'User', False),
VALUES ('245300d5-479e-4fa9-a44b-fbaad0420f76','testing2@example.com', 'password456', 'Tester', 'Users', False);

-- Create countries table
CREATE TABLE IF NOT EXISTS countries (
    code CHAR(2) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
INSERT INTO countries (code, name)
VALUES ('PR', 'Puerto Rico');

-- Create cities table
CREATE TABLE IF NOT EXISTS cities (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    country_code CHAR(2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (country_code) REFERENCES countries(code)
);
INSERT INTO cities (id, name, country_code)
VALUES ('e552392a-6b5f-4df5-bc26-70021887d1ab','San Juan', 'PR')

-- Create Places table
CREATE TABLE IF NOT EXISTS places (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(64) NOT NULL,
    description TEXT NOT NULL,
    address VARCHAR(255) NOT NULL,
    city_id VARCHAR(36),
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    host_id VARCHAR(36),
    number_of_rooms INTEGER NOT NULL,
    number_of_bathrooms INTEGER NOT NULL,
    price_per_night FLOAT NOT NULL,
    max_guests INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (host_id) REFERENCES users(id),
    FOREIGN KEY (city_id) REFERENCES cities(id)
);
INSERT INTO places (id, name, description, address, city_id, latitude, longitude, host_id, number_of_rooms, number_of_bathrooms, price_per_night, max_guests)
VALUES ('fe82bc9a-7b82-4798-83c1-cf0319a231c9','New Place', 'New place in the city', '123 Main Street', 'e552392a-6b5f-4df5-bc26-70021887d1ab', 40.7128, -74.006, '4e7e4f43-0132-43d7-bfef-518e9ed70310', 2, 1, 100.0, 2);

-- Create Amenities table
CREATE TABLE IF NOT EXISTS amenities (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
INSERT INTO amenities(id, name)
VALUES ('d76727dd-0883-4084-8f74-f11f385cd2d5','Wi-Fi')

-- Create Place_Amenities table (for many-to-many relationship)
CREATE TABLE IF NOT EXISTS place_amenities (
    place_id VARCHAR(36),
    amenity_id VARCHAR(36),
    PRIMARY KEY (place_id, amenity_id),
    FOREIGN KEY (place_id) REFERENCES places(id),
    FOREIGN KEY (amenity_id) REFERENCES amenities(id)
);
INSERT INTO place_amenities (place_id, amenity_id)
VALUES ('', '')

-- Create Reviews table
CREATE TABLE IF NOT EXISTS reviews (
    id VARCHAR(36) PRIMARY KEY,
    place_id VARCHAR(36),
    user_id VARCHAR(36),
    rating INTEGER NOT NULL CHECK (rating BETWEEN 1 AND 5),
    comment TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (place_id) REFERENCES places(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);
INSERT INTO reviews (id, place_id, user_id, rating, comment)
VALUES ('0093925b-5c21-4b91-ae41-67eb0b311869', 'fe82bc9a-7b82-4798-83c1-cf0319a231c9', '245300d5-479e-4fa9-a44b-fbaad0420f76', 5, "Very nice place!")
