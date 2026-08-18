from django.contrib import admin

from solich_views.models import ActiveGroup, ActiveTab, SavedFilter, ToggleColumn

admin.site.register([ToggleColumn, ActiveTab, ActiveGroup])
