from django.urls import path
from .views import *

urlpatterns = [
    path('choices/<int:pk>/', AddonChoiceAPIView.as_view(), name='addon-choice-detail'),
    path('orders/', SubmitOrderAPIView.as_view(), name='submit-order'),
    path('rules/', RulesAPIView.as_view(), name='rules'),
    path('addons/', AddonsAPIView.as_view(), name='addons'),
    path('sample-email/', SendSampleEmailView.as_view(), name='send-sample-email'),
]
