from django.db import models
from django.contrib.auth.models import User

class FriendRequest(models.Model):
    STATUS_CHOICES = [
        ('accepted', 'accepted'),
        ('rejected', 'rejected'),
        ('pending', 'pending'),
    ]
    from_user = models.ForeignKey(User, related_name='from_user', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='to_user', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    def __str__(self):
        return f"{self.from_user.username} -> {self.to_user.username}"