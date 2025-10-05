"""
Initialize Workshop Booking Database
Creates SQLite database with stations, timeslots, and bookings tables

Author: Manus AI
Date: October 4, 2025
Version: 1.0
"""

import sqlite3
from datetime import datetime, timedelta

DATABASE = 'workshop_booking.db'

def init_database():
    """Initialize database with tables and seed data"""
    
    print("=" * 60)
    print("🔧 Initializing Workshop Booking Database")
    print("=" * 60)
    
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Drop existing tables
    print("\n📋 Dropping existing tables...")
    cursor.execute('DROP TABLE IF EXISTS bookings')
    cursor.execute('DROP TABLE IF EXISTS timeslots')
    cursor.execute('DROP TABLE IF EXISTS stations')
    print("✅ Existing tables dropped")
    
    # Create stations table
    print("\n📋 Creating stations table...")
    cursor.execute('''
        CREATE TABLE stations (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            tables INTEGER NOT NULL,
            time_per_person INTEGER NOT NULL,
            total_capacity INTEGER NOT NULL
        )
    ''')
    print("✅ Stations table created")
    
    # Create timeslots table
    print("\n📋 Creating timeslots table...")
    cursor.execute('''
        CREATE TABLE timeslots (
            slot_id TEXT PRIMARY KEY,
            station_id TEXT NOT NULL,
            round_number INTEGER NOT NULL,
            start_time TEXT NOT NULL,
            end_time TEXT NOT NULL,
            table_number INTEGER NOT NULL,
            is_available BOOLEAN DEFAULT TRUE,
            FOREIGN KEY (station_id) REFERENCES stations(id)
        )
    ''')
    print("✅ Timeslots table created")
    
    # Create bookings table
    print("\n📋 Creating bookings table...")
    cursor.execute('''
        CREATE TABLE bookings (
            booking_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            institution TEXT NOT NULL,
            position TEXT NOT NULL,
            slot_id TEXT NOT NULL,
            status TEXT DEFAULT 'confirmed',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (slot_id) REFERENCES timeslots(slot_id)
        )
    ''')
    print("✅ Bookings table created")
    
    # Insert stations
    print("\n📋 Inserting stations...")
    stations = [
        ('gem', 'GEM Coupler', 3, 10, 63),
        ('plate', 'OSSEOLAB Plate', 2, 20, 26),
        ('leica', 'Leica Microscope', 1, 20, 13)
    ]
    
    cursor.executemany(
        'INSERT INTO stations (id, name, tables, time_per_person, total_capacity) VALUES (?, ?, ?, ?, ?)',
        stations
    )
    print(f"✅ {len(stations)} stations inserted")
    
    # Generate timeslots
    print("\n📋 Generating timeslots...")
    
    # Workshop start time: 13:00
    workshop_start = datetime.strptime("13:00", "%H:%M")
    
    timeslot_count = 0
    
    for station_id, station_name, tables, time_per_person, _ in stations:
        # Calculate number of rounds
        total_minutes = 210  # 3.5 hours (13:00-16:30)
        rounds = total_minutes // time_per_person
        
        print(f"\n   🔹 {station_name}: {rounds} rounds × {tables} tables = {rounds * tables} slots")
        
        for round_num in range(1, rounds + 1):
            # Calculate start and end time
            start_offset = (round_num - 1) * time_per_person
            end_offset = round_num * time_per_person
            
            start_time = workshop_start + timedelta(minutes=start_offset)
            end_time = workshop_start + timedelta(minutes=end_offset)
            
            start_str = start_time.strftime("%H:%M")
            end_str = end_time.strftime("%H:%M")
            
            for table_num in range(1, tables + 1):
                slot_id = f"{station_id}_{round_num}_{table_num}"
                
                cursor.execute(
                    '''INSERT INTO timeslots 
                       (slot_id, station_id, round_number, start_time, end_time, table_number, is_available)
                       VALUES (?, ?, ?, ?, ?, ?, ?)''',
                    (slot_id, station_id, round_num, start_str, end_str, table_num, True)
                )
                
                timeslot_count += 1
    
    print(f"\n✅ {timeslot_count} timeslots generated")
    
    # Commit and close
    conn.commit()
    conn.close()
    
    print("\n" + "=" * 60)
    print("✅ Database initialized successfully!")
    print("=" * 60)
    
    # Print summary
    print("\n📊 Database Summary:")
    print(f"   Stations: {len(stations)}")
    print(f"   Timeslots: {timeslot_count}")
    print(f"   Total Capacity: 93 people")
    print(f"\n   Database file: {DATABASE}")
    print("\n🚀 Ready to start the server!")
    print("   Run: python3 app.py")
    print("=" * 60)

if __name__ == '__main__':
    init_database()
