import os
from amazonorders.session import AmazonSession
from amazonorders.orders import AmazonOrders
from my_functions import export_all_fetched_data_to_csv, export_select_fields_to_csv, get_orders_and_update_csv, ask_confirmation

# Load credentials from environment variables
amazon_username_user1 = os.environ.get("AMAZON_USERNAME_USER1")
amazon_password_user1 = os.environ.get("AMAZON_PASSWORD_USER1")
amazon_username_user2 = os.environ.get("AMAZON_USERNAME_USER2")
amazon_password_user2 = os.environ.get("AMAZON_PASSWORD_USER2")

# Keep them low to test and then modify
fetch_orders_for_year=2025
fetch_max_count_of_order=5  # Set to None to fetch all

if not amazon_username_user1 or not amazon_password_user1 or not amazon_username_user2 or not amazon_password_user2:
    raise ValueError("Missing AMAZON_USERNAME or AMAZON_PASSWORD environment variable.")

# Ask user do you want to run for user?
message=f"Fetch data for {amazon_username_user1}? (y/n): "
if ask_confirmation(message):

    # Initialize session and login
    amazon_session_User1 = AmazonSession(amazon_username_user1, amazon_password_user1) #, debug=True)
    amazon_session_User1.login()

    # Fetch order history
    amazon_orders_User1 = AmazonOrders(amazon_session_User1) #, debug=True)

    #export_select_fields_to_csv(orders)
    #export_all_fetched_data_to_csv(orders)
    # Update the CSV with orders from a specific year
    get_orders_and_update_csv(amazon_orders=amazon_orders_User1,
            year=fetch_orders_for_year,
            max_orders=fetch_max_count_of_order,  # Set to None to fetch all orders
            amazon_username=amazon_username_user1,
            csv_filename="AmazonOrders_db.csv"
            )    
    amazon_session_User1.logout()  # Explicitly log out

# Ask user do you want to run for user?
message=f"Fetch data for {amazon_username_user2}? (y/n): "
if ask_confirmation(message):

    # Initialize session and login
    amazon_session_User2 = AmazonSession(amazon_username_user2, amazon_password_user2)
    amazon_session_User2.login()

    # Fetch order history
    amazon_orders_User2 = AmazonOrders(amazon_session_User2)

    #export_select_fields_to_csv(orders)
    #export_all_fetched_data_to_csv(orders)
    # Update the CSV with orders from a specific year
    get_orders_and_update_csv(amazon_orders=amazon_orders_User2,
            year=fetch_orders_for_year,
            max_orders=fetch_max_count_of_order,  # Set to None to fetch all orders
            amazon_username=amazon_username_user2,
            csv_filename="AmazonOrders_User2_db.csv"
            )    
    amazon_session_User2.logout()  # Explicitly log out
