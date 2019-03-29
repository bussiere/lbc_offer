from django.db import models
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
    adresse_uuid = models.CharField(blank=True, null=True, max_length=48)
    geoHash = models.CharField(blank=True, null=True, max_length=200)
    gpsLat = models.DecimalField(blank=True, null=True, max_digits=9, decimal_places=6)
    gpsLong = models.DecimalField(blank=True, null=True, max_digits=9, decimal_places=6)
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
        if not self.uuid :
            self.uuid = str(uuid.uuid4().hex) +str(random.randint(1000,9999) )
        if not self.geoHash and (self.gpsLat and self.gpsLong):
            try :
                data = {"Lat":self.gpsLat,"Long":self.gpsLong}
                r = requests.post("http://127.0.0.1:8080/EncodeGeoHash/",json=data)
                r = r.json()
                self.geoHash = r["GeoHash"]
            except Exception as e:
                print(e)
                pass
        return super(Seller, self).save(*args, **kwargs)

class Norme(models.Model):
    nameP = (("b", "Big"), ("s", "Small"))
    name = models.CharField(max_length=1, choices=nameP, blank=True, null=True)
    valeur = models.CharField(max_length=100, choices=nameP, blank=True, null=True)
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
        if not self.uuid :
            self.uuid = str(uuid.uuid4().hex) +str(random.randint(1000,9999) )
        if not self.geoHash and (self.gpsLat and self.gpsLong):
            try :
                data = {"Lat":self.gpsLat,"Long":self.gpsLong}
                r = requests.post("http://127.0.0.1:8080/EncodeGeoHash/",json=data)
                r = r.json()
                self.geoHash = r["GeoHash"]
            except Exception as e:
                print(e)
                pass
        return super(Norme, self).save(*args, **kwargs)

class Equipement(models.Model):
    nameP = (("b", "Big"), ("s", "Small"))
    name = models.CharField(max_length=1, choices=nameP, blank=True, null=True)
    valeur = models.CharField(max_length=100, choices=nameP, blank=True, null=True)
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
        if not self.uuid :
            self.uuid = str(uuid.uuid4().hex) +str(random.randint(1000,9999))
        return super(Equipement, self).save(*args, **kwargs)

class Pic(models.Model):
    nameP = (("b", "Big"), ("s", "Small"))
    valeur = models.CharField(max_length=300, choices=nameP, blank=True, null=True)
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
        if not self.uuid :
            self.uuid = str(uuid.uuid4().hex) +str(random.randint(1000,9999) )
        return super(Pic, self).save(*args, **kwargs)

# Create your models here.
class Rent(models.Model):
    Cat_One = (("p", "Police"), ("g", "Gendarmerie"))
    Cat_Two = (("b", "Big"), ("s", "Small"))
    catOne = models.CharField(max_length=1, choices=Cat_One, blank=True, null=True)
    catTwo = models.CharField(max_length=1, choices=Cat_Two, blank=True, null=True)
    created = models.DateTimeField(null=True, blank=True, editable=False)
    modified = models.DateTimeField(null=True, blank=True)
    dateAd = models.DateTimeField(null=True, blank=True)
    name = models.CharField(blank=True, null=True, max_length=200)
    geoHash = models.CharField(blank=True, null=True, max_length=200)
    gpsLat = models.DecimalField(blank=True, null=True, max_digits=9, decimal_places=6)
    gpsLong = models.DecimalField(blank=True, null=True, max_digits=9, decimal_places=6)
    m2 = models.IntegerField(blank=True, null=True)
    m2_1 = models.IntegerField(blank=True, null=True)
    adresse_uuid = models.CharField(blank=True, null=True, max_length=48)
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
    origin = models.CharField(max_length=64, blank=True, null=True)
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
        if not self.uuid :
            self.uuid = str(uuid.uuid4().hex) +str(random.randint(1000,9999) )
        if not self.geoHash and (self.gpsLat and self.gpsLong):
            try :
                data = {"Lat":self.gpsLat,"Long":self.gpsLong}
                r = requests.post("http://127.0.0.1:8080/EncodeGeoHash/",json=data)
                r = r.json()
                self.geoHash = r["GeoHash"]
            except Exception as e:
                print(e)
                pass
        return super(Rent, self).save(*args, **kwargs)


class Buy(models.Model):
    Cat_One = (("p", "Police"), ("g", "Gendarmerie"))
    Cat_Two = (("b", "Big"), ("s", "Small"))
    catOne = models.CharField(max_length=1, choices=Cat_One, blank=True, null=True)
    catTwo = models.CharField(max_length=1, choices=Cat_Two, blank=True, null=True)
    created = models.DateTimeField(null=True, blank=True, editable=False)
    modified = models.DateTimeField(null=True, blank=True)
    dateAd = models.DateTimeField(null=True, blank=True)
    name = models.CharField(blank=True, null=True, max_length=200)
    geoHash = models.CharField(blank=True, null=True, max_length=200)
    gpsLat = models.DecimalField(blank=True, null=True, max_digits=9, decimal_places=6)
    gpsLong = models.DecimalField(blank=True, null=True, max_digits=9, decimal_places=6)
    m2 = models.IntegerField(blank=True, null=True)
    m2_1 = models.IntegerField(blank=True, null=True)
    adresse_uuid = models.CharField(blank=True, null=True, max_length=48)
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
    origin = models.CharField(max_length=64, blank=True, null=True)
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
        if not self.uuid :
            self.uuid = str(uuid.uuid4().hex) +str(random.randint(1000,9999) )
        if not self.geoHash and (self.gpsLat and self.gpsLong):
            try :
                data = {"Lat":self.gpsLat,"Long":self.gpsLong}
                r = requests.post("http://127.0.0.1:8080/EncodeGeoHash/",json=data)
                r = r.json()
                self.geoHash = r["GeoHash"]
            except Exception as e:
                print(e)
                pass
        return super(Buy, self).save(*args, **kwargs)


class BuyPlan(models.Model):
    Cat_One = (("p", "Police"), ("g", "Gendarmerie"))
    Cat_Two = (("b", "Big"), ("s", "Small"))
    catOne = models.CharField(max_length=1, choices=Cat_One, blank=True, null=True)
    catTwo = models.CharField(max_length=1, choices=Cat_Two, blank=True, null=True)
    created = models.DateTimeField(null=True, blank=True, editable=False)
    modified = models.DateTimeField(null=True, blank=True)
    dateAd = models.DateTimeField(null=True, blank=True)
    name = models.CharField(blank=True, null=True, max_length=200)
    geoHash = models.CharField(blank=True, null=True, max_length=200)
    gpsLat = models.DecimalField(blank=True, null=True, max_digits=9, decimal_places=6)
    gpsLong = models.DecimalField(blank=True, null=True, max_digits=9, decimal_places=6)
    m2 = models.IntegerField(blank=True, null=True)
    m2_1 = models.IntegerField(blank=True, null=True)
    adresse_uuid = models.CharField(blank=True, null=True, max_length=48)
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
    origin = models.CharField(max_length=64, blank=True, null=True)
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
        if not self.uuid :
            self.uuid = str(uuid.uuid4().hex) +str(random.randint(1000,9999) )
        if not self.geoHash and (self.gpsLat and self.gpsLong):
            try :
                data = {"Lat":self.gpsLat,"Long":self.gpsLong}
                r = requests.post("http://127.0.0.1:8080/EncodeGeoHash/",json=data)
                r = r.json()
                self.geoHash = r["GeoHash"]
            except Exception as e:
                print(e)
                pass
        return super(BuyPlan, self).save(*args, **kwargs)
