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

class Seller(OdooLocust.OdooLocust):
	host = os.getenv('HOST')
	database = os.getenv('DATABASE')
	port = int(os.getenv('PORT'))
	login = os.getenv('LOGIN')
	password = os.getenv('PASSWORD')
	wait_time = between(0.500, 4)
	weight = 3

	task_set = SellerTaskSet
