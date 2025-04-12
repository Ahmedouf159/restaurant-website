-- Drop tables if they already exist (optional during development)
DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS cart;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS menu;

-- Create the users table
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    location TEXT
);

-- Create the menu table
CREATE TABLE menu (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price REAL NOT NULL,
    image_url TEXT
);

-- Create the orders table
CREATE TABLE orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    total_price REAL,
    location TEXT,
    order_time TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Create the order_items table
CREATE TABLE order_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER,
    item_name TEXT,
    price REAL,
    quantity INTEGER,
    FOREIGN KEY (order_id) REFERENCES orders(id)
);

-- Create the cart table
CREATE TABLE cart (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    item_name TEXT,
    price REAL,
    quantity INTEGER,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Insert menu items with valid local image URLs
INSERT INTO menu (name, price, image_url) VALUES ('Pizza Margherita', 12.99, '/static/images/pizza.jpg');
INSERT INTO menu (name, price, image_url) VALUES ('Spaghetti Carbonara', 10.99, '/static/images/spaghetti.jpg');
INSERT INTO menu (name, price, image_url) VALUES ('Caesar Salad', 8.99, '/static/images/caesar_salad.jpg');
INSERT INTO menu (name, price, image_url) VALUES ('Grilled Chicken', 14.99, '/static/images/grilled_chicken.jpg');
INSERT INTO menu (name, price, image_url) VALUES ('Beef Burger', 11.99, '/static/images/beef_burger.jpg');
INSERT INTO menu (name, price, image_url) VALUES ('Sushi Platter', 19.99, '/static/images/sushi_platter.jpg');
INSERT INTO menu (name, price, image_url) VALUES ('Vegetable Stir Fry', 9.99, '/static/images/vegetable_stir_fry.jpg');
INSERT INTO menu (name, price, image_url) VALUES ('Tacos', 8.49, '/static/images/tacos.jpg');
INSERT INTO menu (name, price, image_url) VALUES ('Fish and Chips', 13.49, '/static/images/fish_and_chips.jpg');
INSERT INTO menu (name, price, image_url) VALUES ('Chocolate Cake', 6.99, '/static/images/chocolate_cake.jpg');
INSERT INTO menu (name, price, image_url) VALUES ('Ice Cream Sundae', 5.99, '/static/images/ice_cream_sundae.jpg');
INSERT INTO menu (name, price, image_url) VALUES ('Pasta Alfredo', 10.49, '/static/images/pasta_alfredo.jpg');
INSERT INTO menu (name, price, image_url) VALUES ('BBQ Ribs', 15.49, '/static/images/bbq_ribs.jpg');
INSERT INTO menu (name, price, image_url) VALUES ('Chicken Wings', 9.49, '/static/images/chicken_wings.jpg');
INSERT INTO menu (name, price, image_url) VALUES ('Garden Salad', 7.99, '/static/images/garden_salad.jpg');
INSERT INTO menu (name, price, image_url) VALUES ('French Fries', 4.99, '/static/images/french_fries.jpg');
INSERT INTO menu (name, price, image_url) VALUES ('Cheesecake', 6.49, '/static/images/cheesecake.jpg');
INSERT INTO menu (name, price, image_url) VALUES ('Pancakes', 5.99, '/static/images/pancakes.jpg');
INSERT INTO menu (name, price, image_url) VALUES ('Lemonade', 2.99, '/static/images/lemonade.jpg');



