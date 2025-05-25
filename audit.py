from datetime import datetime, timezone
from pymongo import MongoClient
from decimal import Decimal
from config import MONGO_URI
from flask import jsonify

client = MongoClient(MONGO_URI)
audit_db = client["audit_logs"]
audit_collection = audit_db["audits"]

def convert_decimals(obj):
    if isinstance(obj, dict):
        return {k: convert_decimals(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_decimals(i) for i in obj]
    elif isinstance(obj, Decimal):
        return float(obj)
    else:
        return obj

def audit_log(action, table, data_before=None, data_after=None, user=None):
    log = {
        "timestamp": datetime.now(timezone.utc),
        "action": action, 
        "table": table,
        "data_before": convert_decimals(data_before),
        "data_after": convert_decimals(data_after),
    }
    audit_collection.insert_one(log)

def audit_data(app):

    @app.route('/api/auditoria', methods=['GET'])
    def get_auditoria():
        try:
            logs = list(audit_collection.find().sort("timestamp", -1))  
            for log in logs:
                log['_id'] = str(log['_id'])  
                log['timestamp'] = log['timestamp'].isoformat()  
            return jsonify(logs), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

