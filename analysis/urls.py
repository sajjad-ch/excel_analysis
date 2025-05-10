from django.contrib import admin
from django.urls import path
from .views import UploadFileView, DataSummaryView, PlotingView, HomeView, AiReportView, DecisionView, FilesView

urlpatterns = [
    path('', HomeView.as_view(), name='Home'),
    path('uploadFile/', UploadFileView.as_view(), name='UploadFile'),
    path('DataSummary/<str:file>/', DataSummaryView.as_view(), name='DataSummary'),
    path('plot/', PlotingView.as_view(), name='Plot'),
    path('ai_report/<str:file>/', AiReportView.as_view(), name='AiReport'),
    path('decision/', DecisionView.as_view(), name='decision'),
    path('files/', FilesView.as_view(), name='files'),
]
