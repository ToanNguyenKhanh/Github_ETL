from database.mongoDB.mongodb_connect import MongoDBConnect
from config.database_config import get_database_config
from database.mongoDB.mongo_manager import create_mongodb_schema, validate_mongodb_schema
from database.mysql.sql_manager import create_mysql_database, execute_sql_file
from database.mysql.mysql_connect import MysqlConnect
from pathlib import Path
from database.redis.redis_connect import RedisConnect
from database.redis.redis_manager import store_redis_data


def main():
    try:
        # Load config
        config = get_database_config()
        print(f"Config loaded: {config}")

        user_data = {
            "user_id": 1,
            "login": "jsonmurphy",
            "gravatar_id": "",
            "gravatar_url": "https://avatars.githubusercontent.com/u/1843574?",
            "url": "https://api.github.com/users/jsonmurphy",
        }
        # MongoDB
        print("Connecting to MongoDB...")
        with MongoDBConnect(config["mongodb"].uri, config["mongodb"].db_name) as mongo_client:
            print("MongoDB connected")
            create_mongodb_schema(mongo_client.connect())
            print("----------Inserting to MongoDB----------", flush=True)
            mongo_client.db.Users.insert_one(user_data)
            validate_mongodb_schema(mongo_client.db)

        # Redis
        print("Connecting to Redis...")
        configRedis = get_database_config()["redis"]
        redis_host = configRedis.host
        redis_port = configRedis.port
        redis_password = configRedis.password

        with RedisConnect(redis_host, redis_port, redis_password) as redis_client:
            print("Redis connected")
            store_redis_data(redis_client, user_data)

        # MySQL
        print("Connecting to MySQL...")
        SQL_FILE_PATH = Path("/home/toan/PycharmProjects/Github_ETL/database/mysql/schema.sql")
        print(f"SQL file exists: {SQL_FILE_PATH.exists()}")
        if not SQL_FILE_PATH.exists():
            raise FileNotFoundError(f"SQL file not found: {SQL_FILE_PATH}")

        mysql_config = config["mysql"]
        mysql_conn_config = {
            "host": mysql_config.host,
            "port": mysql_config.port,
            "user": mysql_config.user,
            "password": mysql_config.password,
            "database": mysql_config.database
        }
        print(f"Connecting to MySQL with config: {mysql_conn_config}")
        with MysqlConnect(mysql_conn_config) as mysql_client:
            cursor = mysql_client.cursor
            create_mysql_database(cursor, mysql_conn_config["database"])
            execute_sql_file(cursor, SQL_FILE_PATH)
            mysql_client.connection.commit()
            print("MySQL operations completed")
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise

if __name__ == "__main__":
    main()