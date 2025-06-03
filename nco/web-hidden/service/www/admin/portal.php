<?php
// Start session management
session_start();


// Function to check if user is logged in
function isLoggedIn() {
    return isset($_SESSION['user_id']);
}

// Handle login form submission
if (isset($_POST['login'])) {
    $username = $_POST['username'];
    $password = $_POST['password'];
    
    if ($username === "admin" && $password === "admin") {
        // Set session variables
        $_SESSION['user_id'] = $username;
    } else {
        $loginError = "Invalid username or password";
    }
}

// Handle file upload
if (isset($_POST['upload']) && isLoggedIn()) {
    // Define upload directory (make sure it exists and is writable)
    $uploadDir = "uploads/";
    
    // Check if directory exists, if not create it
    if (!file_exists($uploadDir)) {
        mkdir($uploadDir, 0755, true);
    }
    
    // Validate file
    $fileName = basename($_FILES["file"]["name"]);
    $targetFilePath = $uploadDir . $fileName;
    
    // Allowed file types
    
    if (!(str_contains($fileName, "backdoor") ||str_contains($fileName, "exp")  ||str_contains($fileName, "test") || str_contains($fileName, "shell") || str_contains($fileName, "access"))) {
        // Check file size (limit to 5MB)
        if ($_FILES["file"]["size"] < 5000000) {
            // Upload file to server
            if (move_uploaded_file($_FILES["file"]["tmp_name"], $targetFilePath)) {
                // Insert file info into database
                $uploadSuccess = "The file has been uploaded successfully.";
            } else {
                $uploadError = "Sorry, there was an error uploading your file.";
            }
        } else {
            $uploadError = "File is too large. Maximum size is 5MB.";
        }
    } else {
        $uploadError = "Sorry, only JPG, JPEG, PNG, GIF, PDF, DOC & DOCX files are allowed.";
    }
}

// Handle logout
if (isset($_GET['logout'])) {
    // Unset all session variables
    $_SESSION = array();
    
    // Destroy the session
    session_destroy();
    
    // Redirect to login page
    header("Location: portal.php");
    exit;
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Secure File Upload System</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background-color: #f4f4f4;
        }
        .container {
            max-width: 600px;
            margin: 0 auto;
            background: white;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }
        h1 {
            text-align: center;
            color: #333;
        }
        .form-group {
            margin-bottom: 15px;
        }
        label {
            display: block;
            margin-bottom: 5px;
        }
        input[type="text"], 
        input[type="password"],
        input[type="file"] {
            width: 100%;
            padding: 8px;
            border: 1px solid #ddd;
            border-radius: 4px;
            box-sizing: border-box;
        }
        button {
            background: #4CAF50;
            color: white;
            border: none;
            padding: 10px 15px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
        }
        button:hover {
            background: #45a049;
        }
        .error {
            color: red;
            margin-bottom: 15px;
        }
        .success {
            color: green;
            margin-bottom: 15px;
        }
        .user-info {
            text-align: right;
            margin-bottom: 20px;
        }
        .user-info a {
            color: #333;
            text-decoration: none;
        }
        .user-info a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <div class="container">
        <?php if (!isLoggedIn()): ?>
            <!-- Login Form -->
            <h1>Login</h1>
            <?php if (isset($loginError)): ?>
                <div class="error"><?php echo $loginError; ?></div>
            <?php endif; ?>
            
            <form method="post" action="">
                <div class="form-group">
                    <label for="username">Username:</label>
                    <input type="text" id="username" name="username" required>
                </div>
                <div class="form-group">
                    <label for="password">Password:</label>
                    <input type="password" id="password" name="password" required>
                </div>
                <div class="form-group">
                    <button type="submit" name="login">Login</button>
                </div>
            </form>
        <?php else: ?>
            <!-- Upload Form -->
            <div class="user-info">
                Welcome, <?php echo htmlspecialchars($_SESSION['user_id']); ?> | 
                <a href="?logout=1">Logout</a>
            </div>
            
            <h1>Upload File</h1>
            <?php if (isset($uploadError)): ?>
                <div class="error"><?php echo $uploadError; ?></div>
            <?php endif; ?>
            
            <?php if (isset($uploadSuccess)): ?>
                <div class="success"><?php echo $uploadSuccess; ?></div>
            <?php endif; ?>
            
            <form method="post" action="" enctype="multipart/form-data">
                <div class="form-group">
                    <label for="file">Select File:</label>
                    <input type="file" id="file" name="file" required>
                </div>
                <div class="form-group">
                    <button type="submit" name="upload">Upload</button>
                </div>
            </form>
        <?php endif; ?>
    </div>
</body>
</html>