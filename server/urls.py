from django.urls import path

from server.views import LoginAccount, RegisterAccount, AccountDetails, PartnerUpdate

urlpatterns = [
    path('user/register/', RegisterAccount.as_view(), name='user-register'),
    path('user/login/', LoginAccount.as_view(), name='user-login'),
    path('user/details/', AccountDetails.as_view(), name='user-details'),
    path('partner/update/', PartnerUpdate.as_view(), name='partner-update'),

]
