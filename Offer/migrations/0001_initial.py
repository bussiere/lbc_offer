# Generated by Django 2.2.2 on 2019-06-09 11:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(blank=True, editable=False, null=True)),
                ('modified', models.DateTimeField(blank=True, null=True)),
                ('value', models.CharField(blank=True, max_length=255, null=True)),
                ('uuid', models.CharField(blank=True, max_length=48, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='EquipmentName',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(blank=True, editable=False, null=True)),
                ('modified', models.DateTimeField(blank=True, null=True)),
                ('name', models.CharField(blank=True, max_length=256, null=True)),
                ('uuid', models.CharField(blank=True, max_length=48, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='GroupSeller',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(blank=True, editable=False, null=True)),
                ('modified', models.DateTimeField(blank=True, null=True)),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('uuid', models.CharField(blank=True, max_length=48, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Norm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(blank=True, editable=False, null=True)),
                ('modified', models.DateTimeField(blank=True, null=True)),
                ('value', models.CharField(blank=True, max_length=256, null=True)),
                ('uuid', models.CharField(blank=True, max_length=48, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='NormName',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(blank=True, editable=False, null=True)),
                ('modified', models.DateTimeField(blank=True, null=True)),
                ('name', models.CharField(blank=True, max_length=256, null=True)),
                ('uuid', models.CharField(blank=True, max_length=48, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Pic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(blank=True, editable=False, null=True)),
                ('modified', models.DateTimeField(blank=True, null=True)),
                ('value', models.TextField(blank=True, choices=[('b', 'Big'), ('s', 'Small')], null=True)),
                ('name', models.CharField(blank=True, max_length=300, null=True)),
                ('type', models.CharField(blank=True, choices=[('b', 'Big'), ('s', 'Small')], max_length=300, null=True)),
                ('uuid', models.CharField(blank=True, max_length=48, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Seller',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(blank=True, editable=False, null=True)),
                ('modified', models.DateTimeField(blank=True, null=True)),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('url', models.CharField(blank=True, max_length=200, null=True)),
                ('contact', models.CharField(blank=True, max_length=200, null=True)),
                ('phone', models.CharField(blank=True, max_length=200, null=True)),
                ('email', models.CharField(blank=True, max_length=200, null=True)),
                ('note', models.CharField(blank=True, max_length=200, null=True)),
                ('adresse_uuid', models.CharField(blank=True, max_length=48, null=True)),
                ('geohash', models.CharField(blank=True, max_length=200, null=True)),
                ('gps_lat', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ('gps_long', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ('uuid', models.CharField(blank=True, max_length=48, null=True)),
                ('group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='Group_Seller', to='Offer.GroupSeller')),
            ],
        ),
        migrations.CreateModel(
            name='Rent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cat_one', models.CharField(blank=True, choices=[('p', 'Police'), ('g', 'Gendarmerie')], max_length=1, null=True)),
                ('cat_two', models.CharField(blank=True, choices=[('b', 'Big'), ('s', 'Small')], max_length=1, null=True)),
                ('created', models.DateTimeField(blank=True, editable=False, null=True)),
                ('modified', models.DateTimeField(blank=True, null=True)),
                ('date_ad', models.DateTimeField(blank=True, null=True)),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('geohash', models.CharField(blank=True, max_length=200, null=True)),
                ('gps_lat', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ('gps_long', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ('m2', models.IntegerField(blank=True, null=True)),
                ('m2_1', models.IntegerField(blank=True, null=True)),
                ('adresse_uuid', models.CharField(blank=True, max_length=48, null=True)),
                ('url_offer', models.CharField(blank=True, max_length=500, null=True)),
                ('note', models.CharField(blank=True, max_length=200, null=True)),
                ('description', models.CharField(blank=True, max_length=300, null=True)),
                ('piece', models.IntegerField(blank=True, null=True)),
                ('chambre', models.IntegerField(blank=True, null=True)),
                ('price', models.FloatField(blank=True, null=True)),
                ('available', models.BooleanField(default=False)),
                ('ref1', models.CharField(blank=True, max_length=200, null=True)),
                ('ref2', models.CharField(blank=True, max_length=200, null=True)),
                ('score', models.IntegerField(blank=True, null=True)),
                ('origin', models.CharField(blank=True, max_length=64, null=True)),
                ('uuid', models.CharField(blank=True, max_length=48, null=True)),
                ('equipment', models.ManyToManyField(blank=True, related_name='EquipRent', to='Offer.Equipment')),
                ('norm', models.ManyToManyField(blank=True, related_name='NormeRent', to='Offer.Norm')),
                ('pic', models.ManyToManyField(blank=True, related_name='PicRent', to='Offer.Pic')),
                ('seller', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, related_name='SellerRent', to='Offer.Seller')),
            ],
        ),
        migrations.AddField(
            model_name='norm',
            name='name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='SellerRent', to='Offer.NormName'),
        ),
        migrations.AddField(
            model_name='equipment',
            name='name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='SellerRent', to='Offer.EquipmentName'),
        ),
        migrations.CreateModel(
            name='BuyPlan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('catOne', models.CharField(blank=True, choices=[('p', 'Police'), ('g', 'Gendarmerie')], max_length=1, null=True)),
                ('catTwo', models.CharField(blank=True, choices=[('b', 'Big'), ('s', 'Small')], max_length=1, null=True)),
                ('created', models.DateTimeField(blank=True, editable=False, null=True)),
                ('modified', models.DateTimeField(blank=True, null=True)),
                ('dateAd', models.DateTimeField(blank=True, null=True)),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('geoHash', models.CharField(blank=True, max_length=200, null=True)),
                ('gpsLat', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ('gpsLong', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ('commune', models.CharField(blank=True, max_length=120, null=True)),
                ('postal_code', models.CharField(blank=True, max_length=10, null=True)),
                ('m2', models.IntegerField(blank=True, null=True)),
                ('m2_1', models.IntegerField(blank=True, null=True)),
                ('adresse_uuid', models.CharField(blank=True, max_length=48, null=True)),
                ('urlOffer', models.CharField(blank=True, max_length=500, null=True)),
                ('note', models.CharField(blank=True, max_length=200, null=True)),
                ('description', models.CharField(blank=True, max_length=300, null=True)),
                ('piece', models.IntegerField(blank=True, null=True)),
                ('chambre', models.IntegerField(blank=True, null=True)),
                ('available', models.BooleanField(default=False)),
                ('price', models.FloatField(blank=True, null=True)),
                ('ref1', models.CharField(blank=True, max_length=200, null=True)),
                ('ref2', models.CharField(blank=True, max_length=200, null=True)),
                ('score', models.IntegerField(blank=True, null=True)),
                ('origin', models.CharField(blank=True, max_length=64, null=True)),
                ('uuid', models.CharField(blank=True, max_length=48, null=True)),
                ('equipment', models.ManyToManyField(blank=True, related_name='EquipBuyPlan', to='Offer.Equipment')),
                ('norm', models.ManyToManyField(blank=True, related_name='NormeBuyPlan', to='Offer.Norm')),
                ('pic', models.ManyToManyField(blank=True, related_name='PicBuyPlan', to='Offer.Pic')),
                ('seller', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, related_name='SellerBuyPlan', to='Offer.Seller')),
            ],
        ),
        migrations.CreateModel(
            name='Buy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cat_one', models.CharField(blank=True, max_length=30, null=True)),
                ('cat_two', models.CharField(blank=True, max_length=30, null=True)),
                ('created', models.DateTimeField(blank=True, editable=False, null=True)),
                ('modified', models.DateTimeField(blank=True, null=True)),
                ('ad_id', models.IntegerField(blank=True, null=True)),
                ('commune', models.CharField(blank=True, max_length=180, null=True)),
                ('postal_code', models.CharField(blank=True, max_length=8, null=True)),
                ('date_ad', models.DateTimeField(blank=True, null=True)),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('geohash', models.CharField(blank=True, max_length=200, null=True)),
                ('gps_lat', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ('gps_long', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ('m2', models.IntegerField(blank=True, null=True)),
                ('m2_1', models.IntegerField(blank=True, null=True)),
                ('adresse_uuid', models.CharField(blank=True, max_length=48, null=True)),
                ('url_offer', models.CharField(blank=True, max_length=500, null=True)),
                ('note', models.CharField(blank=True, max_length=200, null=True)),
                ('description', models.CharField(blank=True, max_length=800, null=True)),
                ('piece', models.IntegerField(blank=True, null=True)),
                ('chambre', models.IntegerField(blank=True, null=True)),
                ('pic1', models.CharField(blank=True, max_length=800, null=True)),
                ('available', models.BooleanField(default=False)),
                ('price', models.FloatField(blank=True, null=True)),
                ('ref1', models.CharField(blank=True, max_length=200, null=True)),
                ('ref2', models.CharField(blank=True, max_length=200, null=True)),
                ('score', models.IntegerField(blank=True, null=True)),
                ('origin', models.CharField(blank=True, max_length=64, null=True)),
                ('uuid', models.CharField(blank=True, max_length=48, null=True)),
                ('equipment', models.ManyToManyField(blank=True, related_name='EquipBuy', to='Offer.Equipment')),
                ('norm', models.ManyToManyField(blank=True, related_name='NormeBuy', to='Offer.Norm')),
                ('pic', models.ManyToManyField(blank=True, related_name='PicBuy', to='Offer.Pic')),
                ('seller', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, related_name='SellerBuy', to='Offer.Seller')),
            ],
        ),
    ]
