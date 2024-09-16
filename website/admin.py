from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register((User, BloodInventory, BloodRequest,
                    BloodDonation, Message, Badge))

admin.site.register(Campaign)
