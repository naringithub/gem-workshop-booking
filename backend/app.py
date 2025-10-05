"""
GEM Coupler Workshop - Booking System Backend API
Flask REST API for station booking management

Author: Manus AI
Date: October 4, 2025
Version: 1.0
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import hashlib
import datetime
import re

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend

# Database configuration
DATABASE = 'workshop_booking.db'

# ================================================================================
# DATABASE FUNCTIONS
# ================================================================================

def get_db_connection():
    """Create database connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def generate_booking_id():
    """Generate unique booking ID"""
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y%m%d%H%M%S")
    random_hash = hashlib.md5(timestamp.encode()).hexdigest()[:6]
    return f"BK{timestamp}{random_hash}".upper()

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone(phone):
    """Validate phone format"""
    pattern = r'^[0-9\-\s\+\(\)]{8,15}$'
    return re.match(pattern, phone) is not None

# ================================================================================
# API ENDPOINTS
# ================================================================================

@app.route('/')
def index():
    """API root endpoint"""
    return jsonify({
        "message": "GEM Coupler Workshop Booking API",
        "version": "1.0",
        "endpoints": {
            "GET /api/stations": "Get all stations info",
            "GET /api/timeslots": "Get available timeslots for a station",
            "POST /api/booking": "Create a new booking",
            "GET /api/booking/<booking_id>": "Get booking details",
            "DELETE /api/booking/<booking_id>": "Cancel a booking",
            "GET /api/stats": "Get booking statistics"
        }
    })

# --------------------------------------------------------------------------------
# GET /api/stations - Get all stations information
# --------------------------------------------------------------------------------

