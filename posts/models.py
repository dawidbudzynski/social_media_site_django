import misaka
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.db import models
from groups.models import Group

User = get_user_model()


class Post(models.Model):
    user = models.ForeignKey(User, related_name="posts")
    created_at = models.DateTimeField(auto_now=True)
    message = models.TextField()
    message_html = models.TextField(editable=False)
    group = models.ForeignKey(Group, related_name="posts", null=True, blank=True)
    image = models.ImageField(upload_to='images/', null=True)

    def __str__(self):
        return self.message

    def save(self, *args, **kwargs):
        self.message_html = misaka.html(self.message)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            "groups:single",
            kwargs={
                "slug": self.group.slug,
            }
        )

    class Meta:
        ordering = ["-created_at"]
        unique_together = ["user", "message"]
