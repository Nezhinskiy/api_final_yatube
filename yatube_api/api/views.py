from api.pagination import CustomPagination
from api.permissions import IsAuthorOrReadOnly
from api.serializers import CommentSerializer, GroupSerializer, PostSerializer
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from posts.models import Comment, Group, Post
from rest_framework import filters, permissions, viewsets
from rest_framework.throttling import AnonRateThrottle
from rest_framework.pagination import LimitOffsetPagination


class CustomViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsAuthorOrReadOnly)
    throttle_classes = (AnonRateThrottle,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,
                       filters.OrderingFilter)
    pagination_class = LimitOffsetPagination
    filterset_fields = ('author', 'group', 'pub_date')
    search_fields = ('text',)
    ordering_fields = '__all__'

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostViewSet(CustomViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class CommentViewSet(CustomViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, pk=post_id)
        new_queryset = post.comments.all()
        return new_queryset


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