@app.route('/api/stations', methods=['GET'])
def get_stations():
    """Get all stations with availability"""
    try:
        conn = get_db_connection()
        
        # Get stations
        stations = conn.execute('SELECT * FROM stations').fetchall()
        
        result = []
        for station in stations:
            # Count available timeslots
            available_count = conn.execute(
                'SELECT COUNT(*) as count FROM timeslots WHERE station_id = ? AND is_available = 1',
                (station['id'],)
            ).fetchone()['count']
            
            result.append({
                "id": station['id'],
                "name": station['name'],
                "tables": station['tables'],
                "time_per_person": station['time_per_person'],
                "total_capacity": station['total_capacity'],
                "available": available_count,
                "booked": station['total_capacity'] - available_count,
                "percentage": round((station['total_capacity'] - available_count) / station['total_capacity'] * 100, 1)
            })
        
        conn.close()
        
        return jsonify({
            "success": True,
            "stations": result
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# --------------------------------------------------------------------------------
# GET /api/timeslots?station=<station_id> - Get available timeslots
# --------------------------------------------------------------------------------

@app.route('/api/timeslots', methods=['GET'])
def get_timeslots():
    """Get available timeslots for a station"""
    try:
        station_id = request.args.get('station')
        
        if not station_id:
            return jsonify({
                "success": False,
                "error": "Missing station parameter"
            }), 400
        
        conn = get_db_connection()
        
        # Get station info
        station = conn.execute(
            'SELECT * FROM stations WHERE id = ?',
            (station_id,)
        ).fetchone()
        
        if not station:
            conn.close()
            return jsonify({
                "success": False,
                "error": "Station not found"
            }), 404
        
        # Get timeslots
        timeslots = conn.execute(
            '''SELECT * FROM timeslots 
               WHERE station_id = ? 
               ORDER BY round_number, table_number''',
            (station_id,)
        ).fetchall()
        
        conn.close()
        
        result = []
        for slot in timeslots:
            result.append({
                "slot_id": slot['slot_id'],
                "round": slot['round_number'],
                "time": f"{slot['start_time']}-{slot['end_time']}",
                "table": slot['table_number'],
                "available": bool(slot['is_available'])
            })
        
        return jsonify({
            "success": True,
            "station": {
                "id": station['id'],
                "name": station['name']
            },
            "timeslots": result
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# --------------------------------------------------------------------------------
# POST /api/booking - Create a new booking
# --------------------------------------------------------------------------------

@app.route('/api/booking', methods=['POST'])
def create_booking():
    """Create a new booking"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'email', 'phone', 'institution', 'position', 'station', 'slot_id']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    "success": False,
                    "error": f"Missing required field: {field}"
                }), 400
        
        # Validate email
        if not validate_email(data['email']):
            return jsonify({
                "success": False,
                "error": "Invalid email format"
            }), 400
        
        # Validate phone
        if not validate_phone(data['phone']):
            return jsonify({
                "success": False,
                "error": "Invalid phone format"
            }), 400
        
        conn = get_db_connection()
        
        # Check if email already has a booking
        existing_booking = conn.execute(
            'SELECT * FROM bookings WHERE email = ? AND status = "confirmed"',
            (data['email'],)
        ).fetchone()
        
        if existing_booking:
            conn.close()
            return jsonify({
                "success": False,
                "error": "This email already has an active booking"
            }), 400
        
        # Check if timeslot is available
        timeslot = conn.execute(
            'SELECT * FROM timeslots WHERE slot_id = ?',
            (data['slot_id'],)
        ).fetchone()
        
        if not timeslot:
            conn.close()
            return jsonify({
                "success": False,
                "error": "Timeslot not found"
            }), 404
        
        if not timeslot['is_available']:
            conn.close()
            return jsonify({
                "success": False,
                "error": "Timeslot is no longer available"
            }), 400
        
        # Get station info
        station = conn.execute(
            'SELECT * FROM stations WHERE id = ?',
            (data['station'],)
        ).fetchone()
        
        # Generate booking ID
        booking_id = generate_booking_id()
        
        # Create booking
        conn.execute(
            '''INSERT INTO bookings 
               (booking_id, name, email, phone, institution, position, slot_id, status)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
            (booking_id, data['name'], data['email'], data['phone'], 
             data['institution'], data['position'], data['slot_id'], 'confirmed')
        )
        
        # Mark timeslot as unavailable
        conn.execute(
            'UPDATE timeslots SET is_available = 0 WHERE slot_id = ?',
            (data['slot_id'],)
        )
        
        conn.commit()
        conn.close()
        
        # Generate QR code URL
        qr_code_url = f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={booking_id}"
        
        return jsonify({
            "success": True,
            "booking_id": booking_id,
            "message": "จองสำเร็จ!",
            "details": {
                "station": station['name'],
                "time": f"{timeslot['start_time']}-{timeslot['end_time']}",
                "table": timeslot['table_number'],
                "qr_code": qr_code_url
            }
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# --------------------------------------------------------------------------------
# GET /api/booking/<booking_id> - Get booking details
# --------------------------------------------------------------------------------

@app.route('/api/booking/<booking_id>', methods=['GET'])
def get_booking(booking_id):
    """Get booking details"""
    try:
        conn = get_db_connection()
        
        # Get booking
        booking = conn.execute(
            '''SELECT b.*, t.start_time, t.end_time, t.table_number, s.name as station_name
               FROM bookings b
               JOIN timeslots t ON b.slot_id = t.slot_id
               JOIN stations s ON t.station_id = s.id
               WHERE b.booking_id = ?''',
            (booking_id,)
        ).fetchone()
        
        conn.close()
        
        if not booking:
            return jsonify({
                "success": False,
                "error": "Booking not found"
            }), 404
        
        # Generate QR code URL
        qr_code_url = f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={booking_id}"
        
        return jsonify({
            "success": True,
            "booking": {
                "booking_id": booking['booking_id'],
                "name": booking['name'],
                "email": booking['email'],
                "phone": booking['phone'],
                "institution": booking['institution'],
                "position": booking['position'],
                "station": booking['station_name'],
                "time": f"{booking['start_time']}-{booking['end_time']}",
                "table": booking['table_number'],
                "status": booking['status'],
                "created_at": booking['created_at'],
                "qr_code": qr_code_url
            }
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# --------------------------------------------------------------------------------
# DELETE /api/booking/<booking_id> - Cancel a booking
# --------------------------------------------------------------------------------

@app.route('/api/booking/<booking_id>', methods=['DELETE'])
def cancel_booking(booking_id):
    """Cancel a booking"""
    try:
        conn = get_db_connection()
        
        # Get booking
        booking = conn.execute(
            'SELECT * FROM bookings WHERE booking_id = ?',
            (booking_id,)
        ).fetchone()
        
        if not booking:
            conn.close()
            return jsonify({
                "success": False,
                "error": "Booking not found"
            }), 404
        
        if booking['status'] == 'cancelled':
            conn.close()
            return jsonify({
                "success": False,
                "error": "Booking already cancelled"
            }), 400
        
        # Cancel booking
        conn.execute(
            'UPDATE bookings SET status = "cancelled" WHERE booking_id = ?',
            (booking_id,)
        )
        
        # Mark timeslot as available again
        conn.execute(
            'UPDATE timeslots SET is_available = 1 WHERE slot_id = ?',
            (booking['slot_id'],)
        )
        
        conn.commit()
        conn.close()
        
        return jsonify({
            "success": True,
            "message": "ยกเลิกการจองสำเร็จ"
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# --------------------------------------------------------------------------------
# GET /api/stats - Get booking statistics
# --------------------------------------------------------------------------------

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get booking statistics"""
    try:
        conn = get_db_connection()
        
        # Total bookings
        total_bookings = conn.execute(
            'SELECT COUNT(*) as count FROM bookings WHERE status = "confirmed"'
        ).fetchone()['count']
        
        # Total capacity
        total_capacity = conn.execute(
            'SELECT SUM(total_capacity) as total FROM stations'
        ).fetchone()['total']
        
        # Bookings by station
        station_stats = conn.execute(
            '''SELECT s.name, s.total_capacity, 
               COUNT(b.booking_id) as booked
               FROM stations s
               LEFT JOIN timeslots t ON s.id = t.station_id
               LEFT JOIN bookings b ON t.slot_id = b.slot_id AND b.status = "confirmed"
               GROUP BY s.id, s.name, s.total_capacity'''
        ).fetchall()
        
        conn.close()
        
        stations = []
        for stat in station_stats:
            stations.append({
                "name": stat['name'],
                "total": stat['total_capacity'],
                "booked": stat['booked'],
                "available": stat['total_capacity'] - stat['booked'],
                "percentage": round(stat['booked'] / stat['total_capacity'] * 100, 1)
            })
        
        return jsonify({
            "success": True,
            "stats": {
                "total_bookings": total_bookings,
                "total_capacity": total_capacity,
                "available": total_capacity - total_bookings,
                "percentage": round(total_bookings / total_capacity * 100, 1),
                "stations": stations
            }
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# ================================================================================
# RUN SERVER
# ================================================================================

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
