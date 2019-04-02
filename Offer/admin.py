# Register your models here.
from django.contrib import admin

from Engine.actions import export_as_csv_action
from simple_history.admin import SimpleHistoryAdmin
from django import forms
from .models import Seller,Norm,Equipment,Pic,Rent,Buy,BuyPlan



class Rent_Form(forms.ModelForm):
    station = forms.ModelMultipleChoiceField(queryset=Seller.objects.order_by('name'))

    class Meta:
        model = Rent
        fields = '__all__'


class Seller_Admin(SimpleHistoryAdmin):
    list_display = ("name","contact","phone","email")
    search_fields = ("name","contact","phone","email")
    actions = [export_as_csv_action("CSV Export", fields=["name","contact","phone","email"])]



class Norm_Admin(SimpleHistoryAdmin):
    list_display = ("name","value")
    search_fields = ("name","value")
    actions = [export_as_csv_action("CSV Export", fields=["name","value"])]
    #form =  RentForm





class Equipment_Admin(SimpleHistoryAdmin):
    list_display = ("name","value")
    search_fields = ("name","value")
    actions = [export_as_csv_action("CSV Export", fields=["name","value"])]

admin.site.register(Seller, Seller_Admin)
admin.site.register(Norm, Norm_Admin)
admin.site.register(Equipment, Equipment_Admin)
