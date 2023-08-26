from django.urls import path
from .views import *

urlpatterns = [
    path('drug_movement/<slug:slug>', DrugMovementDetailView.as_view(), name='drug-movement'),
    path('drug_movements/', DrugMovementListView.as_view(), name='drug-movements'),
    path('drug_order/', DrugOrderView.as_view(), name='drug-order'),
    path('create_drug_receipt/', CreateDrugReceiptView.as_view(), name='create-drug-receipt')

]