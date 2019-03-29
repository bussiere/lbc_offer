from django.db import models
from Geo.models import Adresse
from django.utils import timezone

class Seller(models.Model):
    created = models.DateTimeField(null=True, blank=True, editable=False)
    modified = models.DateTimeField(null=True, blank=True)
    name = models.CharField(blank=True, null=True, max_length=200)
    url = models.CharField(blank=True, null=True, max_length=200)
    contact = models.CharField(blank=True, null=True, max_length=200)
    phone = models.CharField(blank=True, null=True, max_length=200)
    email = models.CharField(blank=True, null=True, max_length=200)
    note = models.CharField(blank=True, null=True, max_length=200)
    adresse = models.ForeignKey(
        Adresse,
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        related_name="AdresseSeller",
    )
    uuid = models.CharField(blank=True, null=True, max_length=48)


    def toJson():
        result = {}
        result["created"] = self.created
        result["modified"] = self.modified
        result["name"] = self.name
        result["url"] = self.url
        result["contact"] = self.contact
        result["phone"] = self.phone
        result["email"] = self.email
        result["note"] = self.note
        result["adresse"] = self.adresse
        result["uuid"] = self.uuid
        return result

class Norme(models.Model):
    created = models.DateTimeField(null=True, blank=True, editable=False)
    modified = models.DateTimeField(null=True, blank=True)
    nameP = (("b", "Big"), ("s", "Small"))
    name = models.CharField(max_length=1, choices=nameP, blank=True, null=True)
    valeur = models.CharField(max_length=100, choices=nameP, blank=True, null=True)
    uuid = models.CharField(blank=True, null=True, max_length=48)


    def toJson():
        result = {}
        result["name"] = self.name
        result["valeur"] = self.valeur
        result["uuid"] = self.uuid
        return result

class Equipement(models.Model):
    created = models.DateTimeField(null=True, blank=True, editable=False)
    modified = models.DateTimeField(null=True, blank=True)
    nameP = (("b", "Big"), ("s", "Small"))
    name = models.CharField(max_length=1, choices=nameP, blank=True, null=True)
    valeur = models.CharField(max_length=100, choices=nameP, blank=True, null=True)
    uuid = models.CharField(blank=True, null=True, max_length=48)

    def toJson():
        result = {}
        result["name"] = self.name
        result["valeur"] = self.valeur
        result["uuid"] = self.uuid
        return result

class Pic(models.Model):
    created = models.DateTimeField(null=True, blank=True, editable=False)
    modified = models.DateTimeField(null=True, blank=True)
    nameP = (("b", "Big"), ("s", "Small"))
    valeur = models.CharField(max_length=300, choices=nameP, blank=True, null=True)
    uuid = models.CharField(blank=True, null=True, max_length=48)

# Create your models here.


    def toJson():
        result = {}
        result["valeur"] = self.valeur
        result["uuid"] = self.uuid
        return result

