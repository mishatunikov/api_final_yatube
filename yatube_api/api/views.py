from rest_framework.generics import get_object_or_404
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly, SAFE_METHODS

from api.serializers import PostSerializer, GroupSerializer, CommentSerializer
from api.permissions import IsAuthor
from posts.models import Post, Group, Comment


class AuthorAccessMixin:
    """Определяет доступ к изменению объекта только для автора."""

    def get_permissions(self):
        permissions = super().get_permissions()
        if self.request.method not in SAFE_METHODS:
            permissions.append(IsAuthor())
        return permissions


class PostViewSet(AuthorAccessMixin, ModelViewSet):
    """Обработки запросов к модели Post."""

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(ReadOnlyModelViewSet):
    """Обработка запросов к модели Group"""

    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(AuthorAccessMixin, ModelViewSet):
    """Обработка запросов к модели Comment."""

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        return self.get_post().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, post=self.get_post())

    def get_post(self):
        return get_object_or_404(Post, pk=self.kwargs['post_id'])




