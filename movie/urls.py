from django.urls import path

from . import views

app_name = 'movie'
urlpatterns = [
    path('movie/', views.MoviesListView.as_view()),
    path('movie/<int:pk>/', views.MoviesDetailView.as_view() ),
    path('review/', views.ReviewCreateView.as_view()),
    path('rating/', views.AddStarRatingView.as_view()),
    path('actors/', views.ActorListView.as_view()),
    path('actors/<int:pk>/', views.ActorDetailView.as_view()),
]
