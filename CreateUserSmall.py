import sys
import os
import django

sys.path.append("../../../OfferGreatParis.settings")
os.environ["DJANGO_SETTINGS_MODULE"] = "OfferGreatParis.settings"
django.setup()



print("toto")
# print(People.objects.all()[0].any_fild)

from django.contrib.auth.models import User

try:
    userBussiere = User.objects.create_user("bussiere", password="rpgjdr09")
    userBussiere.is_superuser = True
    userBussiere.is_staff = True
    userBussiere.save()
except:
    pass

try:
    userBulle = User.objects.create_user("bulle", password="bullebulle")
    userBulle.is_superuser = True
    userBulle.is_staff = True
    userBulle.save()
except:
    pass

try:
    userAlex = User.objects.create_user("alex", password="alexalex")
    userAlex.is_superuser = True
    userAlex.is_staff = True
    userAlex.save()
except:
    pass
