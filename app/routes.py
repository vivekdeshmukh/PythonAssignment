from flask import request, jsonify
from app import app, db
from app.models import Member, Inventory, Booking
import pandas as pd
from datetime import datetime

MAX_BOOKINGS = 2

@app.route('/', methods=['GET'])
@app.route('/get_members', methods=['GET'])
def get_all_members():
    members = Member.query.all()  # Get all members from the database
    return jsonify([member.to_dict() for member in members])  # Convert each member to a dictionary and return as JSON

@app.route('/get_inventories', methods=['GET'])
def get_all_inventories():
    inventories = Inventory.query.all()
    return jsonify([inv.to_dict() for inv in inventories])
    
@app.route('/upload_members', methods=['POST'])
def upload_members():
    file = request.files['file']
    df = pd.read_csv(file)

    for _, row in df.iterrows():
        member = Member(
            name=row['name'],
            surname=row['surname'],
            booking_count=row['booking_count'],
            date_joined=datetime.strptime(row['date_joined'], "%Y-%m-%d %H:%M:%S")
        )
        db.session.add(member)
    db.session.commit()
    return jsonify({"message": "Members uploaded successfully"}), 200

@app.route('/upload_inventory', methods=['POST'])
def upload_inventory():
    file = request.files['file']
    df = pd.read_csv(file)
    
    for _, row in df.iterrows():
        inventory = Inventory(
            title=row['title'],
            description=row['description'],
            remaining_count=row['remaining_count'],
            expiration_date=datetime.strptime(row['expiration_date'], '%d/%m/%Y')
        )
        db.session.add(inventory)
    db.session.commit()
    return jsonify({"message": "Inventory uploaded successfully"}), 200

@app.route('/book', methods=['POST'])
def book():
    member_id = request.json['member_id']
    inventory_id = request.json['inventory_id']
    
    member = Member.query.get(member_id)
    inventory = Inventory.query.get(inventory_id)
    
    if not member or not inventory:
        return jsonify({"message": "Invalid member or inventory"}), 400

    # Check booking count limit and remaining inventory
    if member.booking_count >= MAX_BOOKINGS:
        return jsonify({"message": "Booking limit reached"}), 400
    
    if inventory.remaining_count <= 0:
        return jsonify({"message": "No inventory available"}), 400

    # Create booking
    booking = Booking(member_id=member.id, inventory_id=inventory.id)
    db.session.add(booking)
    
    # Update member booking count and inventory remaining count
    member.booking_count += 1
    inventory.remaining_count -= 1
    db.session.commit()

    return jsonify({"message": "Booking successful", "booking_id": booking.id}), 200

@app.route('/cancel', methods=['POST'])
def cancel():
    booking_id = request.json['booking_id']
    booking = Booking.query.get(booking_id)
    
    if not booking:
        return jsonify({"message": "Booking not found"}), 400
    
    # Update member and inventory
    booking.member.booking_count -= 1
    booking.inventory.remaining_count += 1
    db.session.delete(booking)
    db.session.commit()

    return jsonify({"message": "Booking canceled successfully"}), 200
