import mysql.connector
from mysql.connector import Error

def create_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection

def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")

def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")
        return []

class Flight:
    def __init__(self, flight_id, airline, destination, departure_time, available_seats):
        self.flight_id = flight_id
        self.airline = airline
        self.destination = destination
        self.departure_time = departure_time
        self.available_seats = available_seats

class Reservation:
    def __init__(self, reservation_id, passenger_name, flight_id, seat_number, reservation_date):
        self.reservation_id = reservation_id
        self.passenger_name = passenger_name
        self.flight_id = flight_id
        self.seat_number = seat_number
        self.reservation_date = reservation_date

class Passenger:
    def __init__(self, passenger_id, name, contact_info):
        self.passenger_id = passenger_id
        self.name = name
        self.contact_info = contact_info

class AirlineReservationSystem:
    def __init__(self, db_connection):
        self.connection = db_connection

    def add_flight(self, flight):
        insert_flight_query = f"""
        INSERT INTO Flights (flight_id, airline, destination, departure_time, available_seats)
        VALUES ({flight.flight_id}, '{flight.airline}', '{flight.destination}', '{flight.departure_time}', {flight.available_seats});
        """
        execute_query(self.connection, insert_flight_query)

    def update_flight(self, flight_id, **kwargs):
        updates = []
        if kwargs.get('airline') is not None:
            updates.append(f"airline = '{kwargs['airline']}'")
        if kwargs.get('destination') is not None:
            updates.append(f"destination = '{kwargs['destination']}'")
        if kwargs.get('departure_time') is not None:
            updates.append(f"departure_time = '{kwargs['departure_time']}'")
        if kwargs.get('available_seats') is not None:
            updates.append(f"available_seats = {kwargs['available_seats']}")
        
        if updates:
            update_flight_query = f"UPDATE Flights SET {', '.join(updates)} WHERE flight_id = {flight_id};"
            execute_query(self.connection, update_flight_query)

    def delete_flight(self, flight_id):
        delete_flight_query = f"DELETE FROM Flights WHERE flight_id = {flight_id};"
        execute_query(self.connection, delete_flight_query)

    def add_reservation(self, reservation):
        insert_reservation_query = f"""
        INSERT INTO Reservations (reservation_id, passenger_id, flight_id, seat_number, reservation_date)
        VALUES ({reservation.reservation_id}, 
                (SELECT passenger_id FROM Passengers WHERE name='{reservation.passenger_name}'), 
                {reservation.flight_id}, '{reservation.seat_number}', '{reservation.reservation_date}');
        """
        execute_query(self.connection, insert_reservation_query)

    def update_reservation(self, reservation_id, **kwargs):
        updates = []
        if kwargs.get('passenger_name') is not None:
            updates.append(f"passenger_id = (SELECT passenger_id FROM Passengers WHERE name='{kwargs['passenger_name']}')")
        if kwargs.get('flight_id') is not None:
            updates.append(f"flight_id = {kwargs['flight_id']}")
        if kwargs.get('seat_number') is not None:
            updates.append(f"seat_number = '{kwargs['seat_number']}'")
        if kwargs.get('reservation_date') is not None:
            updates.append(f"reservation_date = '{kwargs['reservation_date']}'")
        
        if updates:
            update_reservation_query = f"UPDATE Reservations SET {', '.join(updates)} WHERE reservation_id = {reservation_id};"
            execute_query(self.connection, update_reservation_query)

    def cancel_reservation(self, reservation_id):
        delete_reservation_query = f"DELETE FROM Reservations WHERE reservation_id = {reservation_id};"
        execute_query(self.connection, delete_reservation_query)

    def passengers_on_flight_report(self, flight_id):
        select_passengers_query = f"""
        SELECT p.name
        FROM Reservations r
        JOIN Passengers p ON r.passenger_id = p.passenger_id
        WHERE r.flight_id = {flight_id};
        """
        passengers = execute_read_query(self.connection, select_passengers_query)
        return [passenger[0] for passenger in passengers]

    def add_passenger(self, passenger):
        insert_passenger_query = f"""
        INSERT INTO Passengers (passenger_id, name, contact_info)
        VALUES ({passenger.passenger_id}, '{passenger.name}', '{passenger.contact_info}');
        """
        execute_query(self.connection, insert_passenger_query)

    def update_passenger(self, passenger_id, **kwargs):
        updates = []
        if kwargs.get('name') is not None:
            updates.append(f"name = '{kwargs['name']}'")
        if kwargs.get('contact_info') is not None:
            updates.append(f"contact_info = '{kwargs['contact_info']}'")
        
        if updates:
            update_passenger_query = f"UPDATE Passengers SET {', '.join(updates)} WHERE passenger_id = {passenger_id};"
            execute_query(self.connection, update_passenger_query)

    def delete_passenger(self, passenger_id):
        delete_passenger_query = f"DELETE FROM Passengers WHERE passenger_id = {passenger_id};"
        execute_query(self.connection, delete_passenger_query)

