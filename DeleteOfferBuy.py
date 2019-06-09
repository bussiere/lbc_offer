import sys
import os
import django

sys.path.append("../../../Offer_Annonce_GreatParis")
os.environ["DJANGO_SETTINGS_MODULE"] = "OfferGreatParis.settings"
django.setup()

from Offer.models import Buy

r = Buy.objects.all()
r.delete()

