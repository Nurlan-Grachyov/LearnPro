import json

import requests
import stripe
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from config.settings import API_KEY


@csrf_exempt
def create_product(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        product_name = data.get('name')
        param = {'name': product_name}

        response = requests.post('https://api.stripe.com/v1/products', data=param,
                                 headers={
                                     'Authorization': f'Bearer {API_KEY}'
                                 })
        product_data = response.json()
        product_id = product_data['id']
        print(product_id)
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'fail'}, status=400)


@csrf_exempt
def create_price(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        print(data)
        product = data.get('product_data')
        unit_amount = data.get('unit_amount')
        product = json.dumps(product)

        param = {"unit_amount": unit_amount,
                 "product_data": product, "currency": "usd"}

        response = requests.post('https://api.stripe.com/v1/prices', data=param, headers={
            'Authorization': f'Bearer {API_KEY}'
        })

        price_data = response.json()
        print(price_data)
        price_id = price_data['id']
        print(price_id)
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'fail'}, status=400)


@csrf_exempt
def create_session(request):
    if request.method == 'POST':
        price = request.POST.get('price')
        response = requests.post('https://api.stripe.com/v1/products', data={
            'price': price
        }, headers={
            'Authorization': f'Bearer {API_KEY}'
        })
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'fail'}, status=400)
