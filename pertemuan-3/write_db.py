import os
import pandas as pd
import clickhouse_connect
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('write_db.log'),
        logging.StreamHandler()
    ]
)

CH_USER = 'clickhouse'
CH_PASSWORD = 'adminpass123'
CH_DATABASE = 'tes_clickhouse'
CH_PORT = '8123'
CH_HOST = 'localhost'

def get_clickhouse_client():
    return clickhouse_connect.get_client(
        host=CH_HOST,
        port=CH_PORT,
        username=CH_USER,
        password=CH_PASSWORD,
        database=CH_DATABASE
    )

Dataset_mapping = [
    ("dim_costumers", "olist_customers_dataset.csv", "dim_costumers", "DIM"),
    ("dim_geolocation", "olist_geolocation_dataset.csv", "dim_geolocation", "DIM"),
    ("dim_order_payments", "olist_order_payments_dataset.csv", "dim_order_payments", "DIM"),
    ("dim_products", "olist_products_dataset.csv", "dim_products", "DIM"),
    ("dim_sellers", "olist_sellers_dataset.csv", "dim_sellers", "DIM"),
    ("dim_product_category_name_translation", "product_category_name_translation.csv", "dim_product_category_name_translation", "DIM"),
    ("fact_order_items", "olist_order_items_dataset.csv", "fact_order_items", "FACT"),
    ("fact_order_reviews", "olist_order_reviews_dataset.csv", "fact_order_reviews", "FACT"),
    ("fact_orders", "olist_orders_dataset.csv", "fact_orders", "FACT")
]

ARCHIVE_DIR = os.path.join(os.path.dirname(__file__), "archive")

def drop_table_if_exist(client, table_name: str):
    client.command(f"DROP TABLE IF EXISTS {table_name}")
    logging.info(f"✅ Tabel {table_name} berhasil dihapus jika sudah ada")

def create_table_from_df(client, table_name: str, df: pd.DataFrame):
    columns_structure = []

    for col_name, dtype in df.dtypes.items():
        if "int" in str(dtype):
            ch_type = "Nullable(Int64)"
        elif "float" in str(dtype):
            ch_type = "Nullable(Float64)"
        elif "datetime" in str(dtype) or "date" in str(dtype):
            ch_type = "Nullable(DateTime)"
        else:
            ch_type = "Nullable(String)"

        columns_structure.append(f"`{col_name}` {ch_type}")

    column_str = ", ".join(columns_structure)

    create_query = f"""
    CREATE TABLE IF NOT EXISTS {table_name}({column_str})
    ENGINE = MergeTree()
    ORDER BY tuple();
    """
    client.command(create_query)
    logging.info(f"✅ Tabel {table_name} berhasil dibuat dengan skema otomatis")
        

def ingest_csv_to_clickhouse():
    logging.info("Starting CSV Ingestion to Clickhouse....")

    try:
        client = get_clickhouse_client()
        logging.info(f"✅ Database connection estabilished sucessfully")
    except Exception as e:
        logging.error(f"❌ Failed to connect to Database: {e}")
        return

    for label, csv_file, table_name, tabel_type in Dataset_mapping:
        csv_path = os.path.join(ARCHIVE_DIR, csv_file)
        logging.info(f"Processing {csv_file} for table {table_name} ({tabel_type})")
        try:
            df = pd.read_csv(csv_path)
            logging.info(f"✅ Successfully Read {csv_file} into Dataframe")

            df = df.where(pd.notnull(df),None)

            drop_table_if_exist(client, table_name)

            create_table_from_df(client, table_name, df)

            client.insert_df(
                table=table_name,
                df=df
            )
            logging.info(f"✅ Successfully ingested {csv_file} into Clickhouse table {table_name}")

        except Exception as e:
            logging.error(f"❌ Failed to ingest {csv_file} into clickhouse: {e}")

if __name__ == "__main__":
    ingest_csv_to_clickhouse()
    logging.info("CSV Ingestion to Clickhouse completed")