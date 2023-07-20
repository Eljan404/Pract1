<?php

$host = 'localhost';
$dbname = 'database';
$username = 'root';
$password = 'G3ne4at3#d_';

try {
    $conn = new PDO("mysql:host=$host;dbname=$dbname", $username, $password);
    $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION); #PDO::ERRMODE_SILENT (if we wouldn't write this line, it would output silent error)

    $createTableQuery = "
    CREATE TABLE IF NOT EXISTS products(
        id INT(250) AUTO_INCREMENT PRIMARY KEY,
        product_name VARCHAR(250),
        product_count INT,
        product_price FLOAT
    )";
    
    $conn->exec($createTableQuery);

    function show_choices()
    {
        echo "Press 1 to Add\n";
        echo "Press 2 to Update\n";
        echo "Press 3 to Delete\n";
    }

    function add_function()
    {
        global $conn;
        $product_name = readline("Enter the name of the product: ");
        $select_query = "SELECT product_name FROM products WHERE product_name=?";
        $statement = $conn->prepare($select_query);
        $statement->execute([$product_name]);
        $names = $statement->fetchAll(PDO::FETCH_NUM);
        foreach ($names as $row)
        {
            if ($row[0] == $product_name)
            {
                echo "This product has already been added\n";
                return;
            }
        }
        $product_count = readline("Enter the number of the product: ");
        $product_price = readline("Enter the price of the product: ");
        $insert_query = "INSERT INTO products (product_name, product_count, product_price) VALUES (?,?,?)";
        $statement = $conn->prepare($insert_query);
        $statement->execute([$product_name, $product_count, $product_price]);
        echo "The product has been added successfully!\n";
    }

    function update_function($product_name)
    {
        global $conn;
        $select_query = "SELECT product_name FROM products WHERE product_name=?";
        $statement = $conn->prepare($select_query);
        $statement->execute([$product_name]);
        $names = $statement->fetchAll(PDO::FETCH_NUM);
        foreach ($names as $row)
        {
            if ($row[0] == $product_name)
            {
                $new_name = readline("Enter the new name of the product: ");
                $new_count = readline("Enter the updated number of products: ");
                $new_price = readline("Enter the new price of the product: ");
                $update_query = "UPDATE products SET product_name=?, product_count=?, product_price=? WHERE product_name=?";
                $statement = $conn->prepare($update_query);
                $statement->execute([$new_name, $new_count, $new_price, $product_name]);
                echo "The product has been updated successfully!\n";
                return;
            }
        }
        echo "There is no product with that name.\n";
    }

    function delete_function($product_name)
    {
        global $conn;
        $select_query = "SELECT product_name FROM products WHERE product_name=?";
        $statement = $conn->prepare($select_query);
        $statement->execute([$product_name]);
        $names = $statement->fetchAll(PDO::FETCH_NUM);
        foreach ($names as $row)
        {
            if ($row[0] == $product_name)
            {
                $delete_query = "DELETE FROM products WHERE product_name=?";
                $statement = $conn->prepare($delete_query);
                $statement->execute([$product_name]);
                echo "The product has been deleted successfully!\n";
                return;
            }
        }
        echo "There is no product with that name.\n";
    }

    while (true)
    {
        show_choices();
        $choice = readline("Enter your choice: ");
        if ($choice == 1)
        {
            add_function();
        }
        else if ($choice == 2)
        {
            $product_name = readline("Enter the name of the product to update: ");
            update_function($product_name);
        }
        else if ($choice == 3)
        {
            $product_name = readline("Enter the name of the product to delete: ");
            delete_function($product_name);
        }
        else
        {
            echo "Invalid choice, try again\n";
            continue;
        }

        $answer = readline("Do you want to continue to add/update/delete the process? (Yes or No) ");
        if (strtolower($answer) == 'yes')
        {
            continue;
        }     
        else if (strtolower($answer) == 'no')
        {
            break;
        }
        else
        {
            echo "Invalid choice, try again\n";
        }
    }
}
catch(PDOException $e)
{
    echo "Connection failed: " . $e->getMessage();
}
?>
