from django.contrib import admin
from .models import *


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'phone_number',
                    'blood_group', 'location', 'user_type')
    search_fields = ('username', 'email', 'phone_number')
    list_filter = ('user_type', 'blood_group')


@admin.register(BloodRequest)
class BloodRequestAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'requested_blood_group',
                    'request_date', 'urgency', 'status', 'location')
    search_fields = ('recipient__username',
                     'requested_blood_group', 'location')
    list_filter = ('status', 'urgency', 'requested_blood_group')
    date_hierarchy = 'request_date'


@admin.register(BloodDonation)
class BloodDonationAdmin(admin.ModelAdmin):
    list_display = ('donor', 'recipient', 'date_of_donation',
                    'location', 'is_verified', 'blood_request')
    search_fields = ('donor__username', 'recipient__username', 'location')
    list_filter = ('is_verified', 'date_of_donation')
    date_hierarchy = 'date_of_donation'


@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ('name', 'threshold')
    search_fields = ('name',)
    list_filter = ('threshold',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'timestamp', 'read')
    search_fields = ('sender__username', 'receiver__username', 'content')
    list_filter = ('read',)
    date_hierarchy = 'timestamp'


@admin.register(BloodInventory)
class BloodInventoryAdmin(admin.ModelAdmin):
    list_display = ('blood_group', 'available_units',
                    'hospital_location', 'last_updated')
    search_fields = ('blood_group', 'hospital_location')
    list_filter = ('blood_group',)
    date_hierarchy = 'last_updated'


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'location')
    search_fields = ('title', 'location')
    date_hierarchy = 'date'
