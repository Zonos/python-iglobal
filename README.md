# python-iglobal
====================================

Welcome to the documentation for python-iglobal

Basic Usage
-----------------------------

	import iglobal
	
	api = iglobal.Api(store_id="<store_id>", secret_key="<secret_key>")

	# Fetch all iGlobal international Order Numbers
	orders = api.all_orders()

	# Fetch Order Numbers from certain date
	orders = api.order_numbers(since_date='20151101')

	# Fetch Order Details of specific order
	order = api.order_details(order_id='999-99999')

All responses are decoded json while any none 200 response raises an exception.
