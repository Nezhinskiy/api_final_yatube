from api.pagination import CustomPagination
from api.permissions import IsAuthorOrReadOnly
from api.serializers import (CommentSerializer, FollowSerializer,
                             GroupSerializer, PostSerializer)
from django.shortcuts import get_object_or_404
from posts.models import Comment, Follow, Group, Post
from rest_framework import filters, permissions, viewsets
from rest_framework.throttling import AnonRateThrottle


class CustomViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsAuthorOrReadOnly)
    throttle_classes = (AnonRateThrottle,)
    filter_backends = (filters.SearchFilter,
                       filters.OrderingFilter)
    pagination_class = CustomPagination
    filterset_fields = ('author',)
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


class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):
        return self.request.user.follower.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
