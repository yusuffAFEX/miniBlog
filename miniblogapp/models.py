import profile

from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from PIL import Image


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField()
    image = models.ImageField(null=True, blank=True, upload_to='post')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', args=[str(self.slug)])


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, editable=False)
    text = models.TextField()
    email = models.EmailField(editable=False)
    firstname = models.CharField(max_length=200, null=True, editable=False)
    lastname = models.CharField(max_length=200, null=True, editable=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.firstname}, {self.lastname}'


class Profile(models.Model):
    image = models.ImageField(null=True, blank=True, upload_to='media/photos')
    author = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.author.first_name} Profile'

    def save(self, *args, **kwargs):
        super(Profile, self).save()
        if self.image:
            image = Image.open(self.image.path)
            if image.height > 300 and image.width >300:
                size = (200, 200)
                image.thumbnail(size)
                image.save(self.image.path)




@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(author=instance)


# @receiver(post_save, sender=User)
# def save_profile(sender, instance, **kwargs):
#     instance.profile.save()
