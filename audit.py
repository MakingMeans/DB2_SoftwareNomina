from datetime import datetime, timezone
from pymongo import MongoClient
from decimal import Decimal
from config import MONGO_URI

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
