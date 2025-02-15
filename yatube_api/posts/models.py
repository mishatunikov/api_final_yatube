from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Post(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts'
    )
    image = models.ImageField(upload_to='posts/', null=True, blank=True)
    group = models.ForeignKey(
        'Group',
        verbose_name='posts',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.text

    class Meta:
        ordering = ('-pub_date',)


class Group(models.Model):
    title = models.CharField(max_length=64, unique=True)
    slug = models.SlugField(max_length=64)
    description = models.TextField()

    def __str__(self):
        return self.title


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments'
    )
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments'
    )
    text = models.TextField()
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )


class Follow(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user_following'
    )
    following = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='followers'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'following'), name='unique_user_following'
            ),
            models.CheckConstraint(
                check=~models.Q(user=models.F('following')),
                name='user_not_equal_following',
            ),
        ]
