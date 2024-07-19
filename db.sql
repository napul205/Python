-- Flights Table
CREATE TABLE Flights (
    flight_id INT PRIMARY KEY,
    airline VARCHAR(100),
    destination VARCHAR(100),
    departure_time DATETIME,
    available_seats INT
);

-- Passengers Table
CREATE TABLE Passengers (
    passenger_id INT PRIMARY KEY,
    name VARCHAR(100),
    contact_info VARCHAR(100)
);

-- Reservations Table
CREATE TABLE Reservations (
    reservation_id INT PRIMARY KEY,
    passenger_id INT,
    flight_id INT,
    seat_number VARCHAR(10),
    reservation_date DATE,
    FOREIGN KEY (passenger_id) REFERENCES Passengers(passenger_id),
    FOREIGN KEY (flight_id) REFERENCES Flights(flight_id)
);
