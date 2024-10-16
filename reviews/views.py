from rest_framework import viewsets, filters, status
from .models import MovieReview, Like
from .serializers import ReviewSerializer
from .permissions import IsReviewOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend

class MovieReviewPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 100

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = MovieReview.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsReviewOwnerOrReadOnly]
    pagination_class = MovieReviewPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['title', 'rating']
    ordering_fields = ['created', 'rating']
    ordering = ['created']


    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def by_movie(self, request):
        movie_title = request.query_params.get('title')
        if not movie_title:
            return Response({"detail": "Movie title parameter is required."}, status=400)
        
        # Filter reviews by the provided movie title
        reviews = MovieReview.objects.filter(title__icontains=movie_title)
        
        # Apply pagination
        page = self.paginate_queryset(reviews)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        # If no pagination is needed, just return the reviews
        serializer = self.get_serializer(reviews, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post','delete'], permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        review = self.get_object()
        user = request.user

        if request.method == 'POST':
            like, created = Like.objects.get_or_create(user=user, review=review)
            if created:
                return Response({"message": "Review liked"}, status=status.HTTP_201_CREATED)
            return Response({"message": "Review already liked"}, status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'Delete':
            Like.objects.filter(user=user, review=review).delete()
            return Response({"mesage": "Like removed"}, status=status.HTTP_204_NO_CONTENT)