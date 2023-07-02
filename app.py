from flask import Flask, request, jsonify
from uuid import uuid4
import datetime
from marshmallow import Schema, fields, validate, ValidationError, validates
import math

app = Flask(__name__)

# Store receipts in memory as instructed; otherwise, should be saved to database like sqlalchemy 
receipts = {}

# Schemas for input validation
class ItemSchema(Schema):
    shortDescription = fields.Str(required=True, validate=validate.Regexp("^[\\w\\s\\-]+$"))
    price = fields.Str(required=True, validate=validate.Regexp("^\\d+\\.\\d{2}$"))

class ReceiptSchema(Schema):
    retailer = fields.Str(required=True, validate=validate.Regexp("^[\w\s&'-]+$"))
    purchaseDate = fields.Str(required=True, validate=validate.Regexp("^\d{4}-\d{2}-\d{2}$"))
    purchaseTime = fields.Str(required=True, validate=validate.Regexp("^\d{2}:\d{2}$"))
    total = fields.Str(required=True, validate=validate.Regexp("^\\d+\\.\\d{2}$"))
    items = fields.List(fields.Nested(ItemSchema), required=True, validate=validate.Length(min=1))  



receipt_schema = ReceiptSchema()

@app.route('/receipts/process', methods=['POST'])
def process_receipt():
    try:
        data = receipt_schema.load(request.get_json())
        data['purchaseDate'] = datetime.datetime.strptime(data['purchaseDate'], '%Y-%m-%d').date()
        data['purchaseTime'] = datetime.datetime.strptime(data['purchaseTime'], '%H:%M').time()
        data['total'] = float(data['total'])
        for item in data['items']:
            item['price'] = float(item['price'])
    except ValidationError as err:
        return jsonify(err.messages), 400

    # Count the points.
    points = calculate_points(data)
    data['points'] = points

    # Save the receipt and items to the receipts dictionary
    receipt_id = str(uuid4())
    receipts[receipt_id] = data

    # Return receipt ID in .json.
    return jsonify({ 'id': receipt_id }), 200

@app.route('/receipts/<id>/points', methods=['GET'])
def get_points(id):
    receipt = receipts.get(id)
    if receipt is None:
        return jsonify({ 'error': 'Receipt not found' }), 404

    return jsonify({ 'points': receipt['points'] }), 200

def calculate_points(receipt):
    points = 0
    retailer_points = len([char for char in receipt['retailer'] if char.isalnum()])
    points += retailer_points

    total = receipt['total']

    if total.is_integer():
        points += 50

    if total % 0.25 == 0:
        points += 25

    item_points = len(receipt['items']) // 2 * 5
    points += item_points

    for item in receipt['items']:
        item_desc_len = len(item['shortDescription'].strip())
        if item_desc_len % 3 == 0:
            price_points = math.ceil(item['price'] * 0.2)
            points += price_points

    purchase_date = receipt['purchaseDate']
    if purchase_date.day % 2 != 0:
        points += 6

    purchase_time = receipt['purchaseTime']
    if datetime.time(14, 0) <= purchase_time <= datetime.time(16, 0):
        points += 10

    return points

if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)