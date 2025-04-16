from mysql.connector import Error

def create_mysql_database(cursor, database_name):
    cursor.execute("CREATE DATABASE IF NOT EXISTS {}".format(database_name))
    print("=================Database {} created=================".format(database_name))

def execute_sql_file(cursor, sql_file_path):
    with open(sql_file_path, "r") as sql_file:
        sql_script = sql_file.read()

    sql_commands = [command.strip() for command in sql_script.split(";") if command.strip()]

    for command in sql_commands:
        try:
            cursor.execute(command)
            print(f"Executed {command.strip()[:50]} SQL commands")
        except Error as e:
            print("------------------Error executing SQL commands------------------", e)
            raise