CREATE TABLE IF NOT EXISTS customers(
    customer_ID VARCHAR(225),
    customer_unique_ID VARCHAR(225),
    customer_zip_code_prefix VARCHAR(50),
    customer_city VARCHAR(225),
    customer_state VARCHAR(225)
  );

CREATE TABLE IF NOT EXISTS geolocation(
  geolocation_zip_code_prefix VARCHAR(50),
  geolocation_lat VARCHAR(225),
  geolocation_lng VARCHAR(225),
  geolocation_city VARCHAR(225),
  geolocation_state VARCHAR(225)
);

CREATE TABLE IF NOT EXISTS order_items(
  order_ID VARCHAR(225),
  order_item_ID VARCHAR(10),
  product_ID VARCHAR(225),
  seller_ID VARCHAR(225),
  shipping_limit_date TIMESTAMP,
  price FLOAT,
  freight_value FLOAT
  );

CREATE TABLE IF NOT EXISTS order_payments(
  order_ID VARCHAR(225),
  payment_sequential VARCHAR(225),
  payment_type VARCHAR(225),
  payment_installments INT,
  payment_value FLOAT
);

CREATE TABLE IF NOT EXISTS orders_reviews(
  review_ID VARCHAR(225),
  order_ID VARCHAR(225),
  review_score VARCHAR(225),
  review_comment_title VARCHAR(225),
  review_comment_message VARCHAR(225),
  review_creation_date TIMESTAMP,
  review_answer_timestamp TIMESTAMP
);

CREATE TABLE IF NOT EXISTS orders(
  order_ID VARCHAR(225),
  customer_ID VARCHAR(225),
  order_status VARCHAR(225),
  order_purchase_timestamp TIMESTAMP,
  order_approved_at TIMESTAMP,
  order_delivered_carrier_date TIMESTAMP,
  order_delivered_customer_date TIMESTAMP,
  order_estimated_delivery_date TIMESTAMP
);

CREATE TABLE IF NOT EXISTS product_cat_tran_eng(
  product_category_name VARCHAR(225),
  product_category_name_english VARCHAR(225)
);

CREATE TABLE IF NOT EXISTS products(
  product_ID VARCHAR(225),
  product_category_name VARCHAR(225),
  product_name_length INT,
  product_description_length INT,
  product_photos_qty INT,
  product_weight_g INT,
  product_length_cm INT,
  product_height_cm INT,
  product_width_cm INT
);

CREATE TABLE IF NOT EXISTS sellers(
  seller_ID VARCHAR(225),
  seller_zip_code_prefix VARCHAR(225),
  seller_city VARCHAR(225),
  seller_state VARCHAR(225)
);