import unittest
import iglobal
from iglobal.exceptions import iGlobalException

class ApiTest(unittest.TestCase):
    def setUp(self):
        self.api = iglobal.Api(store_id=0, secret_key="secret key")

    def test_all_orders(self):
        pass

    def test_order_numbers(self):
        # test incorrect since_date type
        self.assertRaises(iGlobalException, self.api.order_numbers, since_order_id="100", since_date=0)
        # test incorrect through_date type
        self.assertRaises(iGlobalException, self.api.order_numbers, since_order_id="100", through_date=0)
        # test incorrect argument set (since_order_id or since_date required)
        self.assertRaises(iGlobalException, self.api.order_numbers, through_date=0)

    def test_order_details(self):
        # test incorrect argument set
        self.assertRaises(iGlobalException, self.api.order_details)
        # test incorrect reference_id type
        self.assertRaises(iGlobalException, self.api.order_details, reference_id=0)

    def test_update_merchant_order_id(self):
        # test incorrect argument set
        self.assertRaises(iGlobalException, self.api.update_merchant_order_id)
        self.assertRaises(iGlobalException, self.api.update_merchant_order_id, order_id="123-1234")
        self.assertRaises(iGlobalException, self.api.update_merchant_order_id, merchant_order_id="12345678")
        # test incorrect merchant_order_id type
        self.assertRaises(iGlobalException, self.api.update_merchant_order_id, order_id="123-1234", merchant_order_id=0)

    def test_update_vendor_order_status(self):
        # test incorrect argument set
        self.assertRaises(iGlobalException, self.api.update_vendor_order_status)
        self.assertRaises(iGlobalException, self.api.update_vendor_order_status, order_id="123-1234")
        self.assertRaises(iGlobalException, self.api.update_vendor_order_status, status="IGLOBAL_FRAUD_REVIEW")
        # test incorrect stauts type
        self.assertRaises(iGlobalException, self.api.update_vendor_order_status, order_id="123-1234", status=0)

    def test_create_temp_cart(self):
        # test incorrect argument set
        self.assertRaises(TypeError, self.api.create_temp_cart)
        # test empty data
        data = {}
        self.assertRaises(iGlobalException, self.api.create_temp_cart, data=data)
        # test wrong items type
        data['items'] = "{'description': 'this is a JSON string.'}"
        self.assertRaises(iGlobalException, self.api.create_temp_cart, data=data)
        # test wrong item type
        data['items'] = ["bad item type"]
        self.assertRaises(iGlobalException, self.api.create_temp_cart, data=data)
        # test no item data (also tests no item description)
        data['items'] = [{}]
        self.assertRaises(iGlobalException, self.api.create_temp_cart, data=data)
        # test bad item description type
        data['items'] = [{"description": 1}]
        self.assertRaises(iGlobalException, self.api.create_temp_cart, data=data)
        # test no item quantity
        data['items'] = [{"description": "test"}]
        self.assertRaises(iGlobalException, self.api.create_temp_cart, data=data)
        # test bad quantity type
        data['items'] = [{"description": "test", "quantity": "spam"}]
        self.assertRaises(iGlobalException, self.api.create_temp_cart, data=data)
        # test no item unit price
        data['items'] = [{"description": "test", "quantity": 1}]
        self.assertRaises(iGlobalException, self.api.create_temp_cart, data=data)
        # test bad unit price type
        data['items'] = [{"description": "test", "quantity": 1, "unitPrice": 3.00}]
        self.assertRaises(iGlobalException, self.api.create_temp_cart, data=data)
