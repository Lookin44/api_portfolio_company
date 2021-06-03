from django.db import models

from users.models import User


class Company(models.Model):
    name = models.CharField(max_length=50, unique=True)
    about = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='companys'
    )

    def __str__(self):
        return self.name


class CompanyNews(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='news'
    )
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name='news'
    )
    text = models.TextField()
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )

    class Meta:
        ordering = ('-created', )

    def __str__(self):
        return self.text[:20]


class Follow(models.Model):

    user = models.ForeignKey(
        User,
        related_name='follower',
        on_delete=models.CASCADE
    )
    following = models.ForeignKey(
        User,
        related_name='following',
        on_delete=models.CASCADE
    )

    class Meta:
        constraints = [models.UniqueConstraint(fields=['user', 'following'],
                                               name='unique_follows')]
