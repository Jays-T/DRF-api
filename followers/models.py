from django.db import models
from django.contrib.auth.models import User


class Follower(models.Model):
    """
    Follower model is related to 'owner' and 'followed'.
    'owner' is a User that is following another User.
    'followed' is a User that is followed by 'owner'.
    The related name is required so that django can differentiate
    between 'owner' and 'followed' both of whom are User model instances.
    'unique_together' makes sure a User cannot follow the same User twice.
    """
    owner = models.ForeignKey(
        User, related_name='following', on_delete=models.CASCADE
    )
    followed = models.ForeignKey(
        User, related_name='followed', on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ['-created_at']
        unique_together = ['owner', 'followed']

    def __str__(self) -> str:
        return f'{self.owner} {self.followed}'
