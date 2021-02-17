from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your models here.





class Blog(models.Model):
    author = models.ForeignKey(User, related_name='author_messages', on_delete=models.CASCADE)
    post = models.TextField(blank=True)
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author.username

    @classmethod
    def last_10_messages(cls):
        return Blog.objects.order_by('-create_time').all()[:10]