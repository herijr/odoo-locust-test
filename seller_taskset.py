from locust import task, TaskSet
from locust.wait_time import between
from OdooLocust import OdooLocust
import os

from dotenv import load_dotenv
load_dotenv()


class SellerTaskSet(TaskSet):
    @task(10)
    def read_partners(self):
        cust_model = self.client.get_model('res.partner')
        cust_ids = cust_model.search([])
        prtns = cust_model.read(cust_ids)

    @task(5)
    def read_products(self):
        prod_model = self.client.get_model('product.product')
        ids = prod_model.search([])
        prods = prod_model.read(ids)

    @task(20)
    def create_so(self):
        prod_model = self.client.get_model('product.product')
        cust_model = self.client.get_model('res.partner')
        so_model = self.client.get_model('sale.order')

        cust_id = cust_model.search([('name', 'ilike', 'fletch')])[0]
        prod_ids = prod_model.search([('name', 'ilike', 'ipad')])

        order_id = so_model.create({
            'partner_id': cust_id,
            'order_line': [(0, 0, {'product_id': prod_ids[0],
                                   'product_uom_qty': 1}),
                           (0, 0, {'product_id': prod_ids[1],
                                   'product_uom_qty': 2}),
                           ],

        })
        so_model.action_button_confirm([order_id, ])


class Seller(OdooLocust.OdooLocust):
	host = os.getenv('HOST')
	database = os.getenv('DATABASE')
	port = int(os.getenv('PORT'))
	login = os.getenv('LOGIN')
	password = os.getenv('PASSWORD')
	wait_time = between(0.500, 4)
	weight = 3

	task_set = SellerTaskSet