import psycopg2 as sql
import pandas as pd
import os
import sys
import dotenv
src_file = os.path.dirname(__file__)
project_root = os.path.dirname(src_file)
dataset = os.path.join(project_root,'Dataset')

dotenv.load_dotenv()

db_host = os.getenv('DB_HOST')
db_name = os.getenv('DB_NAME')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')

customers_file = os.path.join(dataset,'customers_dataset.csv' )
geolocation_file = os.path.join(dataset,'geolocation_dataset.csv')
order_items_file = os.path.join(dataset,'order_items_dataset.csv')
order_payments_file = os.path.join(dataset,'order_payments_dataset.csv')
order_reviews_file = os.path.join(dataset,'order_reviews_dataset.csv')
orders_file = os.path.join(dataset,'orders_dataset.csv')
product_category_name_translation_file = os.path.join(dataset,'product_category_name_translation.csv')
product_file = os.path.join(dataset,'products_dataset.csv')
sellers_file = os.path.join(dataset,'sellers_dataset.csv')


try:
    conn = sql.connect(database=db_name, user= db_user, password=db_password ,host=db_host )
    print('connection successful')
    cur = conn.cursor()
    try:
        with open(customers_file,"r", encoding="utf-8", newline="") as c:
            cur.copy_expert("COPY customers(customer_id,customer_unique_id," \
            "customer_zip_code_prefix,customer_city,customer_state) " \
            "FROM STDIN WITH (FORMAT CSV, NULL '' ,HEADER",c)
            conn.commit()
            print("customers Table Loaded")

        with open(geolocation_file,"r", encoding="utf-8", newline="") as g:
            cur.copy_expert('''COPY geolocation (geolocation_zip_code_prefix,
            geolocation_lat,geolocation_lng,geolocation_city,geolocation_state) FROM STDIN 
            WITH (FORMAT CSV, NULL '', HEADER )''',g)
            conn.commit()
            print('Geolocation Table Loaded')

        with open(order_items_file,'r', encoding="utf-8", newline="") as oi:
            cur.copy_expert('''COPY order_items(order_id,order_item_id,product_id,
            seller_id,shipping_limit_date,price,freight_value) FROM STDIN WITH 
            (FORMAT CSV, NULL '', HEADER )''',oi)
            conn.commit()
            print('Order Items Table loaded')

        with open(order_payments_file,'r', encoding="utf-8", newline="") as op:
            cur.copy_expert('''COPY order_payments(order_id,payment_sequential,
            payment_type,payment_installments,payment_value) FROM STDIN WITH 
            (FORMAT CSV, NULL '',HEADER )''',op)
            conn.commit()
            print('Order Payments Table Loaded')

        with open(order_reviews_file,'r', encoding="utf-8", newline="") as ors:
            cur.copy_expert('''COPY orders_reviews (review_id,order_id,review_score,
            review_comment_title,review_comment_message,review_creation_date,
            review_answer_timestamp) FROM STDIN WITH (FORMAT CSV, NULL '',HEADER )''',ors)
            conn.commit()
            print('Orders Reviews Table Loaded')

        with open(orders_file,'r', encoding="utf-8", newline="") as o:
            cur.copy_expert(''' COPY orders (order_id,customer_id,order_status,
            order_purchase_timestamp,order_approved_at,order_delivered_carrier_date,
            order_delivered_customer_date,order_estimated_delivery_date) FROM STDIN
            WITH (FORMAT CSV,NULL '',HEADER )''',o) 
            conn.commit()
            print("Orders Table Loaded")

        with open(product_category_name_translation_file,'r', encoding="utf-8", newline="") as pcnt:
            cur.copy_expert('''COPY product_cat_tran_eng (product_category_name,
            product_category_name_english)FROM STDIN WITH(FORMAT CSV,NULL '',HEADER )
            ''',pcnt)
            conn.commit()
            print('Product trans Table Loaded')

        with open(product_file,'r', encoding="utf-8", newline="") as p:
            cur.copy_expert(''' COPY products (product_id,product_category_name,
            product_name_length,product_description_length,product_photos_qty,
            product_weight_g,product_length_cm,product_height_cm,product_width_cm)
            FROM STDIN WITH (FORMAT CSV,NULL '',HEADER )''',p)
            conn.commit()
            print('Product Table Loaded')

        with open(sellers_file,"r", encoding="utf-8", newline="") as s:
            cur.copy_expert('''COPY sellers (seller_id,seller_zip_code_prefix,seller_city,
            seller_state) FROM STDIN WITH (FORMAT CSV, NULL '',HEADER )''',s)
            conn.commit()
            print('Seller Table Loaded')
        print('All files Loaded')
        cur.close()
        conn.close()
        print('Connection Closed')
    except Exception as e :
        print('Error' ,e)
        conn.close()
except sql.Error as e:
    print('Connection Failed due to erroe ', e)

