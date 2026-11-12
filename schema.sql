-- Olist mini dataset (500 orders) - MySQL 8 schema with PRIMARY and FOREIGN KEYS
-- Run this whole file first, then the LOAD DATA section (or use Workbench's Table Data Import Wizard).
CREATE DATABASE IF NOT EXISTS olist_mini;
USE olist_mini;
SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS geolocation, order_reviews, order_payments, order_items, orders, customers, products, sellers, product_category_name_translation;
SET FOREIGN_KEY_CHECKS = 1;

-- zip prefix repeats many times here (several lat/lng rows per prefix), so it cannot be a PK or an FK target.
-- geolocation_id is a surrogate PK added for this practice set. Joining customers/sellers to it ON zip prefix
-- multiplies rows (join fan-out) - good pitfall practice.
CREATE TABLE geolocation (
  geolocation_id              INT PRIMARY KEY,
  geolocation_zip_code_prefix VARCHAR(5),
  geolocation_lat             DOUBLE,
  geolocation_lng             DOUBLE,
  geolocation_city            VARCHAR(60),
  geolocation_state           CHAR(2),
  INDEX idx_geo_zip (geolocation_zip_code_prefix)
);

-- PARENT (lookup) TABLES ------------------------------------------------------
CREATE TABLE product_category_name_translation (
  product_category_name          VARCHAR(80) PRIMARY KEY,
  product_category_name_english  VARCHAR(80)
);

CREATE TABLE customers (
  customer_id               CHAR(32) PRIMARY KEY,
  customer_unique_id        CHAR(32) NOT NULL,   -- same person can have several customer_id
  customer_zip_code_prefix  VARCHAR(5),
  customer_city             VARCHAR(60),
  customer_state            CHAR(2)
);

CREATE TABLE sellers (
  seller_id                CHAR(32) PRIMARY KEY,
  seller_zip_code_prefix   VARCHAR(5),
  seller_city              VARCHAR(60),
  seller_state             CHAR(2)
);

-- product_category_name has NULLs and a few names with no translation, so it is NOT enforced as an FK
-- (join on it with LEFT JOIN - that is task 7). 
CREATE TABLE products (
  product_id                  CHAR(32) PRIMARY KEY,
  product_category_name       VARCHAR(80),
  product_name_lenght         INT,
  product_description_lenght  INT,
  product_photos_qty          INT,
  product_weight_g            INT,
  product_length_cm           INT,
  product_height_cm           INT,
  product_width_cm            INT
);

-- CHILD TABLES ----------------------------------------------------------------
CREATE TABLE orders (
  order_id                       CHAR(32) PRIMARY KEY,
  customer_id                    CHAR(32) NOT NULL,
  order_status                   VARCHAR(20),
  order_purchase_timestamp       DATETIME,
  order_approved_at              DATETIME,
  order_delivered_carrier_date   DATETIME,
  order_delivered_customer_date  DATETIME,
  order_estimated_delivery_date  DATETIME,
  FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE order_items (               -- composite PK: one row per item in an order
  order_id             CHAR(32) NOT NULL,
  order_item_id        INT NOT NULL,
  product_id           CHAR(32) NOT NULL,
  seller_id            CHAR(32) NOT NULL,
  shipping_limit_date  DATETIME,
  price                DECIMAL(10,2),
  freight_value        DECIMAL(10,2),
  PRIMARY KEY (order_id, order_item_id),
  FOREIGN KEY (order_id)   REFERENCES orders(order_id),
  FOREIGN KEY (product_id) REFERENCES products(product_id),
  FOREIGN KEY (seller_id)  REFERENCES sellers(seller_id)
);

CREATE TABLE order_payments (            -- composite PK: an order can be paid in several parts
  order_id              CHAR(32) NOT NULL,
  payment_sequential    INT NOT NULL,
  payment_type          VARCHAR(20),
  payment_installments  INT,
  payment_value         DECIMAL(10,2),
  PRIMARY KEY (order_id, payment_sequential),
  FOREIGN KEY (order_id) REFERENCES orders(order_id)
);

CREATE TABLE order_reviews (             -- review_id alone is NOT unique, so PK is (review_id, order_id)
  review_id                CHAR(32) NOT NULL,
  order_id                 CHAR(32) NOT NULL,
  review_score             INT,
  review_comment_title     VARCHAR(255),
  review_comment_message   TEXT,
  review_creation_date     DATETIME,
  review_answer_timestamp  DATETIME,
  PRIMARY KEY (review_id, order_id),
  FOREIGN KEY (order_id) REFERENCES orders(order_id)
);

-- LOAD DATA -------------------------------------------------------------------
-- 1) SHOW VARIABLES LIKE 'secure_file_priv';  -> put the CSVs in that folder (or enable local_infile)
-- 2) Edit the folder path below (forward slashes, even on Windows). Load in this order (parents first).
-- Empty cells become NULL through NULLIF.
/*
SET GLOBAL local_infile = 1;
LOAD DATA LOCAL INFILE 'C:/olist_mini/product_category_name_translation.csv' INTO TABLE product_category_name_translation
  FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 LINES;
LOAD DATA LOCAL INFILE 'C:/olist_mini/customers.csv' INTO TABLE customers
  FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 LINES;
LOAD DATA LOCAL INFILE 'C:/olist_mini/sellers.csv' INTO TABLE sellers
  FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 LINES;
LOAD DATA LOCAL INFILE 'C:/olist_mini/products.csv' INTO TABLE products
  FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 LINES
  (product_id,@cat,@a,@b,@c,@d,@e,@f,@g)
  SET product_category_name=NULLIF(@cat,''), product_name_lenght=NULLIF(@a,''), product_description_lenght=NULLIF(@b,''),
      product_photos_qty=NULLIF(@c,''), product_weight_g=NULLIF(@d,''), product_length_cm=NULLIF(@e,''),
      product_height_cm=NULLIF(@f,''), product_width_cm=NULLIF(@g,'');
LOAD DATA LOCAL INFILE 'C:/olist_mini/orders.csv' INTO TABLE orders
  FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 LINES
  (order_id,customer_id,order_status,order_purchase_timestamp,@a,@b,@c,order_estimated_delivery_date)
  SET order_approved_at=NULLIF(@a,''), order_delivered_carrier_date=NULLIF(@b,''), order_delivered_customer_date=NULLIF(@c,'');
LOAD DATA LOCAL INFILE 'C:/olist_mini/order_items.csv' INTO TABLE order_items
  FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 LINES;
LOAD DATA LOCAL INFILE 'C:/olist_mini/order_payments.csv' INTO TABLE order_payments
  FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 LINES;
LOAD DATA LOCAL INFILE 'C:/olist_mini/order_reviews.csv' INTO TABLE order_reviews
  FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 LINES
  (review_id,order_id,review_score,@t,@m,review_creation_date,review_answer_timestamp)
  SET review_comment_title=NULLIF(@t,''), review_comment_message=NULLIF(@m,'');
LOAD DATA LOCAL INFILE 'C:/olist_mini/geolocation.csv' INTO TABLE geolocation
  FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 LINES;
*/
