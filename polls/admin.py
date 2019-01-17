from django.contrib import admin

from .models import Party
from .models import Invitation

class InvitationInline(admin.TabularInline):
    model = Invitation
    fields = ('first_name', 'last_name', 'status')
    readonly_fields = ('first_name', 'last_name')

admin.site.register(Party)
admin.site.register(Invitation)

# Register your models here.
