<?php

$host='localhost';
$dbname='database';
$username='root';
$password='G3ne4at3#d_';

try {
    $conn=new PDO("mysql::host=$host;dbname=$dbname",$username,$password);
    $conn->setAttribute(PDO::ATTR_ERRMODE,PDO::ERRMODE_EXCEPTION);
    
    $createTableQuery="
        CREATE TABLE IF NOT EXISTS users(
            id INT(100) AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255) NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL
    )";
    
    $conn->exec($createTableQuery);

    function register($username,$password)
    {
        global $conn;
        $hashed_password=hash_password($password);

        try {
            $insertQuery="INSERT INTO users (username,password) VALUES (?,?)";
            $statement= $conn->prepare($insertQuery);
            $statement->execute([$username, $hashed_password]);
            echo "Registration successful!\n";
        }

        catch(PDOException $e) {
            echo "Registration failed: " . $e->getMessage();
        }
    }

    function login($username,$password)
    {
        global $conn;
        $selectQuery="SELECT * FROM users WHERE username = ?";
        $statement=$conn->prepare($selectQuery);
        $statement->execute([$username]);
        $user = $statement->fetch();
        if (verify_password($password,$user['password']))
        {
            echo "Login successful!";
        } 
        else 
        {
            echo "Login failed. Invalid username or password.";
        }
    }

    function hash_password($password)
    {
        $salt=password_hash($password,PASSWORD_DEFAULT);
        return $salt;
    }
    
    function verify_password($password,$hashed_password)
    {
        return password_verify($password,$hashed_password);
    }

    register("cemil56", "rinq");
    login("cemil56", "rinq");

} catch (PDOException $e) {
    echo "Connection failed: " . $e->getMessage();
}
?>

