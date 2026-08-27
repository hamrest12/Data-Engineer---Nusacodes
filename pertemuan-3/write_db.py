import os
import pandas as pd
from sqlalchemy import create_engine, text
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('write_db.log'),
        logging.StreamHandler()
    ]
)

PG_USER = 'postgres'
PG_PASSWORD = 'adminpass123'
PG_DATABASE = 'tes_postgres'
PG_PORT = '5432'
PG_HOST = 'localhost'

pg_engine = create_engine(f"postgresql+psycopg2://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DATABASE}")

Dataset_mapping = [
    ("dim_costumers", "olist_costumers_dataset.csv", "public.dim_costumers", "DIM"),
    ("dim_geolocation", "olist_geolocation_dataset.csv", "public.dim_geolocation", "DIM"),
    ("dim_order_payments", "olist_order_payments_dataset.csv", "public.dim_order_payments", "DIM"),
    ("dim_products", "olist_products_dataset.csv", "public.dim_products", "DIM"),
    ("dim_sellers", "olist_sellers_dataset.csv", "public.dim_sellers", "DIM"),
    ("dim_product_category_name_translation", "product_category_name_translation.csv", "public.dim_product_category_name_translation", "DIM"),
    ("fact_order_items", "olist_order_items_dataset.csv", "public.fact_order_items", "FACT"),
    ("fact_order_reviews", "olist_order_reviews_dataset.csv", "public.fact_order_reviews", "FACT"),
    ("fact_orders", "olist_orders_dataset.csv", "public.fact_orders", "FACT")
]

ARCHIVE_DIR = os.path.join(os.path.dirname(__file__), "archive")

def drop_table_if_exist(engine, table_name: str):
    with engine.connect() as conn:
        conn.execute(text(f"DROP TABLE IF EXISTS {table_name} CASCADE;"))
        logging.info(f"✅ Tabel {table_name} berhasil dihapus jika sudah ada")
        conn.commit()
        logging.info(f"Tabel {table_name} Berhasil dihapus jika sudah ada")


def ingest_csv_to_postgres():
    logging.info("Starting CSV Ingestion to PostgressSQL....")

    try:
        engine = pg_engine
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

            drop_table_if_exist(engine, table_name)

            df.to_sql(
                name=label,
                con=engine,
                schema=table_name.split('.')[0],
                if_exists='replace',
                index=False,
                chunksize=1000
            )
        except Exception as e:
            logging.error(f"❌ Failed to ingest {csv_file} into postgress: {e}")
if __name__ == "__main__":
    ingest_csv_to_postgres()
    logging.info("CSV Ingestion to PostgresSQL completed")