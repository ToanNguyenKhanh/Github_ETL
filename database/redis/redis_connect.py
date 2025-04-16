import redis
from redis.exceptions import ConnectionError
from config.database_config import get_database_config
from database.redis.redis_manager import store_redis_data
class RedisConnect:
    def __init__(self, host, port, password):
        self.host = host
        self.port = port
        self.password = password
        self.connection = None

    def connect(self):
        try:
            self.connection = redis.Redis(
                host=self.host,
                port=self.port,
                password=self.password
            )
            self.connection.ping()
            return self.connection
        except ConnectionError as e:
            raise Exception(f"---------- Failed to connect to Redis: {e} ----------")

    def close(self):
        self.connection.close()
        self.connection = None
        print("---------- Connection closed ----------")

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()



if __name__ == "__main__":
    configRedis= get_database_config()["redis"]
    host = configRedis.host
    port = configRedis.port
    password = configRedis.password

    user_data = {
        "user_id": 1,
        "login": "jsonmurphy",
        "gravatar_id": "",
        "gravatar_url": "https://avatars.githubusercontent.com/u/1843574?",
        "url": "https://api.github.com/users/jsonmurphy",
    }

    with RedisConnect(host, port, password) as redis_client:
        print(f'---------- Redis connection established: {redis_client} ----------')
        store_redis_data(redis_client, user_data)





