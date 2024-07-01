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

-- Insert initial data into Users table
-- INSERT INTO users (id, email, password, first_name, last_name) VALUES
-- ('123e4567-e89b-12d3-a456-426614174000', 'host1@example.com', 'password1', 'Host', 'One'),
-- ('123e4567-e89b-12d3-a456-426614174001', 'guest1@example.com', 'password2', 'Guest', 'One');

-- Create countries table
CREATE TABLE IF NOT EXISTS countries (
    code CHAR(2) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
/* INSERT INTO countries(code, name) VALUES
('US', 'United States'); */

-- Create cities table
CREATE TABLE IF NOT EXISTS cities (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    country_code CHAR(2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (country_code) REFERENCES countries(code)
);
/* INSERT INTO cities(id, name, country_code) VALUES
('123e4567-e89b-12d3-a456-426614174002', 'New York', 'US'),
('123e4567-e89b-12d3-a456-426614174005', 'Miami', 'US'); */

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

-- Insert initial data into Places table
/* INSERT INTO places (id, host_id, name, description, address, city_id, price_per_night, max_guests) VALUES
('123e4567-e89b-12d3-a456-426614174000', '123e4567-e89b-12d3-a456-426614174001', 'Cozy Cottage', 'A cozy cottage in the countryside', '123 Country Lane', '123e4567-e89b-12d3-a456-426614174002', 100.00, 4),
('123e4567-e89b-12d3-a456-426614174003', '123e4567-e89b-12d3-a456-426614174004', 'Modern Apartment', 'A modern apartment in the city center', '456 City Street', '123e4567-e89b-12d3-a456-426614174005', 150.00, 2); */

-- Create Amenities table
CREATE TABLE IF NOT EXISTS amenities (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert initial data into Amenities table
/* INSERT INTO amenities (id, name) VALUES
('123e4567-e89b-12d3-a456-426614174006', 'WiFi'),
('123e4567-e89b-12d3-a456-426614174007', 'Air Conditioning'),
('123e4567-e89b-12d3-a456-426614174008', 'Kitchen'),
('123e4567-e89b-12d3-a456-426614174009', 'Parking'); */

-- Create Place_Amenities table (for many-to-many relationship)
CREATE TABLE IF NOT EXISTS place_amenities (
    place_id VARCHAR(36),
    amenity_id VARCHAR(36),
    PRIMARY KEY (place_id, amenity_id),
    FOREIGN KEY (place_id) REFERENCES places(id),
    FOREIGN KEY (amenity_id) REFERENCES amenities(id)
);

-- Insert initial data into Place_Amenities table
/* INSERT INTO place_amenities (place_id, amenity_id) VALUES
('123e4567-e89b-12d3-a456-426614174000', '123e4567-e89b-12d3-a456-426614174006'), -- Cozy Cottage has WiFi
('123e4567-e89b-12d3-a456-426614174000', '123e4567-e89b-12d3-a456-426614174008'), -- Cozy Cottage has Kitchen
('123e4567-e89b-12d3-a456-426614174003', '123e4567-e89b-12d3-a456-426614174006'), -- Modern Apartment has WiFi
('123e4567-e89b-12d3-a456-426614174003', '123e4567-e89b-12d3-a456-426614174007'), -- Modern Apartment has Air Conditioning
('123e4567-e89b-12d3-a456-426614174003', '123e4567-e89b-12d3-a456-426614174009'); -- Modern Apartment has Parking
 */

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

-- Insert initial data into Reviews table
/* INSERT INTO reviews (id, place_id, user_id, rating, comment) VALUES
('123e4567-e89b-12d3-a456-426614174010', '123e4567-e89b-12d3-a456-426614174000', '123e4567-e89b-12d3-a456-426614174004', 5, 'Amazing stay! The cottage was cozy and comfortable.'),
('123e4567-e89b-12d3-a456-426614174011', '123e4567-e89b-12d3-a456-426614174003', '123e4567-e89b-12d3-a456-426614174004', 4, 'Great location and amenities, but a bit noisy at night.');
 */
