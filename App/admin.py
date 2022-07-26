from django.contrib import admin

from App.models import searchResultDb, searchperdayDb, timeDb

# Register your models here.
admin.site.register(searchResultDb)
admin.site.register(timeDb)
admin.site.register(searchperdayDb)