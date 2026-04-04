-- ============================================================
-- make_tables.sql
-- Creates MySQL tables for suppliers and orders.
-- The 'parts' table must already exist (created by j2sql_parts.sh).
-- ============================================================

DROP TABLE IF EXISTS OrderPart;
DROP TABLE IF EXISTS Orders;
DROP TABLE IF EXISTS SupplierPhone;
DROP TABLE IF EXISTS supplier;

CREATE TABLE supplier (
    _id   INT PRIMARY KEY,
    name  VARCHAR(100) NOT NULL,
    email VARCHAR(100)
) ENGINE=InnoDB;

CREATE TABLE SupplierPhone (
    phone_number VARCHAR(30) PRIMARY KEY,
    supp_id      INT NOT NULL,
    FOREIGN KEY (supp_id) REFERENCES supplier(_id)
) ENGINE=InnoDB;

CREATE TABLE Orders (
    order_id   INT PRIMARY KEY,
    when_date  DATE,
    supp_id    INT NOT NULL,
    FOREIGN KEY (supp_id) REFERENCES supplier(_id)
) ENGINE=InnoDB;

CREATE TABLE OrderPart (
    id       INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    part_id  INT NOT NULL,
    qty      INT NOT NULL,
    FOREIGN KEY (order_id) REFERENCES Orders(order_id),
    FOREIGN KEY (part_id)  REFERENCES parts(_id)
) ENGINE=InnoDB;