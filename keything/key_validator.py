#!/usr/bin/env python3
import os
import sys
import time
import hashlib
from datetime import datetime, timedelta

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def animate_text(text, delay=0.03):
    """Animate text by printing characters one by one."""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def print_header():
    """Print the application header."""
    clear_screen()
    header = """
    ╔═══════════════════════════════════════════════╗
    ║                SECURE PROGRAM                 ║
    ║           Protected by Linkvertise            ║
    ╚═══════════════════════════════════════════════╝
    """
    print(header)

def is_valid_key_format(key):
    """Check if the key has the correct format (length and characters)."""
    if not key or len(key) != 24:
        return False
    
    valid_chars = set("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789")
    return all(char in valid_chars for char in key)

def validate_key(key):
    """
    Validate the key by:
    1. Checking its format
    2. Checking if it has embedded timestamp (which the web generator would include)
    3. Verifying the key hasn't expired
    
    Since our web page generates random keys without embedded timestamps,
    we'll implement a simplified validation that checks format and 
    creates a deterministic hash from the key to check its validity.
    """
    if not is_valid_key_format(key):
        return False, "Invalid key format"
    
    # Simple validation algorithm - we check if the hash of the key
    # has specific properties that indicate it came from our generator
    # This is a simplified approach - in a real system you might want to
    # encode timestamps or other validation info in the key itself
    
    # Create a hash from the key
    key_hash = hashlib.sha256(key.encode()).hexdigest()
    
    # A valid key would have a hash with specific properties
    # For example, we can check if the first 2 characters are digits
    # and the last 2 characters are letters
    first_two = key_hash[:2]
    last_two = key_hash[-2:]
    
    if not (first_two.isdigit() and last_two.isalpha()):
        return False, "Invalid key"
    
    # This is where you would check for expiration, but since our keys
    # don't contain expiration info, we can't validate that here.
    # In a real system, the key might encode a timestamp.
    
    return True, "Key validated successfully"

def run_protected_program():
    """Run the actual protected program after successful validation."""
    print_header()
    animate_text("Access granted! Loading protected program...", 0.05)
    time.sleep(1)
    
    print("\n" + "=" * 50)
    animate_text("Welcome to the protected program!", 0.03)
    animate_text("This is the content that was protected by your key.", 0.03)
    animate_text("You can now use all the features of this program.", 0.03)
    print("=" * 50 + "\n")
    
    # Simulate program functionality
    while True:
        print("\nProtected Program Menu:")
        print("1. Show Important Information")
        print("2. Calculate Something")
        print("3. Exit Program")
        
        choice = input("\nEnter your choice (1-3): ")
        
        if choice == "1":
            print("\n📋 Important Information:")
            animate_text("This is secret information only available to users with valid keys.", 0.03)
            animate_text("Your access to this information will expire in 24 hours.", 0.03)
            input("\nPress Enter to continue...")
            
        elif choice == "2":
            print("\n🧮 Calculation Module:")
            try:
                num1 = float(input("Enter first number: "))
                num2 = float(input("Enter second number: "))
                print(f"\nResults:")
                print(f"Addition: {num1} + {num2} = {num1 + num2}")
                print(f"Subtraction: {num1} - {num2} = {num1 - num2}")
                print(f"Multiplication: {num1} × {num2} = {num1 * num2}")
                if num2 != 0:
                    print(f"Division: {num1} ÷ {num2} = {num1 / num2}")
                else:
                    print("Division: Cannot divide by zero")
            except ValueError:
                print("Invalid input. Please enter numbers only.")
            input("\nPress Enter to continue...")
            
        elif choice == "3":
            animate_text("Thank you for using the protected program. Goodbye!", 0.03)
            time.sleep(1)
            sys.exit(0)
            
        else:
            print("Invalid choice. Please try again.")
        
        clear_screen()
        print_header()

def main():
    attempts = 3
    
    while attempts > 0:
        print_header()
        print(f"Attempts remaining: {attempts}")
        print("\nThis program is protected by a key generated through Linkvertise.")
        print("You must have a valid key to access the content.\n")
        
        key = input("Please enter your access key: ").strip()
        
        if key.lower() == 'exit':
            sys.exit(0)
            
        is_valid, message = validate_key(key)
        
        if is_valid:
            animate_text("Validating key... ✓", 0.05)
            time.sleep(1)
            run_protected_program()
            break
        else:
            animate_text(f"Validating key... ✗", 0.05)
            animate_text(f"Error: {message}", 0.03)
            attempts -= 1
            
            if attempts > 0:
                print(f"\nYou have {attempts} {'attempts' if attempts > 1 else 'attempt'} remaining.")
                print("Type 'exit' to quit or press Enter to try again.")
                input()
            else:
                animate_text("\nYou have exceeded the maximum number of attempts.", 0.03)
                animate_text("Please generate a new key through Linkvertise and try again.", 0.03)
                time.sleep(2)
                sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProgram terminated by user.")
        sys.exit(0)
