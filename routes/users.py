from fastapi import APIRouter, Query
from database.setup import mongo_client

user = APIRouter()


@user.get("/logs")
async def get_all_logs(page: int = Query(1, alias="page"), page_size: int = Query(10, alias="page_size")):
    db = mongo_client["face_recognition_db"]
    data = None
    try:
        logs_collection = db["logs"]
        total_logs = logs_collection.count_documents({})
        logs = logs_collection.find().skip((page - 1) * page_size).limit(page_size)
        logs_list = []

        for log in logs:
            # Convert ObjectId to string
            log['_id'] = str(log['_id'])
            log_data = {
                "id": log['_id'],
                # Get the 'name' field or default to 'Unknown'
                "name": log.get('name', 'Unknown'),
                # Get 'entry_time' field or default to 'N/A'
                "timestamp": log.get('timestamp', 'N/A'),
                # get 'image' field or default to 'N/A'
                "image": log.get('image', 'N/A'),
            }
            logs_list.append(log_data)

        data = logs_list
    except Exception as e:
        print(e)
    return {
        'data': data,
        'total': total_logs,
        'page': page,
        'page_size': page_size,
        'total_pages': (total_logs + page_size - 1) // page_size
    }


@user.get("/warnings")
async def get_all_warnings(page: int = Query(1, alias="page"), page_size: int = Query(10, alias="page_size")):
    db = mongo_client["face_recognition_db"]
    data = None
    try:
        logs_collection = db["warnings"]
        total_logs = logs_collection.count_documents({})
        logs = logs_collection.find().skip((page - 1) * page_size).limit(page_size)
        logs_list = []

        for log in logs:
            # Convert ObjectId to string
            log['_id'] = str(log['_id'])
            log_data = {
                "id": log['_id'],
                # Get the 'name' field or default to 'Unknown'
                "name": log.get('name', 'Unknown'),
                # Get 'entry_time' field or default to 'N/A'
                "timestamp": log.get('timestamp', 'N/A'),
                # get 'image' field or default to 'N/A'
                "image": log.get('image', 'N/A'),
            }
            logs_list.append(log_data)

        data = logs_list
    except Exception as e:
        print(e)
    return {
        'data': data,
        'total': total_logs,
        'page': page,
        'page_size': page_size,
        'total_pages': (total_logs + page_size - 1) // page_size
    }


@user.post("/create_statement_light")
async def create_statement_light():
    db = mongo_client["face_recognition_db"]
    try:
        logs_collection = db["statements"]
        data = {
            "name": "Light",
            "state": "true"
        }
        logs_collection.insert_one(data)
    except Exception as e:
        print(e)
    return {
        'status': 'success'
    }


@user.post("/create_statement_door")
async def create_statement_door():
    db = mongo_client["face_recognition_db"]
    try:
        logs_collection = db["statements"]
        data = {
            "name": "Door",
            "state": "true"
        }
        logs_collection.insert_one(data)
    except Exception as e:
        print(e)
    return {
        'status': 'success'
    }


@user.get("/get_statement_light")
async def get_statement_light():
    db = mongo_client["face_recognition_db"]
    data = None
    try:
        logs_collection = db["statements"]
        data = logs_collection.find_one({"name": "Light"})
    except Exception as e:
        print(e)
    return {
        'data': data.get('state')
    }


@user.get("/get_statement_door")
async def get_statement_door():
    db = mongo_client["face_recognition_db"]
    data = None
    try:
        logs_collection = db["statements"]
        data = logs_collection.find_one({"name": "Door"})
    except Exception as e:
        print(e)
    return {
        'data': data.get('state')
    }


@user.post("/toogle_statement_light")
async def toogle_statement_light():
    db = mongo_client["face_recognition_db"]
    try:
        logs_collection = db["statements"]
        data = logs_collection.find_one({"name": "Light"})
        state = data.get('state')
        new_state = "false" if state == "true" else "true"
        logs_collection.update_one(
            {"name": "Light"}, {"$set": {"state": new_state}})
    except Exception as e:
        print(e)
    return {
        'data': new_state
    }


@user.post("/toogle_statement_door")
async def toogle_statement_door():
    db = mongo_client["face_recognition_db"]
    try:
        logs_collection = db["statements"]
        data = logs_collection.find_one({"name": "Door"})
        state = data.get('state')
        new_state = "false" if state == "true" else "true"
        logs_collection.update_one(
            {"name": "Door"}, {"$set": {"state": new_state}})
    except Exception as e:
        print(e)
    return {
        'data': new_state
    }
