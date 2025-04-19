import os
from datetime import datetime
import csv

def ask_confirmation(message="Do you want to continue? (y/n): "):
    while True:
        user_input = input(message).strip().lower()
        if user_input in ['y', 'yes']:
            print("Continuing...")
            return True
        elif user_input in ['n', 'no']:
            print("Exiting program.")
            return False
        else:
            print("Invalid input. Please enter 'y' or 'n'.")


def export_select_fields_to_csv(orders):
    """
    Export Amazon orders to a CSV file with specific fields.
    """
    # Generate timestamped filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"AmazonOrders_{timestamp}.csv"

    # Define the field names in the specified order
    fieldnames = [
        'index',
        'order_details_link',
        'order_placed_date',
        'item_title',
        'item_price',
        'payment_method',
        'payment_method_last_4',
        'subtotal',
        'postage_and_packing',
        'total_before_vat',
        'vat',
        'total',
        'promotion_applied',
        'gift_card_amount',
        'grand_total',
        'refund_total'
    ]
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for index, order in enumerate(orders, 1):
            # Check if the order has multiple items or a single item
            items = []
            if hasattr(order, 'items'):
                items = order.items
            elif hasattr(order, 'item'):
                items = [order.item]
            else:
                items = []
            
            # If there are no items, create a single row with empty item fields
            if items:
                # Create a row for each item in the order
                for i, item in enumerate(items):
                    row = {
                        'index': getattr(order, 'index', ''),
                        'order_details_link': getattr(order, 'order_details_link', ''),
                        'order_placed_date': getattr(order, 'order_placed_date', ''),
                        'item_title': getattr(item, 'title', ''),
                        'item_price': getattr(item, 'price', ''),
                        'payment_method': getattr(order, 'payment_method', ''),
                        'payment_method_last_4': getattr(order, 'payment_method_last_4', ''),
                        'subtotal': getattr(order, 'subtotal', ''),
                        'postage_and_packing': getattr(order, 'postage_and_packing', ''),
                        'total_before_vat': getattr(order, 'total_before_vat', ''),
                        'vat': getattr(order, 'vat', ''),
                        'total': getattr(order, 'total', ''),
                        'promotion_applied': getattr(order, 'promotion_applied', ''),
                        'gift_card_amount': getattr(order, 'gift_card_amount', ''),
                        'grand_total': getattr(order, 'grand_total', ''),
                        'refund_total': getattr(order, 'refund_total', '')
                    }
                    writer.writerow(row)
        
    print(f"Orders exported to {filename}")
    return filename



def export_all_fetched_data_to_csv(orders, csv_add_items_in_rows = True):
    # Generate timestamped filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"All_data_{timestamp}.csv"

    # Open CSV file for writing
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        if csv_add_items_in_rows:
            if orders:
                # Extract all attributes from the first order
                first_order = orders[0]
                
                # Get all attributes that don't begin with underscore (public attributes)
                base_fields = [attr for attr in dir(first_order) if not attr.startswith('_') and not callable(getattr(first_order, attr))]
                
                # Create CSV writer and write header with item fields
                writer = csv.writer(file)
                writer.writerow(base_fields + ["item_title", "item_price"])
                
                # Write order details with item information
                for order in orders:
                    # Get base order information
                    base_row = []
                    for field in base_fields:
                        try:
                            value = getattr(order, field)
                            if isinstance(value, (list, dict)):
                                value = str(value)
                            base_row.append(value)
                        except Exception:
                            base_row.append("")
                    
                    # Check if the order has items
                    if hasattr(order, "items") and order.items:
                        # Add a row for each item in the order
                        for item in order.items:
                            item_row = base_row.copy()  # Copy the base order information
                            
                            # Add item title
                            if hasattr(item, "title"):
                                item_row.append(item.title)
                            else:
                                item_row.append("")
                            
                            # Add item price
                            if hasattr(item, "price"):
                                item_row.append(item.price)
                            else:
                                item_row.append("")
                            
                            writer.writerow(item_row)
                    else:
                        # If no items, just write the order info with empty item fields
                        writer.writerow(base_row + ["", ""])
                
                print(f"Orders and items saved to {filename}")

        else:
            if orders:
                # Extract all attributes from the first order
                first_order = orders[0]
                base_fields = [attr for attr in dir(first_order) if not attr.startswith('_') and not callable(getattr(first_order, attr)) and attr != "items"]
                
                # Find max number of items in any order to know how many columns we need
                max_items = max(len(order.items) if hasattr(order, "items") and order.items else 0 for order in orders)
                
                # Create header
                header = base_fields.copy()
                for i in range(1, max_items + 1):
                    header.append(f"item_{i}_title")
                    header.append(f"item_{i}_price")
                
                writer = csv.writer(file)
                writer.writerow(header)
                
                # Write each order row
                for order in orders:
                    base_row = []
                    for field in base_fields:
                        try:
                            value = getattr(order, field)
                            if isinstance(value, (list, dict)):
                                value = str(value)
                            base_row.append(value)
                        except Exception:
                            base_row.append("")
                    
                    # Add item details
                    item_fields = []
                    if hasattr(order, "items") and order.items:
                        for item in order.items:
                            title = getattr(item, "title", "")
                            price = getattr(item, "price", "")
                            item_fields.extend([title, price])
                    
                    # Pad item_fields to fill remaining columns if fewer than max_items
                    while len(item_fields) < max_items * 2:
                        item_fields.extend(["", ""])
                    
                    writer.writerow(base_row + item_fields)
                
                print(f"Orders and items saved to {filename}")


