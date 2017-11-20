import logging
import requests
import json

from django.template.response import TemplateResponse
from django.views.generic.base import TemplateView


class RewardsView(TemplateView):
    template_name = 'index.html'

    def __init__(self, logger=logging.getLogger(__name__)):
        self.logger = logger

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if  request.method == 'GET' and 'email' in request.GET and 'total' in request.GET:
            if request.GET['email'] and request.GET['total']:
                payload = {
                    'email': request.GET['email'],
                    'purchase': float(request.GET['total'])
                }
                print(payload)
                r = requests.post('http://rewardsservice:7050/purchase', data=json.dumps(payload))
                print(r)
        if request.method == 'GET' and 'email' in request.GET and 'total' not in request.GET:
            payload = {
                'email': request.GET['email']
            }
            customerResponse = requests.post('http://rewardsservice:7050/customers', data=json.dumps(payload))
            print(customerResponse.json())
            customers = []
            customers.append(customerResponse.json())
            context['customers'] = customers
        else:
            customerResponse = requests.get('http://rewardsservice:7050/customers')
            context['customers'] = customerResponse.json()

        response = requests.get("http://rewardsservice:7050/rewards")
        context['rewards_data'] = response.json()

        return TemplateResponse(
            request,
            self.template_name,
            context
        )