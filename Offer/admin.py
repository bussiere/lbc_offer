from django.contrib import admin

# Register your models here.
from Engine.actions import export_as_csv_action
from .models import BuyPlan

# Register your models here.


class BuyPlan_Admin(admin.ModelAdmin):
    actions = [
        export_as_csv_action(
            "CSV Export",
            fields=["commune","population", "created", "modified"],
        )
    ]

admin.site.register(BuyPlan, BuyPlan_Admin)