def main():
    connection = create_connection("localhost", "root", "12345678", "airline_reservation_system")
    system = AirlineReservationSystem(connection)

    while True:
        print("1. Add Flight")
        print("2. Update Flight")
        print("3. Delete Flight")
        print("4. Add Reservation")
        print("5. Update Reservation")
        print("6. Cancel Reservation")
        print("7. Generate Passenger Report")
        print("8. Add Passenger")
        print("9. Update Passenger")
        print("10. Delete Passenger")
        print("11. Exit")
        choice = input("Enter choice: ")

        try:
            if choice == '1':
                flight_id = int(input("Enter flight ID: "))
                airline = input("Enter airline: ")
                destination = input("Enter destination: ")
                departure_time = input("Enter departure time (YYYY-MM-DD HH:MM:SS): ")
                available_seats = int(input("Enter available seats: "))
                flight = Flight(flight_id, airline, destination, departure_time, available_seats)
                system.add_flight(flight)
                print("Flight added successfully.")

            elif choice == '2':
                flight_id = int(input("Enter flight ID: "))
                airline = input("Enter airline (press enter to skip): ")
                destination = input("Enter destination (press enter to skip): ")
                departure_time = input("Enter departure time (YYYY-MM-DD HH:MM:SS) (press enter to skip): ")
                available_seats = input("Enter available seats (press enter to skip): ")
                system.update_flight(flight_id, airline=airline or None, destination=destination or None,
                                     departure_time=departure_time or None,
                                     available_seats=int(available_seats) if available_seats else None)
                print("Flight updated successfully.")

            elif choice == '3':
                flight_id = int(input("Enter flight ID: "))
                system.delete_flight(flight_id)
                print("Flight deleted successfully.")

            elif choice == '4':
                reservation_id = int(input("Enter reservation ID: "))
                passenger_name = input("Enter passenger name: ")
                flight_id = int(input("Enter flight ID: "))
                seat_number = input("Enter seat number: ")
                reservation_date = input("Enter reservation date (YYYY-MM-DD): ")
                reservation = Reservation(reservation_id, passenger_name, flight_id, seat_number, reservation_date)
                system.add_reservation(reservation)
                print("Reservation added successfully.")

            elif choice == '5':
                reservation_id = int(input("Enter reservation ID: "))
                passenger_name = input("Enter passenger name (press enter to skip): ")
                flight_id = input("Enter flight ID (press enter to skip): ")
                seat_number = input("Enter seat number (press enter to skip): ")
                reservation_date = input("Enter reservation date (YYYY-MM-DD) (press enter to skip): ")
                system.update_reservation(reservation_id, passenger_name=passenger_name or None,
                                          flight_id=int(flight_id) if flight_id else None,
                                          seat_number=seat_number or None, reservation_date=reservation_date or None)
                print("Reservation updated successfully.")

            elif choice == '6':
                reservation_id = int(input("Enter reservation ID: "))
                system.cancel_reservation(reservation_id)
                print("Reservation cancelled successfully.")

            elif choice == '7':
                flight_id = int(input("Enter flight ID: "))
                passengers = system.passengers_on_flight_report(flight_id)
                print(f"Passengers on flight {flight_id}: {', '.join(passengers)}")

            elif choice == '8':
                passenger_id = int(input("Enter passenger ID: "))
                name = input("Enter passenger name: ")
                contact_info = input("Enter contact info: ")
                passenger = Passenger(passenger_id, name, contact_info)
                system.add_passenger(passenger)
                print("Passenger added successfully.")

            elif choice == '9':
                passenger_id = int(input("Enter passenger ID: "))
                name = input("Enter passenger name (press enter to skip): ")
                contact_info = input("Enter contact info (press enter to skip): ")
                system.update_passenger(passenger_id, name=name or None, contact_info=contact_info or None)
                print("Passenger updated successfully.")

            elif choice == '10':
                passenger_id = int(input("Enter passenger ID: "))
                system.delete_passenger(passenger_id)
                print("Passenger deleted successfully.")

            elif choice == '11':
                print("Exiting...")
                break

            else:
                print("Invalid choice. Please try again.")
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
