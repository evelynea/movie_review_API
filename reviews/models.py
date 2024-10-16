from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator

from django.utils import timezone
from django.conf import settings
from django.db import models


class MovieReview(models.Model):
    title = models.CharField(max_length=255)
    review_content = models.TextField()
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)] ,help_text="Rate the movie between 1 (worst) and 5 (best)")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="review")
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('title', 'user')  # Ensuring each user can review the same movie only once.

    def __str__(self):
        return f"review: {self.review_content} on the movie {self.title} and the rating is {self.rating}"
    
class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    review = models.ForeignKey(MovieReview, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'review')