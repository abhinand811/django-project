from django.db import models
from user.models import Account


class Room(models.Model):
    USER_TYPE_CHOICES = (
        (1, 'Student'),
        (2, 'Teacher'),
        (3, 'Teacher'),

    )
    name = models.CharField(max_length=128)
    online = models.ManyToManyField(to=Account, blank=True, related_name='users_online')
    type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES)
    created_by = models.ForeignKey(Account, on_delete=models.CASCADE)

    def get_online_count(self):
        return self.online.count()

    def join(self, user):
        self.online.add(user)
        self.save()

    def leave(self, user):
        self.online.remove(user)
        self.save()

    def __str__(self):
        return f'{self.name} ({self.get_online_count()})'


class Message(models.Model):
    user = models.ForeignKey(to=Account, on_delete=models.CASCADE)
    room = models.ForeignKey(to=Room, on_delete=models.CASCADE)
    content = models.CharField(max_length=512)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.name}: {self.content} [{self.timestamp}]'
