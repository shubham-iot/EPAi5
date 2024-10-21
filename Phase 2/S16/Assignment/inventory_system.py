# inventory_system.py
import copy

def create_inventory():
    """
    Create and return an inventory using different dictionary creation methods,
    including dictionary comprehensions and dict() constructor.
    """
    electronics = dict()
    #electronics['mobile'] = 'Moto g84'
    electronics['laptop'] = {'name': 'Laptop', 'price': 1100, 'quantity': 5}
    grocery = dict([("Rice", {'name': 'Rice', 'price': 100, 'quantity': 1000}),("oil", dict(name='Oil', price=220, quantity=50))])
    category = [electronics, grocery]
    keys = ['Electronics', 'Groceries']
    inventory = dict(((keys[0], electronics), (keys[1], grocery)))
    return inventory

def update_inventory(inventory, category, item_name, update_info):
    """
    Update item information (e.g., increasing stock, updating price) in the inventory.
    """
    """
    for k,v in update_info.items():
        inventory[category][item_name][k] = v
    return
    """
    for update_key, update_value in update_info.items():
        inventory[category][item_name][update_key] = update_value
    return

def merge_inventories(inv1, inv2):
    """
    Merge two inventory systems without losing any data.
    """
    newKeys = inv2.keys() - inv1.keys()
    commonKeys = inv1.keys() & inv2.keys()
    for key in newKeys:
        inv1[key] = inv2[key]

    for key in commonKeys:
        newInnerKeys = inv2[key].keys() - inv1[key].keys()
        commonInnerKeys = inv1[key].keys() & inv2[key].keys()
        for innerKey in newInnerKeys:
            inv1[key][innerKey] = inv2[key][innerKey]
        for innerKey in commonInnerKeys:
            inv1[key][innerKey]['quantity'] += inv2[key][innerKey]['quantity']

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
    maxPrice = 0
    expensiveItem = None
    for category in inventory.values():
        for item in category.values():
            if item['price'] > maxPrice:
                maxPrice = item['price']
                expensiveItem = item

    return expensiveItem

def check_item_in_stock(inventory, item_name):
    """
    Check if an item is in stock and return its details if available.
    """
    for _,v in inventory.values():
        if item_name in v and v[item_name]['quantity'] > 0:
            return v[item_name]
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
        all_items.extend(items.values())
    return all_items

def view_category_item_pairs(inventory):
    """
    View category-item pairs (items view of the inventory).
    """
    pairs = []
    for category, items in inventory.items():
        for item in items:
            pairs.append((category, item))
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
