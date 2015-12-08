Python iGlobal

# Introduction
This library provides a python interface for the iGlobalStores API.


# Basic Usage

```python
	import iglobal

	api = iglobal.Api(store_id="<store_id>", secret_key="<secret_key>")

	# Fetch all iGlobal international Order Numbers
	orders = api.all_orders()

	# Fetch Order Numbers from certain date
	orders = api.order_numbers(since_date='20151101')

	# Fetch Order Details of specific order
	order = api.order_details(order_id='999-99999')

	# Update an Order with a new Merchant Order ID
	response = api.update_merchant_order_id(order_id="123-1234", merchant_order_id="123456")
```

Responses are returned as Python namedtuples decoded from JSON. Non-200 responses from the API will raise an iGlobalException.

# Testing

To run the unit tests:

```
	python test.py
```
