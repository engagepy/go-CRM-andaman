import csv
import psycopg2

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    host="localhost", database="gobasic", user="yourusername", password="yourpassword"
)

# Open the CSV file and create a CSV reader object
with open("data.csv", "r") as csvfile:
    csvreader = csv.reader(csvfile)

    # Skip the header row
    next(csvreader)

    # Create a list to hold the data rows
    rows = []

    # Loop through the rows in the CSV file
    for row in csvreader:
        # Extract the data from the row
        hotel_name = row[0]
        customer_rating = row[1]
        room_name = row[2]
        room_categories = row[3]
        location = row[4]
        net_cp = int(row[5])
        net_map = int(row[6])
        net_ap = int(row[7])
        net_cp_kid = int(row[8])
        net_map_kid = int(row[9])

        rows.append(
            (
                hotel_name,
                customer_rating,
                room_name,
                room_categories,
                location,
                net_cp,
                net_map,
                net_ap,
                net_map_kid,
                net_cp_kid,
            )
        )

    # Insert the data rows into the database
    cursor = conn.cursor()
    insert_query = "INSERT INTO hotel (hotel_name, customer_rating, room_name, room_categories, location, net_cp, net_map, net_ap, net_map_kid, net_cp_kid) VALUES %s"
    psycopg2.extras.execute_values(cursor, insert_query, rows)
    conn.commit()

conn.close()
