# Register your models here.
from django.contrib import admin

from Engine.actions import export_as_csv_action
from simple_history.admin import SimpleHistoryAdmin
from django import forms
from .models import Seller,Norm,Equipment,Pic,Rent,Buy,BuyPlan,GroupSeller

#https://stackoverflow.com/questions/14597937/show-multiple-choices-to-admin-in-django


class Rent_Form(forms.ModelForm):
    seller = forms.ModelChoiceField(queryset=Seller.objects.order_by('name'))
    norm = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple,queryset=Norm.objects.order_by('name'),required=False)
    equipment = forms.ModelMultipleChoiceField(queryset=Equipment.objects.order_by('name'),required=False)
    pic = forms.ModelMultipleChoiceField(queryset=Pic.objects.order_by('name'),required=False)
    class Meta:
        model = Rent
        fields = '__all__'


class GroupSeller_Admin(SimpleHistoryAdmin):
    list_display = ("name","created")
    search_fields = ("name","created")
    actions = [export_as_csv_action("CSV Export", fields=["name","created"])]

class Seller_Admin(SimpleHistoryAdmin):
    list_display = ("name","created","contact","phone","email")
    search_fields = ("name","created","contact","phone","email")
    actions = [export_as_csv_action("CSV Export", fields=["name","created","contact","phone","email"])]



class Norm_Admin(SimpleHistoryAdmin):
    list_display = ("name","created","value")
    search_fields = ("name","created","value")
    actions = [export_as_csv_action("CSV Export", fields=["name","created","value"])]





class Equipment_Admin(SimpleHistoryAdmin):
    list_display = ("name","created","value")
    search_fields = ("name","created","value")
    actions = [export_as_csv_action("CSV Export", fields=["name","created","value"])]


class Pic_Admin(SimpleHistoryAdmin):
    list_display = ("name","created","type")
    search_fields = ("name","created","type")
    actions = [export_as_csv_action("CSV Export", fields=["name","created","type"])]



class Rent_Admin(SimpleHistoryAdmin):
    list_display = ("name","created","catOne","catTwo")
    search_fields = ("name","created","catOne","catTwo")
    actions = [export_as_csv_action("CSV Export", fields=["name","created","catOne","catTwo"])]
    form =  Rent_Form


admin.site.register(GroupSeller, GroupSeller_Admin)
admin.site.register(Seller, Seller_Admin)
admin.site.register(Norm, Norm_Admin)
admin.site.register(Equipment, Equipment_Admin)
admin.site.register(Pic, Pic_Admin)
admin.site.register(Rent, Rent_Admin)
