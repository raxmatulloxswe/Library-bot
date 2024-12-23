from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

from apps.common.models import BaseModel


User = get_user_model()

# Create your models here.
class BotAdmin(BaseModel):
    telegram_id = models.CharField(max_length=128, verbose_name=_("Telegram ID of the bot admin"))

    def __str__(self):
        return f"{self.telegram_id}"

class Category(BaseModel):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name

class Author(BaseModel):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name
    
class Book(BaseModel):
    name = models.CharField(max_length=128)
    description = models.TextField()
    image = models.ImageField(upload_to='book/images/')
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, related_name='books')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='books')

    def __str__(self):
        return f"{self.name} | {self.author.name}"

class Comment(BaseModel):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='comments')
    comment = models.TextField()
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True, related_name='comments')
    rating = models.PositiveIntegerField(default=1)
    
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.user.first_name

class Challenge(BaseModel):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    title = models.CharField(max_length=128)
    challenger = models.ForeignKey(User, on_delete=models.CASCADE, related_name='challenges_initiated')
    opponent = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='challenges_received')
    book = models.CharField(max_length=128)
    book_pages_count = models.PositiveIntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    challenger_progress = models.FloatField(default=0.0, help_text="Percentage of book read by challenger")
    opponent_progress = models.FloatField(default=0.0, help_text="Percentage of book read by opponent")
    winner_contestant = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="challenges_winner")

    def __str__(self):
        return f"Challenge between {self.challenger.first_name} and {self.opponent.first_name} for '{self.book}'"

class Results(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='results')
    book_name = models.CharField(max_length=128)
    read_pages_count = models.PositiveIntegerField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.book_name} | {self.user.first_name}"