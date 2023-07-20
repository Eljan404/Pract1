import psycopg2
from tabulate import tabulate
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

def show_choices():
    print("Press 1 to See the table")
    print("Press 2 to Add")
    print("Press 3 to Update")
    print("Press 4 to Delete")

def read_function():
    cursor.execute("SELECT * FROM dictionary1")
    rows = cursor.fetchall()
    if rows:
        headers = [desc[0] for desc in cursor.description]
        print(tabulate(rows, headers=headers, tablefmt="fancy_grid"))
        print("\n")
    else:
        print("The table is empty.")


def add_function():
    name = input("Enter the name of the product: ")
    cursor.execute("SELECT product_name FROM dictionary1 WHERE product_name=%s", (name,))
    names = cursor.fetchall()
    if names:
        print("This product has already been added.")
        return
    
    id = int(input("Enter the id number of the product: "))
    count = int(input("Enter the number of products: "))
    price = float(input("Enter the price of the product: "))
    
    product_data = {
        "product_id": id,
        "product_name": name,
        "product_count": count,
        "product_price": price
    }
    
    cursor.execute("INSERT INTO dictionary1 (product_id, product_name, product_count, product_price) VALUES (%s, %s, %s, %s)", 
                   (product_data['product_id'], product_data['product_name'], product_data['product_count'], product_data['product_price']))
    conn.commit()
    print("The product data has been added successfully!")
    read_function()

def update_function(name):
    cursor.execute("SELECT product_name FROM dictionary1 WHERE product_name=%s", (name,))
    names = cursor.fetchall()
    for row in names:
        if row[0] == name:
            new_id = int(input("Enter the id number of the product: "))
            new_name = input("Enter the name of the product: ")
            new_count = int(input("Enter the number of products: "))
            new_price = float(input("Enter the new price of the product: "))
            cursor.execute("UPDATE dictionary1 SET product_id=%s, product_name=%s, product_count=%s, product_price=%s WHERE product_name=%s", 
                           (new_id, new_name, new_count, new_price, name))
            conn.commit()
            print("The product has been updated successfully!")
            read_function()
            break
    else:
        print("There is no product with that name.")

def delete_function(name):
    cursor.execute("SELECT product_name FROM dictionary1 WHERE product_name=%s", (name,))
    names = cursor.fetchall()
    for row in names:
        if row[0] == name:
            cursor.execute("DELETE FROM dictionary1 WHERE product_name=%s", (name,))
            conn.commit()
            print("The product has been deleted successfully!")
            read_function()
            break
    else:
        print("There is no product with that name.")

def main():
    while True:
        show_choices()
        choice = input("Enter your choice: ")

        if choice == '1':
            read_function()

        elif choice == '2':
            add_function()

        elif choice == '3':
            read_function()
            name = input("Enter the name of the product to update: ")
            update_function(name)

        elif choice == '4':
            read_function()
            name = input("Enter the name of the product to delete: ")
            delete_function(name)

        else:
            print("Invalid choice")

        answer = input("Do you want to continue to read/add/update/delete the process? (Yes or No) ")

        if answer.lower() == 'yes':
            continue

        if answer.lower() == 'no':
            break

if __name__ == "__main__":
    main()
