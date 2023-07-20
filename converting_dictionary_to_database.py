import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="12bpform$4",
    port=5432
)
cursor = conn.cursor()

cursor.execute(
    
    '''CREATE TABLE IF NOT EXISTS dictionary1 (
    product_id serial PRIMARY KEY, 
    product_name VARCHAR(255) NOT NULL UNIQUE,
    product_count integer NOT NULL,
    product_price float NOT NULL
    )
    '''
)
id=int(input("Enter the id number of the product: "))
name=input("Enter the name of the product: ")
count=int(input("Enter the number of products: "))
price=float(input("Enter the price of the product: "))

product_data={
    "product_id": id,
    "product_name" : name,
    "product_count" : count,
    "product_price" : price
}



cursor.execute(
    "INSERT INTO dictionary1 (product_id, product_name,product_count,product_price) VALUES (%s, %s,%s,%s)", (product_data['product_id'],product_data['product_name'],product_data['product_count'],product_data['product_price'])
)
conn.commit()

