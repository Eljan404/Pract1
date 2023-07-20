<?php

$host = 'localhost';
$dbname = 'database';
$username = 'root';
$password = 'G3ne4at3#d_';

try {
    $conn = new PDO("mysql:host=$host;dbname=$dbname", $username, $password);
    $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    
    $conn->exec('
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255) NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL
        )
    ');

    function register($username, $password, $conn) {
        $hashed_password = hash_password($password);
        try {
            $statement = $conn->prepare("INSERT INTO users (username, password) VALUES (:username, :password)");
            $statement->bindParam(':username', $username);
            $statement->bindParam(':password', $hashed_password);
            $statement->execute();
            echo "Registration successful!\n";
            return true;
        } catch (PDOException $e) {
            if ($e->getCode() == 23000) {
                echo "Registration failed because username already exists. Try again, please:\n";
            } else {
                echo "Registration failed: " . $e->getMessage() . "\n";
            }
            return false;
        }
    }

    function login($username, $password, $conn) {
        $statement = $conn->prepare("SELECT * FROM users WHERE username=:username");
        $statement->bindParam(':username', $username);
        $statement->execute();
        $user = $statement->fetch();
        
        while ($user === false || !verify_password($password, $user['password'])) {
            echo "Login failed. Invalid username or password. Please, try again:\n";
            $username = readline("Enter your username: ");
            $password = readline("Enter your password: ");
            
            $statement = $conn->prepare("SELECT * FROM users WHERE username=:username");
            $statement->bindParam(':username', $username);
            $statement->execute();
            $user = $statement->fetch();
        }
        
        echo "Login successful!\n";
    }

    function hash_password($password) {
        return password_hash($password, PASSWORD_BCRYPT);
    }

    function verify_password($password, $hashed_password) {
        return password_verify($password, $hashed_password);
    }

    $registration_success = false;
    while (!$registration_success) {
        $username = readline("Enter your username: ");
        $password = readline("Enter your password: ");
        $registration_success = register($username, $password, $conn);
    }

    $login_username = readline("Enter your username: ");
    $login_password = readline("Enter your password: ");
    login($login_username, $login_password, $conn);

    $conn = null;
} catch (PDOException $e) {
    echo "Connection failed: " . $e->getMessage() . "\n";
}
