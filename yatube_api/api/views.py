from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.generics import get_object_or_404
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import (
    GenericViewSet,
    ModelViewSet,
    ReadOnlyModelViewSet,
)

from api.permissions import IsAuthor
from api.serializers import (
    CommentSerializer,
    FollowSerializer,
    GroupSerializer,
    PostSerializer,
)
from posts.models import Comment, Follow, Group, Post


class AuthorAccessMixin:
    """Определяет доступ к изменению объекта только для автора."""

    def get_permissions(self):
        permissions = super().get_permissions()
        if self.request.method not in SAFE_METHODS:
            permissions.append(IsAuthor())
        return permissions


class AuthorCreateMixin:
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostViewSet(AuthorAccessMixin, AuthorCreateMixin, ModelViewSet):
    """Обработки запросов к модели Post."""

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = LimitOffsetPagination


class GroupViewSet(ReadOnlyModelViewSet):
    """Обработка запросов к модели Group."""

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


class FollowViewSet(
    AuthorCreateMixin, CreateModelMixin, ListModelMixin, GenericViewSet
):
    """Обработка запросов к модели Follow."""

    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (SearchFilter,)
    search_fields = ('following__username',)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        following = request.data.get('following')

        if (
            self.get_user()
            .user_following.filter(following__username=following)
            .exists()
        ):
            return Response(
                {'detail': 'Вы уже подписаны на этого пользователя.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if self.get_user().username == following:
            return Response(
                {'detail': 'Нельзя оформить подписку на себя.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return super().create(request, *args, **kwargs)

    def get_queryset(self):
        return self.get_user().user_following.all()

    def get_user(self):
        return self.request.user
