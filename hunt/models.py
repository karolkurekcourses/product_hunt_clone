from django.db import models
from django.conf import settings


class Product(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    short_body = models.CharField(max_length=511)
    url = models.TextField()
    pub_datetime = models.DateTimeField()
    votes = models.IntegerField(default=1)
    icon = models.ImageField(upload_to='images/')
    image = models.ImageField(upload_to='images/')
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    vote_users = models.TextField(default='', blank=True)

    def __str__(self):
        return self.title

    def pub_date(self):
        return self.pub_datetime.strftime("%d.%m.%Y")

    def body_begin(self):
        if '.' in self.body:
            return '.'.join(self.body.split('.')[:2])
        else:
            return ' '.join(self.body.split(' ')[:12])

    def body_rest(self):
        if '.' in self.body:
            return '.'.join(self.body.split('.')[2:])
        else:
            return ' '.join(self.body.split(' ')[12:])