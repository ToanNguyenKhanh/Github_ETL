import redis
from redis.exceptions import RedisError
from jsonschema import validate, ValidationError

# JSON schema để đảm bảo dữ liệu hợp lệ trước khi lưu vào Redis
USER_SCHEMA = {
    "type": "object",
    "required": ["user_id", "login"],
    "properties": {
        "user_id": {"type": "integer"},
        "login": {"type": "string"},
        "gravatar_id": {"type": ["string", "null"]},
        "gravatar_url": {"type": ["string", "null"]},
        "url": {"type": ["string", "null"]}
    }
}

def store_redis_data(redis_client, user_data):
    try:
        # Validate schema
        validate(instance=user_data, schema=USER_SCHEMA)

        key = f"user:{user_data['user_id']}"

        # Nếu key tồn tại nhưng không phải kiểu hash → xóa để tránh lỗi
        if redis_client.connection.exists(key):
            redis_type = redis_client.connection.type(key)
            if redis_type != b'hash':
                redis_client.connection.delete(key)

        stringified_data = {k: '' if v is None else str(v) for k, v in user_data.items()}
        redis_client.connection.hset(key, mapping=stringified_data)

        print(f"----------Stored user in Redis: {key}----------")

    except ValidationError as ve:
        raise Exception(f"----------Schema validation failed: {ve.message}----------")
    except RedisError as re:
        raise Exception(f"----------Redis operation failed: {re}----------")
