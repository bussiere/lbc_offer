from django.contrib import admin
from .models import Token
from Engine.actions import export_as_csv_action

# Register your models here.
class Token_Admin(admin.ModelAdmin):
    list_display = ("value", "get_userId")
    search_fields = ("value", "user_id")
    actions = [export_as_csv_action("CSV Export", fields=["name", "get_userId"])]

    def get_userId(self, obj):
        return obj.user

    get_userId.admin_order_field = "user__id"


admin.site.register(Token, Token_Admin)
