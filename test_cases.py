# test_cases.py

import unittest
from praveen_inventory_system import (
    create_inventory,
    update_inventory,
    merge_inventories,
    get_items_in_category,
    find_most_expensive_item,
    check_item_in_stock,
    view_categories,
    view_all_items,
    view_category_item_pairs,
    copy_inventory
)


class TestInventorySystem(unittest.TestCase):

    def setUp(self):
        self.inventory = create_inventory()

    def test_create_inventory(self):
        self.assertIsInstance(self.inventory, dict)
        self.assertIn('Electronics', self.inventory)
        self.assertIn('Groceries', self.inventory)

    def test_update_inventory(self):
        update_info = {'price': 1200, 'quantity': 7}
        update_inventory(self.inventory, 'Electronics', 'Laptop', update_info)
        item = self.inventory['Electronics']['Laptop']
        self.assertEqual(item['price'], 1200)
        self.assertEqual(item['quantity'], 7)

    def test_merge_inventories(self):
        inv1 = create_inventory()
        inv2 = {
            'Electronics': {
                'Laptop': {'name': 'Laptop', 'price': 1100, 'quantity': 3},
                'Tablet': {'name': 'Tablet', 'price': 500, 'quantity': 15}
            },
            'Clothing': {
                'Jeans': {'name': 'Jeans', 'price': 40, 'quantity': 50}
            }
        }
        merged_inv = merge_inventories(inv1, inv2)
        self.assertIn('Clothing', merged_inv)
        self.assertIn('Tablet', merged_inv['Electronics'])
        self.assertEqual(merged_inv['Electronics']['Laptop']['quantity'], 8)

    def test_get_items_in_category(self):
        electronics = get_items_in_category(self.inventory, 'Electronics')
        self.assertIsInstance(electronics, dict)
        self.assertIn('Laptop', electronics)

    def test_find_most_expensive_item(self):
        most_expensive = find_most_expensive_item(self.inventory)
        self.assertIsNotNone(most_expensive)
        self.assertEqual(most_expensive['name'], 'Laptop')

    def test_check_item_in_stock(self):
        item = check_item_in_stock(self.inventory, 'Laptop')
        self.assertIsNotNone(item)
        self.assertEqual(item['name'], 'Laptop')
        self.assertGreater(item['quantity'], 0)

        item = check_item_in_stock(self.inventory, 'NonExistingItem')
        self.assertIsNone(item)

    def test_view_categories(self):
        categories = view_categories(self.inventory)
        self.assertIn('Electronics', categories)
        self.assertIn('Groceries', categories)

    def test_view_all_items(self):
        all_items = view_all_items(self.inventory)
        self.assertTrue(len(all_items) > 0)
        item_names = [item['name'] for item in all_items]
        self.assertIn('Laptop', item_names)

    def test_view_category_item_pairs(self):
        pairs = view_category_item_pairs(self.inventory)
        self.assertTrue(len(pairs) > 0)
        categories = [category for category, _ in pairs]
        self.assertIn('Electronics', categories)

    def test_copy_inventory(self):
        # Test deep copy
        inv_copy = copy_inventory(self.inventory, deep=True)
        self.assertEqual(inv_copy, self.inventory)
        inv_copy['Electronics']['Laptop']['price'] = 2000
        self.assertNotEqual(inv_copy['Electronics']['Laptop']['price'],
                            self.inventory['Electronics']['Laptop']['price'])

        # Test shallow copy
        inv_shallow_copy = copy_inventory(self.inventory, deep=False)
        inv_shallow_copy['Electronics']['Laptop']['price'] = 2500
        self.assertEqual(inv_shallow_copy['Electronics']['Laptop']['price'],
                         self.inventory['Electronics']['Laptop']['price'])

if __name__ == '__main__':
    unittest.main()