class Rent(models.Model):
    Cat_One = (("p", "Police"), ("g", "Gendarmerie"))
    Cat_Two = (("b", "Big"), ("s", "Small"))
    catOne = models.CharField(max_length=1, choices=Cat_One, blank=True, null=True)
    catTwo = models.CharField(max_length=1, choices=Cat_Two, blank=True, null=True)
    created = models.DateTimeField(null=True, blank=True, editable=False)
    modified = models.DateTimeField(null=True, blank=True)
    name = models.CharField(blank=True, null=True, max_length=200)
    geoHash = models.CharField(blank=True, null=True, max_length=200)
    m2 = models.IntegerField(blank=True, null=True)
    m2_1 = models.IntegerField(blank=True, null=True)
    adresse = models.ForeignKey(
        Adresse, blank=True, on_delete=models.PROTECT, related_name="AdresseRent"
    )
    seller = models.ForeignKey(
        Seller, blank=True, on_delete=models.PROTECT, related_name="SellerRent"
    )
    urlOffer = models.CharField(blank=True, null=True, max_length=500)
    note = models.CharField(blank=True, null=True, max_length=200)
    description = models.CharField(blank=True, null=True, max_length=300)
    piece = models.IntegerField(blank=True, null=True)
    chambre = models.IntegerField(blank=True, null=True)
    norme = models.ManyToManyField(Norme, blank=True, related_name="NormeRent")
    equipement = models.ManyToManyField(
        Equipement, blank=True, related_name="EquipRent"
    )
    pic = models.ManyToManyField(Pic, blank=True, related_name="PicRent")
    price = models.FloatField(blank=True, null=True)
    available = models.BooleanField(default=False)
    ref1 = models.CharField(blank=True, null=True, max_length=200)
    ref2 = models.CharField(blank=True, null=True, max_length=200)
    score = models.IntegerField(blank=True, null=True)
    uuid = models.CharField(blank=True, null=True, max_length=48)
    
    def __str__(self):
        return self.name + ":" + str(self.id) + ":" + self.adresse

    def __unicode__(self):
        return self.name + ":" + str(self.id)

    def save(self, *args, **kwargs):
        """ On save, update timestamps """
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        if not self.geoHash:
            if self.adresse.geoHash:
                self.geoHash = self.adresse.geoHash
        return super(Rent, self).save(*args, **kwargs)


    def toJson():
        result = {}
        result["catOne"] = self.catOne
        result["catTwo"] = self.catTwo
        result["created"] = self.created
        result["modified"] = self.modified
        result["name"] = self.name
        result["geoHash"] = self.geoHash
        result["m2"] = self.m2
        result["m2_1"] = self.m2_1
        result["adresse"] = self.adresse
        result["seller"] = self.seller
        result["urlOffer"] = self.urlOffer
        result["note"] = self.note
        result["description"] = self.description
        result["piece"] = self.piece
        result["chambre"] = self.chambre
        result["norme"] = self.norme
        result["equipement"] = self.equipement
        result["pic"] = self.pic
        result["price"] = self.price
        result["available"] = self.available
        result["ref1"] = self.ref1
        result["ref2"] = self.ref2
        result["score"] = self.score
        result["uuid"] = self.uuid
        return result

class Buy(models.Model):
    Cat_One = (("p", "Police"), ("g", "Gendarmerie"))
    Cat_Two = (("b", "Big"), ("s", "Small"))
    catOne = models.CharField(max_length=1, choices=Cat_One, blank=True, null=True)
    catTwo = models.CharField(max_length=1, choices=Cat_Two, blank=True, null=True)
    created = models.DateTimeField(null=True, blank=True, editable=False)
    modified = models.DateTimeField(null=True, blank=True)
    name = models.CharField(blank=True, null=True, max_length=200)
    geoHash = models.CharField(blank=True, null=True, max_length=200)
    m2 = models.IntegerField(blank=True, null=True)
    m2_1 = models.IntegerField(blank=True, null=True)
    adresse = models.ForeignKey(
        Adresse, blank=True, on_delete=models.PROTECT, related_name="AdresseBuy"
    )
    seller = models.ForeignKey(
        Seller, blank=True, on_delete=models.PROTECT, related_name="SellerBuy"
    )
    urlOffer = models.CharField(blank=True, null=True, max_length=500)
    note = models.CharField(blank=True, null=True, max_length=200)
    description = models.CharField(blank=True, null=True, max_length=300)
    piece = models.IntegerField(blank=True, null=True)
    chambre = models.IntegerField(blank=True, null=True)
    norme = models.ManyToManyField(Norme, blank=True, related_name="NormeBuy")
    equipement = models.ManyToManyField(Equipement, blank=True, related_name="EquipBuy")
    pic = models.ManyToManyField(Pic, blank=True, related_name="PicBuy")
    available = models.BooleanField(default=False)
    price = models.FloatField(blank=True, null=True)
    ref1 = models.CharField(blank=True, null=True, max_length=200)
    ref2 = models.CharField(blank=True, null=True, max_length=200)
    score = models.IntegerField(blank=True, null=True)
    uuid = models.CharField(blank=True, null=True, max_length=48)
    def __str__(self):
        return self.name + ":" + str(self.id) + ":" + self.codePostal

    def __unicode__(self):
        return self.name + ":" + str(self.id)

    def save(self, *args, **kwargs):
        """ On save, update timestamps """
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        if not self.geoHash:
            if self.adresse.geoHash:
                self.geoHash = self.adresse.geoHash
        return super(Buy, self).save(*args, **kwargs)


    def toJson():
        result = {}
        result["catOne"] = self.catOne
        result["catTwo"] = self.catTwo
        result["created"] = self.created
        result["modified"] = self.modified
        result["name"] = self.name
        result["geoHash"] = self.geoHash
        result["m2"] = self.m2
        result["m2_1"] = self.m2_1
        result["adresse"] = self.adresse
        result["seller"] = self.seller
        result["urlOffer"] = self.urlOffer
        result["note"] = self.note
        result["description"] = self.description
        result["piece"] = self.piece
        result["chambre"] = self.chambre
        result["norme"] = self.norme
        result["equipement"] = self.equipement
        result["pic"] = self.pic
        result["available"] = self.available
        result["price"] = self.price
        result["ref1"] = self.ref1
        result["ref2"] = self.ref2
        result["score"] = self.score
        result["uuid"] = self.uuid
        return result

