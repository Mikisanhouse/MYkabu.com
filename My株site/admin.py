from django.contrib import admin
from .models import Favorite_Code, Company_Code, BoardModel, ImageModel
# Register your models here.

admin.site.register(Favorite_Code)
admin.site.register(Company_Code)
admin.site.register(BoardModel)
admin.site.register(ImageModel)
