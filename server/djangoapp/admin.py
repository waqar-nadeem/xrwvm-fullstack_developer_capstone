from django.contrib import admin
from .models import CarMake, CarModel

# CarMake Admin class to customize display
class CarMakeAdmin(admin.ModelAdmin):
    list_display = ('name', 'country_of_origin', 'description')
    search_fields = ['name']

# CarModel Admin class to customize display
class CarModelAdmin(admin.ModelAdmin):
    # Fields to display in the list view
    list_display = ('name', 'car_make', 'type', 'year', 'dealer_id')
    # Fields to filter the list by
    list_filter = ('car_make', 'type', 'year')
    # Fields to allow searching on
    search_fields = ['name', 'car_make__name'] 

# Register the models with their custom admin classes
admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)