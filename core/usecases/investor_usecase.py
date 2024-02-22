from db.models import Investor, Wallet
from django.contrib.auth.models import User

def create_investor(name, last_name, phone, email, password):
    user_already_exists = User.objects.filter(email=email, username=email).exists()
    if user_already_exists:
        raise Exception('Usuario existente') # todo: response with bad request
    
    user = User(email=email, username=email)
    
    user.set_password(password)
    user.save()

    investor = Investor(name=name, last_name=last_name, phone=phone, user=user)
    investor.save()

    Wallet(investor=investor).save()
    
    return investor