def get_orders_and_update_csv(amazon_orders, year, max_orders, amazon_username, csv_filename="AmazonOrders_db.csv"):
    """
    Fetch Amazon orders for a specific year and update an existing CSV file.
    Only adds new orders/items that aren't already in the CSV file.
    Uses custom incremental IDs for orders that remain the same across items within the same order.
    
    Args:
        amazon_orders: AmazonOrders instance
        year (int): The year to fetch orders for
        max_orders (int): Maximum number of orders to fetch (or None for all)
        csv_filename (str): Name of the CSV file to update (default: "AmazonOrders_db.csv")
        
    Returns:
        tuple: (added_count, skipped_count) - counts of added and skipped items
    """
    import os
    import csv
    from datetime import datetime

    # Fetch orders
    print(f"Fetching up to {max_orders if max_orders else 'all'} orders from {year}...")
    orders = amazon_orders.get_order_history(
        year=year,
        max_orders=max_orders,
        full_details=True
    )
    
    if not orders:
        print("No orders found for the specified year.")
        return 0, 0
    
    # Check if the CSV file exists, create it if it doesn't
    file_exists = os.path.isfile(csv_filename)
    
    # Define the field names (added new columns)
    fieldnames = [
        'username',
        'custom_id',
        'order_details_link',
        'order_placed_date',
        'item_title',
        'item_price',
        'item_qty', 
        'payment_method',
        'payment_method_last_4',
        #'subtotal',
        #'postage_and_packing',
        #'total_before_vat',
        #'vat',
        'total',
        'promotion_applied',
        'gift_card_amount',
        'grand_total',
        'item_price_total',           
        'promotion_nondelivery',       
        'allocation',                  
        'item_price_paid',             
        'refund_total',
        'final_item_amount',
        'comments'
    ]
    
    # Read existing entries to compare against new orders and find the highest ID
    existing_entries = set()
    highest_id = 0
    order_links_to_ids = {}  
    
    if file_exists:
        with open(csv_filename, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Create a unique identifier for each order item
                entry_key = (row['order_details_link'], row['item_title'])
                existing_entries.add(entry_key)
                
                # Track the highest ID and maintain order link to ID mapping
                try:
                    current_id = int(row['custom_id'])
                    highest_id = max(highest_id, current_id)
                    
                    # Store the ID for this order link if not already mapped
                    if row['order_details_link'] not in order_links_to_ids:
                        order_links_to_ids[row['order_details_link']] = current_id
                except (ValueError, KeyError):
                    pass  # Skip if ID is not a valid integer or missing
    
    # Open the file for appending (or create new with headers)
    mode = 'a' if file_exists else 'w'
    with open(csv_filename, mode, newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # Write header only if creating a new file
        if not file_exists:
            writer.writeheader()
        
        added_count = 0
        skipped_count = 0
        next_id = highest_id + 1
        
        # Process each order
        for order in orders:
            order_link = getattr(order, 'order_details_link', '')
            
            # Determine the ID for this order
            # If this order link already has an ID, use it, otherwise assign a new one
            if order_link in order_links_to_ids:
                order_id = order_links_to_ids[order_link]
            else:
                order_id = next_id
                order_links_to_ids[order_link] = order_id
                next_id += 1
            
            # Check if the order has multiple items or a single item
            items = []
            if hasattr(order, 'items') and order.items:
                items = order.items
            elif hasattr(order, 'item') and order.item:
                items = [order.item]
            
            # Calculate item_price_total for the order
            item_price_total = 0
            # First pass to calculate item_price_total
            for item in items:
                item_price_str = getattr(item, 'price', 0)
                if item_price_str is None:
                    item_price_str = 0.0
                item_price_total += round(item_price_str,1)
            
            # Calculate promotion_nondelivery
            total = getattr(order, 'total', None)
            promotion_applied = getattr(order, 'promotion_applied', 0)
            
            # Add this line after processing total
            if item_price_total is None:
                item_price_total = 0.0
            if promotion_applied is None:
                promotion_applied = 0.0
            
            # Calculate promotion_nondelivery (negative values mean an extra charge)
            if total is None:
                promotion_nondelivery = 0.0
            else:
                promotion_nondelivery = round(total - item_price_total + promotion_applied, 1)
            
            if items:
                # Create a row for each item in the order
                for item in items:
                    #item_title = getattr(item, 'title', '')
                    full_title = getattr(item, 'title', '').strip()
                    item_title = (full_title[:47] + '...') if len(full_title) > 50 else full_title

                    comments = ''
                    item_qty = getattr(item, 'quantity', 1)
                    if item_qty is not None and item_qty > 1:
                        comments += "Please verify item price since qty > 1."

                    # Generate a unique key for this entry
                    entry_key = (order_link, item_title)
                    
                    # Skip if this entry already exists
                    if entry_key in existing_entries:
                        skipped_count += 1
                        continue
                    
                    # Get item price and convert to float
                    item_price = getattr(item, 'price', '0')
                    if item_price is None:
                        item_price = 0.0
                    
                    # Calculate allocation (avoid division by zero)
                    allocation = 0 if item_price_total == 0 else round(item_price / item_price_total, 1)
                    
                    # Calculate item_price_paid
                    item_price_paid = round(item_price + (allocation * promotion_nondelivery),1)

                    # Fetch refund value from order object (using getattr with default 0)
                    refund = getattr(order, 'refund_total', 0)
                    final_item_amount = round(item_price_paid,1)  # assume full item price initially
                    if refund is not None:
                        # If refund is within 95% of item_price_total
                        # or if refund is within 95% of item_price
                        if abs(refund - item_price_total) <= (0.05 * item_price_total) or abs(refund - item_price) <= (0.05 * item_price):
                            final_item_amount = 0
                        if not (refund == item_price_total or refund == item_price):
                            comments += " Please verify refunds are attributed correctly."
                    
                    # Add to CSV file
                    row = {
                        'username':amazon_username,
                        'custom_id': order_id,
                        'order_details_link': order_link,
                        'order_placed_date': getattr(order, 'order_placed_date', ''),
                        'item_title': item_title,
                        'item_price': item_price,
                        'item_qty': item_qty,
                        'payment_method': getattr(order, 'payment_method', ''),
                        'payment_method_last_4': getattr(order, 'payment_method_last_4', ''),
                        #'subtotal': getattr(order, 'subtotal', ''),
                        #'postage_and_packing': getattr(order, 'postage_and_packing', ''),
                        #'total_before_vat': getattr(order, 'total_before_vat', ''),
                        #'vat': getattr(order, 'vat', ''),
                        'total': getattr(order, 'total', ''),
                        'promotion_applied': getattr(order, 'promotion_applied', ''),
                        'gift_card_amount': getattr(order, 'gift_card_amount', ''),
                        'grand_total': getattr(order, 'grand_total', ''),
                        'item_price_total': round(item_price_total,1),
                        'promotion_nondelivery': round(promotion_nondelivery,1),
                        'allocation': round(allocation,1),
                        'item_price_paid': round(item_price_paid,1),
                        'refund_total': getattr(order, 'refund_total', ''),
                        'final_item_amount':final_item_amount,
                        'comments': comments
                    }
                    writer.writerow(row)
                    added_count += 1
    
    # Provide feedback to the user
    print(f"CSV update complete: {added_count} items added, {skipped_count} items skipped (already existed)")
    print(f"Database file: {csv_filename}")
    
    return added_count, skipped_count