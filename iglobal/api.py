import requests


class API(object):
    """
    API object to store and handle all requests through the iGlobal REST API,
    Refer to developer.iglobalstores.com/api/1.0/ for responses and expected data
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

    def __init__(self, store_id, secret_key, **kwargs):
        if not store_id:
            raise Exception("Store ID is required to access the iGlobal REST API.")
        if not secret_key:
            raise Exception("Secret Key is required to access the iGlobal REST API.")
        self.store_id = store_id,
        self.secret_key = secret_key
        self.entry_point = "https://api.iglobalstores.com/v1/{}"

    def _callAPI(self, path, data):
        data.update('store', self.store_id)
        data.update('secret', self.secret_key)
        r = requests.post(self.entry_point.format(path), json=data)

        if r.status_code == 200:
            return r.json()
        else:
            return False

    def _convert_date(self, date):
        return date.strftime('%Y%m%d')

    def all_orders(self):
        return self.order_numbers(since_date='20150101')

    def order_numbers(self, since_order_id=None, since_date=None, through_date=None):
        data = {}
        if since_order:
            data['sinceOrderId'] = since_order_id
        elif since_date:
            if hasattr(since_date, 'strftime'):
                since_date = self._convert_date(since_date)
            data['sinceDate'] = since_date
            if through_date:
                if hasattr(through_date, 'strftime'):
                    through_date = self._convert_date(through_date)
                data['throughDate'] = through_date
        else:
            raise Exception('since_order or since_date is required.')

        return self._callAPI('orderNumbers', data)

    def order_details(self, order_id=None, reference_id=None):
        data = {}
        if order_id:
            data['orderId'] = order_id
        elif reference_id:
            data['referenceId'] = reference_id
        else:
            raise Exception('order_id or reference_id is required.')

        return self._callAPI('orderDetail', data)

    def update_merchant_order_id(self, order_id, merchant_order_id):
        data = {
            'orderId': order_id,
            'merchantOrderId': merchant_order_id
        }
        return self._callAPI('updateMerchantOrderId', data)

    def update_vendor_order_status(self, order_id, status):
        data = {
            'orderId': order_id,
            'orderStatus': status
        }
        return self._callAPI('updateVendorOrderStatus', data)

    def create_temp_cart(self, data):
        return self._callAPI('createTempCart', data)
