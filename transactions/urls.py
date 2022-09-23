from django.urls import path
from transactions import views as transactions_views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    #path('', transactions_views.index, name='home'),
    path('', transactions_views.index.as_view(), name='home'),
    path('api/transactions/', transactions_views.transaction_list),
    path('api/transactions/<int:pk>/', transactions_views.transaction_detail),
    path('api/transactions/published/',
         transactions_views.transaction_list_published)
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
