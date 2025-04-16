from typing import Optional
import os
from pyspark.sql import SparkSession

def create_spark_session(
        app_name: str,
        master_url: str = "local[*]",
        executor_memory: Optional[str] = "4g",
        executor_cores: Optional[int] = 2,
        driver_memory: Optional[str] = "2g",
        num_executors: Optional[int] = 3,
        jars: Optional[list[str]] = None,
        spark_conf: Optional[dict[str, str]] = None,
        log_lever: str = "WARN"
) -> SparkSession:

    builder = SparkSession.builder \
        .appName(app_name) \
        .master(master_url)

    if executor_memory:
        builder.config("spark.executor.memory", executor_memory)
    if executor_cores:
        builder.config("spark.executor.cores", executor_cores)
    if driver_memory:
        builder.config("spark.driver.memory", driver_memory)
    if num_executors:
        builder.config("spark.executor.num_executors", num_executors)
    if jars:
        jars_path = ",".join([os.path.abspath(jar) for jar in jars])
        builder.config("spark.jars", jars_path)

    if spark_conf:
        for key, value in spark_conf.items():
            builder.config(key, value)

    spark = builder.getOrCreate()

    spark.sparkContext.setLogLevel(log_lever)

    return spark

def connect_to_mysql(spark: SparkSession, config: dict[str, str], table_name: str):
    df = spark.read \
        .format("jdbc") \
        .option("url", "jdbc:mysql://172.17.0.2:3306/github_data") \
        .option("dbtable", table_name) \
        .option("user", config["user"]) \
        .option("password", config["password"]) \
        .option("driver", "com.mysql.cj.jdbc.Driver") \
        .load()
    return df



