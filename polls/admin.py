from django.contrib import admin

from .models import Question
from .models import Party
from .models import Invitation

admin.site.register(Question)
admin.site.register(Party)
admin.site.register(Invitation)

# Register your models here.
