from django.urls import path
from . import views
from .views import HomePageView
from django.conf.urls import url

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('buy/', views.buy_list, name='buy_list'),
    path('rent/', views.rent_list, name='rent_list'),
    path('buy/search/',views.searchbuy, name='searchbuy'),
    path('rent/search/',views.searchrent, name='searchrent'),
    path('rent/sortascending/',views.sortrent, name='sortrent'),
    path('rent/sortdescending/',views.sortrentde, name='sortrentde'),
    path('buy/sortascending/',views.sortbuy, name='sortbuy'),
    path('buy/sortdescending/',views.sortbuyde, name='sortbuyde'),
    path('rent/filter/',views.rentfilter, name='rentfilter'),
    path('buy/filter/',views.buyfilter, name='buyfilter'),
    path('tenants/',views.tenant_list, name='tenant_list'),
    path('tenants/myaccount/',views.myaccount, name='myaccount'),
    path('tenants/details/maintenance/',views.maintenance, name='maintenance'),
    path('tenants/details/maintenance_error/',views.maintenance, name='nomaintenance'),
    path('tenant/details/payment/',views.payment, name='payment'),
    path('tenant/details/payment/failed/',views.paymentfailed, name='paymentfailed'),
    path('buy/<int:pk>/', views.buy_detail, name='buy_detail'),
    path('cosmo/book/',views.bookappointment,name='bookappointment'),
    path('cosmo/book/success/',views.success,name='success'),
    path('rent/<int:pk>/', views.rent_detail, name='rent_detail'),
    path('tenant/<int:pk>/', views.tenant_detail, name='tenant_detail'),
    path('post/new/', views.post_new, name='post_new'),
    

]
