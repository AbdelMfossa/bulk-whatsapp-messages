from django.contrib import admin
from send.models import *
# Register your models here.

# @admin.register(Candidat)
class CandidatnAdmin(admin.ModelAdmin):
    list_display = ('telephone', 'nom', 'concours','date_envoi', 'go',)
    ordering = ('-nom',)
    list_filter = ('concours', 'go', 'status_code')
    search_fields = ('telephone', 'nom',)
    actions = ['make_no_go']

    # @admin.action(description='Marquer comme non envoyé(s)')
    def make_no_go(modeladmin, request, queryset):
        queryset.update(go=False)

admin.site.register(Candidat, CandidatnAdmin)
