CREATE TABLE IF NOT EXISTS parts
(
  _id INT NOT NULL,
  price DOUBLE(10,2),
  description VARCHAR(50),
  PRIMARY KEY (_id)
) ENGINE = InnoDB;
