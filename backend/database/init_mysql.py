import mysql.connector

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",        # your MySQL username
    password="P00rn1m@",
    database="email_ai"
)

cursor = conn.cursor()

# Insert sample customers
cursor.execute("""
INSERT INTO customers (name, email, age, location, interests, last_purchase, purchase_category, loyalty_score)
VALUES
('John Doe', 'john@gmail.com', 28, 'India', 'fitness,travel', 'Running Shoes', 'Sports', 8),
('Rohith B prasad', 'rohith23ai@gmail.com', 25, 'Hyderabad', 'tech, gadgets', 'smartwatch', 'electronics', 60),               
('Anita Sharma', 'anita@example.com', 32, 'Delhi', 'fashion, shopping', 'handbag', 'fashion', 75), 
('Vikram Rao', 'vikram@example.com', 40, 'Bangalore', 'tech, gaming', 'VR headset', 'electronics', 90),          
('Anita S', 'anita@gmail.com', 34, 'India', 'learning,career', 'Online Course', 'Education', 9)
""")


conn.commit()
print("Sample data inserted successfully")

# Test fetch
cursor.execute("SELECT * FROM customers")
for row in cursor.fetchall():
    print(row)

conn.close()
