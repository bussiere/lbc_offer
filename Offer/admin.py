# Register your models here.
from django.contrib import admin

from Engine.actions import export_as_csv_action
from simple_history.admin import SimpleHistoryAdmin
from django import forms
from .models import Seller,Norme,Equipement,Pic,Rent,Buy,BuyPlan



class RentForm(forms.ModelForm):
    station = forms.ModelMultipleChoiceField(queryset=Seller.objects.order_by('name'))

    class Meta:
        model = Rent
        fields = '__all__'


class seller_admin(SimpleHistoryAdmin):
    list_display = ("name","contact","phone","email")
    search_fields = ("name","contact","phone","email")
    actions = [export_as_csv_action("CSV Export", fields=["name","contact","phone","email"])]



class Rent_Admin(SimpleHistoryAdmin):
    list_display = ("station","line","neighbour","timeTravelS","dateOpen","uuid","modified")
    search_fields = ("station","line","neighbour","timeTravelS","dateOpen","uuid","modified")
    actions = [export_as_csv_action("CSV Export", fields=["station","line","neighbour","timeTravelS","dateOpen","uuid","modified"])]
    form =  RentForm


class Seller_Admin(SimpleHistoryAdmin):
    list_display = ("name","modified")
    search_fields = ("name","modified")
    actions = [export_as_csv_action("CSV Export", fields=["name","modified"])]


admin.site.register(Seller, seller_admin)
#admin.site.register(StationLinkT, StationLinkT_Admin)
