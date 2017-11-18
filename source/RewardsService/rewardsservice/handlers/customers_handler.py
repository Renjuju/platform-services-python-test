import json
import tornado.web
import logging

from pymongo import MongoClient
from tornado.gen import coroutine


class CustomersHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass


class PurchaseHandler(tornado.web.RequestHandler):

    def data_received(self, chunk):
        pass

    @coroutine
    def post(self, *args, **kwargs):
        purchase = json.loads(self.request.body.decode('utf-8'))
        client = MongoClient("mongodb", 27017)
        db = client["Purchases"]

        # customer = list(db.customers.find({"email": str(customer['email'])}))

        db.customers.insert_one(purchase)
        purchases = list(db.customers.find({}, {"_id": 0}))
        self.write(json.dumps(purchases))

        # update customer
        db = client["Customer"]

