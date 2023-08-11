from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

class City(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class User(AbstractUser):
    username = models.CharField(max_length=100, null=True)
    email = models.EmailField(unique=True, null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)
    number = models.IntegerField(blank=True, null=True)
    avatar = models.ImageField(null=True, default="avatar.png")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  # removes email from REQUIRED_FIELDS

class Breed(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Purpose(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Sex(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Announcment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    favorites = models.ManyToManyField(User,related_name='favorites',blank=True)
    image = models.ImageField(null=True,default='dog-icon.png')
    name = models.CharField(max_length=200)
    breed = models.ForeignKey(Breed, on_delete=models.SET_NULL, null=True)
    old = models.CharField(max_length=50, null=True)
    sex = models.ForeignKey(Sex, on_delete=models.SET_NULL, null=True)
    documents = models.CharField(max_length=100, null=True, blank=True)
    purpose = models.ForeignKey(Purpose, on_delete=models.SET_NULL, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    description = models.TextField(null=True, blank=True)
    price = models.IntegerField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)



    def __str__(self):
        return f'{self.name[0:50]}, {self.owner.email}'

    class Meta:
        ordering = ['-updated', '-created']

class Chat(models.Model):
    participants = models.ManyToManyField(User, related_name='participants')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user_id = models.IntegerField(null=True, blank=True)

    def __str__(self):
        name = list(self.participants.all())

        return f'{name}, chat_id: {self.id}'

class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created']

    def __str__(self):
        name = f'{self.body[0:50]}, {self.user}, chat_id: {self.chat.id}, {self.created}'
        return name
