from handlers.rewards_handler import RewardsHandler
from handlers.customers_handler import PurchaseHandler

url_patterns = [
    (r'/rewards', RewardsHandler),
    (r'/purchase', PurchaseHandler)
]