class BuyPlan(models.Model):
    Cat_One = (("p", "Police"), ("g", "Gendarmerie"))
    Cat_Two = (("b", "Big"), ("s", "Small"))
    catOne = models.CharField(max_length=1, choices=Cat_One, blank=True, null=True)
    catTwo = models.CharField(max_length=1, choices=Cat_Two, blank=True, null=True)
    created = models.DateTimeField(null=True, blank=True, editable=False)
    modified = models.DateTimeField(null=True, blank=True)
    name = models.CharField(blank=True, null=True, max_length=200)
    geoHash = models.CharField(blank=True, null=True, max_length=200)
    m2 = models.IntegerField(blank=True, null=True)
    m2_1 = models.IntegerField(blank=True, null=True)
    adresse = models.ForeignKey(
        Adresse, blank=True, on_delete=models.PROTECT, related_name="AdresseBuyPlan"
    )
    seller = models.ForeignKey(
        Seller, blank=True, on_delete=models.PROTECT, related_name="SellerBuyPlan"
    )
    urlOffer = models.CharField(blank=True, null=True, max_length=500)
    note = models.CharField(blank=True, null=True, max_length=200)
    description = models.CharField(blank=True, null=True, max_length=300)
    piece = models.IntegerField(blank=True, null=True)
    chambre = models.IntegerField(blank=True, null=True)
    norme = models.ManyToManyField(Norme, blank=True, related_name="NormeBuyPlan")
    equipement = models.ManyToManyField(
        Equipement, blank=True, related_name="EquipBuyPlan"
    )
    pic = models.ManyToManyField(Pic, blank=True, related_name="PicBuyPlan")
    available = models.BooleanField(default=False)
    price = models.FloatField(blank=True, null=True)
    ref1 = models.CharField(blank=True, null=True, max_length=200)
    ref2 = models.CharField(blank=True, null=True, max_length=200)
    score = models.IntegerField(blank=True, null=True)
    uuid = models.CharField(blank=True, null=True, max_length=48)
    def __str__(self):
        return self.name + ":" + str(self.id) + ":" + self.codePostal

    def __unicode__(self):
        return self.name + ":" + str(self.id)

    def save(self, *args, **kwargs):
        """ On save, update timestamps """
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        if not self.geoHash:
            if self.adresse.geoHash:
                self.geoHash = self.adresse.geoHash
        return super(BuyPlan, self).save(*args, **kwargs)


    def toJson():
        result = {}
        result["catOne"] = self.catOne
        result["catTwo"] = self.catTwo
        result["created"] = self.created
        result["modified"] = self.modified
        result["name"] = self.name
        result["geoHash"] = self.geoHash
        result["m2"] = self.m2
        result["m2_1"] = self.m2_1
        result["adresse"] = self.adresse
        result["seller"] = self.seller
        result["urlOffer"] = self.urlOffer
        result["note"] = self.note
        result["description"] = self.description
        result["piece"] = self.piece
        result["chambre"] = self.chambre
        result["norme"] = self.norme
        result["equipement"] = self.equipement
        result["pic"] = self.pic
        result["available"] = self.available
        result["price"] = self.price
        result["ref1"] = self.ref1
        result["ref2"] = self.ref2
        result["score"] = self.score
        result["uuid"] = self.uuid
        return result