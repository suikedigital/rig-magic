from django.contrib import admin
from .models import BaseYacht, RigType, Mast, Boom

# Inline for Boom (related to Mast)
class BoomInline(admin.StackedInline):
    model = Boom
    extra = 1
    show_change_link = True

# Inline for Mast
class MastInline(admin.StackedInline):
    model = Mast
    extra = 1
    show_change_link = True

# Admin for BaseYacht (includes Masts)
@admin.register(BaseYacht)
class BaseYachtAdmin(admin.ModelAdmin):
    list_display = ('builder', 'model_name', 'model_number', 'variant', 'rig_type')
    inlines = [MastInline, BoomInline]  # Add Mast inline to BaseYacht

# Admin for RigType
@admin.register(RigType)
class RigTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)

# Admin for Mast (includes Boom)
@admin.register(Mast)
class MastAdmin(admin.ModelAdmin):
    list_display = ('base_yacht', 'position', 'mast_height', 'material')
    

# Admin for Boom
@admin.register(Boom)
class BoomAdmin(admin.ModelAdmin):
    list_display = ('base_yacht', 'position', 'length', 'boom_type', 'material')