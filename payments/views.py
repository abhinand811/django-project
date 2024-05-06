import stripe
from django.http import JsonResponse
from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from ManagementProject.settings import STRIPE_SECRET_KEY


class CreateCheckoutSession(APIView):

    def post(self, request):
        stripe.api_key = STRIPE_SECRET_KEY
        dataDict = dict(request.data)
        print(dataDict)
        price = dataDict['price']
        print(price)
        product_name = dataDict['product_name']
        try:
            checkout_session = stripe.checkout.Session.create(
                line_items=[{
                    'price_data': {
                        'currency': 'inr',
                        'product_data': {
                            'name': product_name,
                        },
                        'unit_amount': int(price)*100
                    },
                    'quantity': 1
                }],
                mode='payment',
                success_url="https://www.google.com",
                cancel_url="https://www.yahoo.com"
            )
            print('hi')
            return Response(data={"url": checkout_session.url})
        except Exception as e:
            print(e)
            return Response(data={"message": str(e)}, status=400)


class WebHook(APIView):
    def post(self, request):
        event = None
        payload = request.body
        sig_header = request.META['HTTP_STRIPE_SIGNATURE']

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, webhook_secret
            )
        except ValueError as err:
            # Invalid payload
            raise err
        except stripe.error.SignatureVerificationError as err:
            # Invalid signature
            raise err

        # Handle the event
        if event.type == 'payment_intent.succeeded':
            payment_intent = event.data.object
            print("--------payment_intent ---------->", payment_intent)
        elif event.type == 'payment_method.attached':
            payment_method = event.data.object
            print("--------payment_method ---------->", payment_method)
        # ... handle other event types
        else:
            print('Unhandled event type {}'.format(event.type))

        return JsonResponse(success=True, safe=False)
