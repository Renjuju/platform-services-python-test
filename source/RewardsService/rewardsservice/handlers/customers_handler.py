import json
import tornado.web
import logging
import math

from pymongo import MongoClient
from tornado.gen import coroutine


class CustomerHandler(tornado.web.RequestHandler):

    @coroutine
    def get(self):
        self.set_header('Content-Type', 'application/javascript')
        client = MongoClient("mongodb", 27017)
        db = client["customers"]
        customers = list(db.customers.find({}, {"_id": 0}))
        self.write(json.dumps(customers, indent = 4))

class PurchaseHandler(tornado.web.RequestHandler):

    def data_received(self, chunk):
        pass

    @coroutine
    def post(self, *args, **kwargs):
        self.set_header('Content-Type', 'application/javascript')

        purchase = json.loads(self.request.body.decode('utf-8'))
        if 'email' not in purchase or 'purchase' not in purchase:
            self.write_error(404)
            return

        client = MongoClient("mongodb", 27017)
        db = client["customers"]
        rewards_db = client['Rewards']

        customer = db.customers.find_one({"email": str(purchase['email'])})
        rewards = list(rewards_db.rewards.find({}, {"_id": 0}))
        points = math.floor(purchase['purchase'])
        email = purchase['email']

        new_customer, next_rewards_tier, next_reward_name, next_rewards_tier_progress = None, None, None, None

        totalRewards = len(rewards) - 1
        rewards_tier = ''
        rewards_name = ''

        # New Customers
        if customer is None:
            for idx, reward in enumerate(rewards):
                if idx < totalRewards:
                    if points >= rewards[idx]['points'] and points < rewards[idx + 1]['points']:
                        rewards_tier = reward['tier']
                        rewards_name = reward['rewardName']
                        next_rewards_tier = rewards[idx + 1]['tier']
                        next_reward_name = rewards[idx + 1]['rewardName']
                        next_rewards_tier_progress = round(1 - (rewards[idx + 1]['points'] - points ) / 100, 2)
                elif idx is totalRewards:
                    rewards_tier = reward['tier']
                    rewards_name = reward['rewardName']

            new_customer = {
                'email': email,
                'points': points,
                'rewards_tier': rewards_tier,
                'rewards_name': rewards_name,
                'next_rewards_tier': next_rewards_tier,
                'next_rewards_name': next_reward_name,
                'next_rewards_progress': next_rewards_tier_progress
            }
            print ('no email associated, creating new account')
        else:
            print ('reached if statement')
            print (customer)


        # customer = list(db.customers.find({"email": str(customer['email'])}))
        if new_customer is not None:
            print('new customer' + json.dumps(new_customer))
            self.write(json.dumps(new_customer, indent=4))
            db.customers.insert(new_customer)
            return
        customer.pop('_id')
        self.write(json.dumps(customer, indent=4))
