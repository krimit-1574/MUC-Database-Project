-- ============================================================
-- make_tables.sql
-- Creates MySQL tables for suppliers and orders.
-- The 'parts' table must already exist (created by j2sql_parts.sh).
-- ============================================================

-- Suppliers table
CREATE TABLE IF NOT EXISTS supplier (
    _id   INT PRIMARY KEY,
    name  VARCHAR(100) NOT NULL,
    email VARCHAR(100)
) ENGINE=InnoDB;

-- Supplier phone numbers (multivalued attribute)
-- "Suppliers have no telephone numbers in common" → phone_number is globally unique (PK)
CREATE TABLE IF NOT EXISTS SupplierPhone (
    phone_number VARCHAR(30) PRIMARY KEY,
    supp_id      INT NOT NULL,
    FOREIGN KEY (supp_id) REFERENCES supplier(_id)
) ENGINE=InnoDB;

-- Orders table
CREATE TABLE IF NOT EXISTS Orders (
    order_id   INT AUTO_INCREMENT PRIMARY KEY,
    when_date  DATE,
    supp_id    INT NOT NULL,
    FOREIGN KEY (supp_id) REFERENCES supplier(_id)
) ENGINE=InnoDB;

-- Order-Part relationship (M:N with quantity)
-- Uses auto-increment PK because the JSON data contains orders
-- with duplicate part_ids (same part listed multiple times).
CREATE TABLE IF NOT EXISTS OrderPart (
    id       INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    part_id  INT NOT NULL,
    qty      INT NOT NULL,
    FOREIGN KEY (order_id) REFERENCES Orders(order_id),
    FOREIGN KEY (part_id)  REFERENCES parts(_id)
) ENGINE=InnoDB;
