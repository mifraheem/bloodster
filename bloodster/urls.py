
from django.contrib import admin
from django.urls import path
from website.controllers import basic_controller, user_controller, dashboards, bloodRequest, chat_controller
urlpatterns = [
    path('admin/', admin.site.urls),

    # basic urls
    path('', basic_controller.home, name="home"),



    # user urls
    path('register/', user_controller.register, name='register'),
    path('login/', user_controller.handle_login, name='login'),
    path('logout/', user_controller.handle_logout, name='logout'),
    path('update_profile/', user_controller.update_profile, name="update_profile"),

    # dashboard urls
    path('donor-dashboard/', dashboards.donor_dashboard, name='donor-dashboard'),
    path('recip-dashboard/', dashboards.recipt_dashboard,
         name='recipient-dashboard'),


    # Blood request urls
    path('blood-request/', bloodRequest.create_blood_request, name='blood-request'),
    path('cancel-request/<int:id>',
         bloodRequest.cancel_request, name='cancel-request'),
    path('view-request/<int:id>', bloodRequest.view_request, name='view-request'),
    path('accept-request/<int:request_id>/',
         bloodRequest.accept_blood_request, name='accept_blood_request'),
    path('fulfill-request/<int:request_id>',
         bloodRequest.fulfill_request, name="fulfill-request"),
    path('verify-donation/<int:id>',
         bloodRequest.confirm_donation_by_recipient, name='verify-donation'),
    path('reject-donation/<int:id>',
         bloodRequest.reject_donation_by_recipient, name='reject-donation'),



    # profile urls
    path('donor/<int:id>', dashboards.show_donor_profile, name='donor-profile'),


    # chat urls
    path('chat/', chat_controller.chat, name='chat'),
    path('chat/<str:chat_user>', chat_controller.chat, name='chat_user'),
    path('save_message/<str:chat_user>',
         chat_controller.save_message, name='save_message'),
    path('fetch_all_messages/<str:chat_user>/',
         chat_controller.fetch_all_messages, name='fetch_all_messages'),
]
