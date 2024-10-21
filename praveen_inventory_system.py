# inventory_system.py
import copy
def create_inventory():
    """
    Create and return an inventory using different dictionary creation methods,
    including dictionary comprehensions and dict() constructor.
    """
    inventory = {
            'Electronics': {
                'Laptop': {'name': 'Laptop', 'price': 1100, 'quantity': 5}
            },
            'Groceries': {
                'Rice': {'name': 'Rice', 'price': 100, 'quantity': 1000},
                'Oil': {'name': 'Oil', 'price': 220, 'quantity': 50}
            }
        }
    
    return inventory

def update_inventory(inventory, category, item_name, update_info):
    """
    Update item information (e.g., increasing stock, updating price) in the inventory.
    """
    
    for update_key, update_value in update_info.items():
        inventory[category][item_name][update_key] = update_value
    return

def merge_inventories(inv1, inv2):
    """
    Merge two inventory systems without losing any data.
    """
    for key,value in inv2.items():
        if key not in inv1:
            inv1[key] = value
        else:
            for inner_key, inner_value in inv2[key].items():
                if inner_key not in inv1[key]:
                    inv1[key][inner_key] = inner_value
                else:
                    new_quantity = inv1[key][inner_key]['quantity'] + inv2[key][inner_key]['quantity']
                    inv1[key][inner_key]['quantity'] = new_quantity
    
    return inv1


def get_items_in_category(inventory, category):
    """
    Retrieve all items in a specified category.
    """
    return inventory[category]

def find_most_expensive_item(inventory):
    """
    Find and return the most expensive item in the inventory.
    """
    most_expensive = {}
    price = 0
    for values in inventory.values():
        for key,value in values.items():
            if 'price' in value:
                if value['price'] > price:
                    price = value['price']
                    most_expensive['name'] = key
    
    return most_expensive
def check_item_in_stock(inventory, item_name):
    """
    Check if an item is in stock and return its details if available.
    """
    for values in inventory.values():
        if (item_name in values) and (values[item_name]['quantity'] > 0):
            return values[item_name]
        else:
            return None        


def view_categories(inventory):
    """
    View available categories (keys of the outer dictionary).
    """
    return inventory

def view_all_items(inventory):
    """
    View all items (values of the inventory).
    """
    all_items = []
    for items in inventory.values():
        for item in items.values():
            all_items.append(item)

    return(all_items)

def view_category_item_pairs(inventory):
    """
    View category-item pairs (items view of the inventory).
    """
    pairs = []
    for category,items in inventory.items():
        for item in items:
            pairs.append((category,item))
    return pairs
    
def copy_inventory(inventory, deep=True):
    """
    Copy the entire inventory structure. Use deep copy if deep=True, else use shallow copy.
    """
    if deep:
        inventory_copy = copy.deepcopy(inventory)
    else:
        inventory_copy = inventory.copy()
    return inventory_copy
