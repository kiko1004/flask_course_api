from flask_httpauth import HTTPTokenAuth
from flask_restful import Resource
from flask import request, url_for, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from db import db
from models import AnalystsModel, UserRole
from decouple import config
import stripe


auth = HTTPTokenAuth(scheme='Bearer')
stripe_sk = config('STRIPE_SK')
endpoint_secret = config('ENDPOING_SECRET')
stripe.api_key = stripe_sk

@auth.verify_token
def verify_token(token):
    try:
        user_id = AnalystsModel.decode_token(token=token)
        return AnalystsModel.query.filter_by(id=user_id).first()
    except:
        return False

class PaymentProcessor(Resource):
    @auth.login_required
    def get(self):
        curr_user = auth.current_user()
        data = request.args.to_dict()
        token = curr_user.encode_token()
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    'price': 'price_1LRHOiFgvSt64No9xglF7727',
                    'quantity': 1,
                },
            ],
            mode='subscription',
            success_url=request.base_url.replace('upgrade', 'success_payment') +'?token=' + token,
            cancel_url=request.base_url.replace('upgrade', 'fail_payment') +'?token=' + token
        )
        return checkout_session.url, 200

class SuccessfulPayment(Resource):
    def get(selfs):
        data = request.args.to_dict()
        user_id = AnalystsModel.decode_token(token=data['token'])
        user = AnalystsModel.query.filter_by(id=user_id).first()
        user.role = UserRole.Premium
        db.session.commit()
        return f"Successful Payment, User: {user.email}", 200

class FailedPayment(Resource):
    def get(selfs):
        data = request.args.to_dict()
        user_id = AnalystsModel.decode_token(token=data['token'])
        user = AnalystsModel.query.filter_by(id=user_id).first()
        return f"Payment Failed, User: {user.email}", 200

class Webhook(Resource):
    def post(self):
        event = None
        payload = request.data
        sig_header = request.headers['STRIPE_SIGNATURE']

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, endpoint_secret
            )
        except ValueError as e:
            # Invalid payload
            raise e
        except stripe.error.SignatureVerificationError as e:
            # Invalid signature
            raise e

        # Handle the event
        if event['type'] == 'payment_intent.succeeded':
            payment_intent = event['data']['object']
            #Webhook integration when alive

        # ... handle other event types
        else:
            print('Unhandled event type {}'.format(event['type']))
