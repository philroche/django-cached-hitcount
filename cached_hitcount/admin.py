from django.contrib import admin

from cached_hitcount.models import Hit,BlacklistIP

class HitAdmin(admin.ModelAdmin):
    list_display = ('__unicode__','hits','added')
    fields = ('hits',)


class BlacklistIPAdmin(admin.ModelAdmin):
    pass

admin.site.register(Hit, HitAdmin)

admin.site.register(BlacklistIP, BlacklistIPAdmin)

