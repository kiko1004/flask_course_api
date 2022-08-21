from resources.analysis import *
from resources.payment import *
from resources.signup_login_controller import *

routes = (
    (SignUp, "/register"),
    (Login, "/login"),
    (Recommendation, "/recommendation"),
    (BalanceSheet, "/balancesheet"),
    (Analysis, "/analysis"),
    (PaymentProcessor, "/upgrade"),
    (SuccessfulPayment, "/success_payment"),
    (FailedPayment, "/failed_payment"),
    (Webhook, "/webhook"),
    (ViewMyAnalysis, "/view_my_analysis"),
)
