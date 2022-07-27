from django.urls import path
from . import views


app_name = 'post'
urlpatterns = [
    path('<int:post_id>/<slug:post_slug>/', views.PostDetailView.as_view(), name='detail'),
    path('delete/<int:post_id>/', views.PostDeleteView.as_view(), name='delete'),
    path('update/<int:post_id>/', views.PostUpdateView.as_view(), name='update'),
    path('create/', views.PostCreateView.as_view(), name='create'),
]
