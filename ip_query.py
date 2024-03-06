#!/usr/bin/python3
import argparse
import sqlite3
from datetime import datetime

def create_table(conn):
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ip_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip_address TEXT NOT NULL,
            insert_time DATETIME NOT NULL,
            last_query_time DATETIME
        )
    ''')
    conn.commit()

def is_valid_ip(ip_address):
    # Check if the IP address consists only of digits and dots
    return all(c.isdigit() or c == '.' for c in ip_address)

def insert_ip(conn, ip_address):
    if not is_valid_ip(ip_address):
        print("Invalid IP address format. Only digits (0-9) and dots (.) are allowed.")
        return

    cursor = conn.cursor()
    insert_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Check if IP address already exists
    cursor.execute('SELECT * FROM ip_log WHERE ip_address = ?', (ip_address,))
    existing_ip = cursor.fetchone()

    if existing_ip:
        print(f"IP Address '{ip_address}' already in the database, inserted on {existing_ip[2]}")
    else:
        cursor.execute('INSERT INTO ip_log (ip_address, insert_time) VALUES (?, ?)', (ip_address, insert_time))
        print(f"IP Address '{ip_address}' inserted on {insert_time}")

    conn.commit()

def query_ip(conn, partial_ip):
    cursor = conn.cursor()

    # Check if any IP address matches the partial IP at the beginning in the database
    cursor.execute('SELECT * FROM ip_log WHERE ip_address LIKE ?', (partial_ip + '%',))
    results = cursor.fetchall()

    if results:
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        for result in results:
            ip_address = result[1]
            # Update last_query_time only if it is not already set
            if result[3] is None:
                cursor.execute('UPDATE ip_log SET last_query_time = ? WHERE ip_address = ?', (current_time, ip_address))
                conn.commit()

            print(f"IP Address: {ip_address}")
            print(f"Insert Time: {result[2]}")
            print(f"Last Query Time: {result[3]}")
            print("-----------------------------")
    else:
        print(f"No IP addresses starting with '{partial_ip}' found in the database.")

def get_record_count(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM ip_log')
    result = cursor.fetchone()
    return result[0]

def main():
    parser = argparse.ArgumentParser(description='Simple IP Logger')
    parser.add_argument('-i', '--import', dest='import_ip', help='Import IP address into the database')
    parser.add_argument('ip_address', nargs='?', help='Query the database for the specified IP address')

    args = parser.parse_args()

    conn = sqlite3.connect('/home/user/bin/ip_log.db')
    create_table(conn)

    if args.import_ip:
        insert_ip(conn, args.import_ip)
    elif args.ip_address:
        query_ip(conn, args.ip_address)
    else:
        print("Usage:")
        print("-i, --import IP_ADDRESS   : Import IP address into the database")
        print("IP_ADDRESS               : Query the database for the specified IP address")
        print("No parameters            : Print help and number of records")

    record_count = get_record_count(conn)
    print(f"Number of Records: {record_count}")

    conn.close()

if __name__ == '__main__':
    main()
