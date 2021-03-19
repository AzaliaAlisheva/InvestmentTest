from django.contrib import admin
from .models import Stock, PriceLookupEvent

admin.site.register(PriceLookupEvent)


class PriceLookupEventAdmin(admin.TabularInline):
    model = PriceLookupEvent
    extra = 0


class CompanyAdmin(admin.ModelAdmin):
    readonly_fields = ['periodic_task']

    class Meta:
        model = Stock


admin.site.register(Stock, CompanyAdmin)