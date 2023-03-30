from django.urls import path

from server.views import LoginAccount, RegisterAccount, AccountDetails, PartnerUpdate, ShopView, ProductInfoView,\
    OrderView

urlpatterns = [
    path('user/register/', RegisterAccount.as_view(), name='user-register'),
    path('user/login/', LoginAccount.as_view(), name='user-login'),
    path('user/details/', AccountDetails.as_view(), name='user-details'),
    path('partner/update/', PartnerUpdate.as_view(), name='partner-update'),
    path('user/shop/', ShopView.as_view(), name='user-shop'),
    path('user/info/', ProductInfoView.as_view(), name='user-info'),
    path('user/order/', OrderView.as_view(), name='user-basket'),

]
