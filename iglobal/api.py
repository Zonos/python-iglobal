import json
import requests
import six
from decimal import Decimal
from collections import namedtuple
from .exceptions import iGlobalException, iGlobalUnauthorizedException


class Api(object):
    """
    API object to store and handle all requests through the iGlobal REST API,
    Refer to https://developer.iglobalstores.com/api/1.0/ for responses and expected data
    """
    STATUS_FRAUD = "IGLOBAL_FRAUD_REVIEW" # The order is currently under fraud review by iGlobal. *Settable by: iGlobal System
    STATUS_PROCESS = "IGLOBAL_ORDER_IN_PROCESS" # The order is valid and ready for processing. *Settable by: iGlobal System
    STATUS_HOLD = "IGLOBAL_ORDER_ON_HOLD" # The order is currently on a temporary status hold. *Settable by: iGlobal System
    STATUS_CANCELLED = "IGLOBAL_ORDER_CANCELLED" # The order has been cancelled in the iGlobal System. *Settable by: iGlobal System
    STATUS_VENDOR_PREPARE = "VENDOR_PREPARING_ORDER" # The vendor has marked the order in preparation. *Settable by: Vendor
    STATUS_VENDOR_READY = "VENDOR_SHIPMENT_READY" # The vendor has marked the order ready for shipping. *Settable by: Vendor
    STATUS_VENDOR_LABELS = "VENDOR_LABELS_PRINTED_DATE" # The vendor has printed shipping labels. *Settable by: Vendor
    STATUS_VENDOR_CANCEL = "VENDOR_CANCELLATION_REQUEST" # The order has been requested for cancellation. *Settable by: Vendor
    STATUS_VENDOR_COMPLETE = "VENDOR_END_OF_DAY_COMPLETE" # The order is finalized and complete. *Settable by: Vendor

    def __init__(self, store_id=None, secret_key=None, *args, **kwargs):
        '''
            Instantiates a new iGlobal API object.
        '''
        if store_id is None or secret_key is None:
            raise iGlobalUnauthorizedException("iGlobal requires a Store ID and Secret Key to access the iGlobal REST API.")
        if not isinstance(store_id, six.integer_types):
            raise iGlobalException("Error: store_id must be an integer.")
        if not isinstance(secret_key, six.string_types):
            raise iGlobalException("Error: secret_key must be a string.")

        self.store_id = store_id
        self.secret_key = secret_key
        self.base_url = "https://api.iglobalstores.com/v1/{0}"

    def _callAPI(self, path, data):
        data.update({'store': self.store_id})
        data.update({'secret': self.secret_key})
        response = requests.post(self.base_url.format(path), json=data)

        if response.status_code == 200:
            return response.content
        else:
            raise iGlobalException(
                "iGlobal API Error {0}: {1}".format(
                    response.status_code, response.text
                )
            )

    def _convert_date(self, date):
        '''
            Returns a date formatted for the REST API.
        '''
        return date.strftime('%Y%m%d')

    def all_orders(self):
        return self.order_numbers(since_date='20000101')

    def order_numbers(self, since_order_id=None, since_date=None, through_date=None):
        '''
            Fetch a sequence of order numbers in a date range, or all orders
            after a specific Order ID.

            Returns a namedtuple containing an order count and list of orders.

            Args:
                since_order_id:
                    The starting order ID. Orders that appear before this ID
                    will be filtered from the results.
                since_date:
                    The starting date for the filter. Orders that have occurred
                    before this date will be filtered from the results.
                through_date:
                    Optional end date for the filter. If specified, the results
                    will not include orders that occur after that date.
        '''
        data = {}
        if since_order_id is not None:
            data['sinceOrderId'] = since_order_id
        elif since_date is not None:
            if hasattr(since_date, 'strftime'):
                since_date = self._convert_date(since_date)
            data['sinceDate'] = since_date
            if through_date:
                if hasattr(through_date, 'strftime'):
                    through_date = self._convert_date(through_date)
                data['throughDate'] = through_date
        else:
            raise iGlobalException('since_order_id or since_date is required.')

        api_data = self._callAPI('orderNumbers', data)
        products = json.loads(api_data, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))

        return products

    def order_details(self, order_id=None, reference_id=None):
        '''
            Retrieves the order details and status of an Order completed via the
            iGlobal Stores Checkout.

            Returns a namedtuple with the order details.

            Args:
                order_id (optional):
                    The ID of the Order to be retrieved. If this argument is not
                    provided, the order will be fetched using reference_id.
                reference_id (optional):
                    The reference to an Order's data passed in the
                    createTempCart endpoint. This argument will be ignored if
                    order_id is present.
        '''
        data = {}
        if order_id:
            data['orderId'] = order_id
        elif reference_id:
            if isinstance(reference_id, six.string_types):
                data['referenceId'] = reference_id
            else:
                raise iGlobalException('reference_id must be a string.')
        else:
            raise iGlobalException('order_id or reference_id is required.')

        api_data = self._callAPI('orderDetail', data)
        product = json.loads(api_data, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))

        return product.order

    def update_merchant_order_id(self, order_id=None, merchant_order_id=None):
        '''
            Updates an Order to use a new Merchant Order ID.

            Args:
                order_id:
                    The ID of the Order to be updated.
                merchant_order_id:
                    The new merchant order ID for the order to use.
        '''
        if order_id is None or merchant_order_id is None:
            raise iGlobalException('order_id and merchant_order_id are required.')
        if not isinstance(merchant_order_id, six.string_types):
            raise iGlobalException('merchant_order_id must be a string.')
        data = {
            'orderId': order_id,
            'merchantOrderId': merchant_order_id
        }
        api_data = self._callAPI('updateMerchantOrderId', data)
        order = json.loads(api_data, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
        return order

    def update_vendor_order_status(self, order_id=None, status=None):
        '''
            Updates an Order's status in the iGlobalStores System.

            Returns order details (see order_details).

            Args:
                order_id:
                    The ID of the Order to be updated.
                status:
                    The new status of the Order.
        '''
        if order_id is None or status is None:
            raise iGlobalException("order_id and status are required.")
        if not isinstance(status, six.string_types):
            raise iGlobalException("status must be a string.")
        data = {
            'orderId': order_id,
            'orderStatus': status
        }
        api_data = self._callAPI('updateVendorOrderStatus', data)
        order = json.loads(api_data, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
        return order

    def create_temp_cart(self, data):
        '''
            Passes shopping cart details to the iGlobal Stores Checkout.
            The response will contain a tempCartUUID.

            Args:
                data:
                    A python dictionary containing the cart data.

            Sample data (only inc. required fields):
                data = {
                    "items": [{"description": "test", "quantity": 1, "unitPrice": 1.00}]
                }
        '''
        if not isinstance(data, dict):
            raise iGlobalException("data must be a python dictionary object.")
        else:
            if not data.get('items'):
                raise iGlobalException("data['items'] is required.")
            elif not isinstance(data.get('items'), list):
                raise iGlobalException("data['items'] must contain a list of objects.")
            for item in data.get('items'):
                if not isinstance(item, dict):
                    raise iGlobalException("items must be python dictionary objects.")
                if not item.get('description') or not item.get('quantity') or not item.get('unitPrice'):
                    raise iGlobalException("description, quantity, and unitPrice are required for all items.")
                if not isinstance(item.get('description'), six.string_types):
                    raise iGlobalException("item description must be a string.")
                if not isinstance(item.get('quantity'), six.integer_types):
                    raise iGlobalException("item quantity must be an integer.")
                if not isinstance(item.get('unitPrice'), Decimal):
                    raise iGlobalException("item unit price must be a Decimal.")
                    if item.get('unitPrice') != item.get('unitPrice').quantize(Decimal('0.00')):
                        raise iGlobalException("item unit price must have two decimal points.")

        return self._callAPI('createTempCart', data)
