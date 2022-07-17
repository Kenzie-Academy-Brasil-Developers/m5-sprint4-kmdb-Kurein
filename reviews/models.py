from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class TypeReview(models.TextChoices):
    MW = "Must Watch"
    SW = "Should Watch"
    AW = "Avoid Watch"
    NO = "No Opinion"

class Review(models.Model):
    stars = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])
    review = models.TextField()
    spoilers = models.BooleanField(default=False)
    recomendation = models.CharField(max_length=50, choices=TypeReview.choices, default=TypeReview.NO)

    movie = models.ForeignKey(to="movies.Movie", on_delete=models.CASCADE, related_name="reviews")

    critic = models.ForeignKey(to="accounts.User", on_delete=models.CASCADE, related_name="reviews")