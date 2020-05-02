from django.urls import path

from . import views

urlpatterns = [
    path('', views.viewStatistics, name = 'statistics'),
    path('sendMonthlyReport/', views.sendMonthlyReport, name = 'send_monthly_report')
]