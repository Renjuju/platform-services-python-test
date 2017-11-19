from handlers.rewards_handler import RewardsHandler
from handlers.customers_handler import PurchaseHandler
from handlers.customers_handler import  CustomerHandler
url_patterns = [
    (r'/rewards', RewardsHandler),
    (r'/purchase', PurchaseHandler),
    (r'/customers', CustomerHandler)
]
