# Register your models here.
from django.contrib import admin

from Engine.actions import export_as_csv_action
from simple_history.admin import SimpleHistoryAdmin
from django import forms
from .models import Seller,Norme,Equipement,Pic,Rent,Buy,BuyPlan



class LineTForm(forms.ModelForm):
    station = forms.ModelMultipleChoiceField(queryset=Station.objects.order_by('name'))

    class Meta:
        model = Line
        fields = '__all__'


class Station_Line_Admin(SimpleHistoryAdmin):
    list_display = ("station","line","uuid","modified")
    search_fields = ("station__name","line__name","uuid","modified")
    actions = [export_as_csv_action("CSV Export", fields=["station","line","uuid","modified"])]
    form =  Station_Line_Form


class StationLinkT_Admin(SimpleHistoryAdmin):
    list_display = ("station","line","neighbour","timeTravelS","dateOpen","uuid","modified")
    search_fields = ("station","line","neighbour","timeTravelS","dateOpen","uuid","modified")
    actions = [export_as_csv_action("CSV Export", fields=["station","line","neighbour","timeTravelS","dateOpen","uuid","modified"])]
    form =  Station_Line_Form


class Seller_Admin(SimpleHistoryAdmin):
    list_display = ("name","modified")
    search_fields = ("name","modified")
    actions = [export_as_csv_action("CSV Export", fields=["name","modified"])]


admin.site.register(Seller, Seller_Admin)
#admin.site.register(StationLinkT, StationLinkT_Admin)
