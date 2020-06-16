# from rest_framework.response import Response
# from rest_framework.views import APIView
from rest_framework import generics, permissions
from django.db import models
from django_filters.rest_framework import DjangoFilterBackend

from .models import Movies, Actor
from .service import get_client_ip, MoviesFilter
from .serializers import MoviesSerializer, MoviesDetailSerializer, ReviewCreateSerializer, CreateRatingSerializer, ActorSerializer, ActorDetailSerializer


class MoviesListView(generics.ListAPIView):
    """list view"""
    serializer_class = MoviesSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = MoviesFilter
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset =  Movies.objects.filter(draft=False).annotate(
        rating_user=models.Count('ratings', filter=models.Q(ratings__ip=get_client_ip(self.request)))).annotate(middle_star=models.Sum(models.F('ratings__star')) / models.Count(models.F('ratings')))
        return queryset


# class MoviesListView(APIView):
#     """List view"""
#     def get(self, request):
#         movies = Movies.objects.filter(draft=False).annotate(
#         rating_user=models.Count('ratings', filter=models.Q(ratings__ip=get_client_ip(request)))).annotate(middle_star=models.Sum(models.F('ratings__star')) / models.Count(models.F('ratings')))
#         serializer = MoviesSerializer(movies, many=True)
#         return Response(serializer.data)


class MoviesDetailView(generics.RetrieveAPIView):
    """detail view"""
    queryset = Movies.objects.filter(draft=False)
    serializer_class = MoviesDetailSerializer




# class MoviesDetailView(APIView):
#     """detail view"""
#     def get(self, request, pk):
#         movies = Movies.objects.get(pk=pk, draft=False)
#         serializer = MoviesDetailSerializer(movies)
#         return Response(serializer.data)


class ReviewCreateView(generics.CreateAPIView):
    """review create"""
    serializer_class = ReviewCreateSerializer


# class ReviewCreateView(APIView):
#     """review create"""
#     def post(self, request):
#         review = ReviewCreateSerializer(data=request.data)
#         if review.is_valid():
#             review.save()
#         return Response(status=201)


class AddStarRatingView(generics.CreateAPIView):
    """add star"""
    serializer_class = CreateRatingSerializer

    def perform_create(self, serializer):
        serializer.save(ip=get_client_ip(self.request))


# class AddStarRatingView(APIView):
#     """add star"""
#
#     def post(self, request):
#         serializer = CreateRatingSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(ip=get_client_ip(request))
#             return Response(status=201)
#         else:
#             return Response(status=400)


class ActorListView(generics.ListAPIView):
    """view actor's list"""
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer


class ActorDetailView(generics.RetrieveAPIView):
    """view actor's detail"""
    queryset = Actor.objects.all()
    serializer_class = ActorDetailSerializer
