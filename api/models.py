import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings


# avatar画像のアップロード先パス
def upload_avatar_path(instance, filename):
    extension = filename.split('.')[-1]
    return '/'.join(['avatars', str(instance.userProfile.id)+str(instance.nickName)+str('.')+str(extension)])


# postした画像のアップロード先パス
def upload_post_path(instance, filename):
    extension = filename.split('.')[-1]
    return '/'.join(['posts', str(instance.userPost.id)+str(instance.title)+str('.')+str(extension)])

# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email


class Profile(models.Model):
    nickName = models.CharField(max_length=20)
    userProfile = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name='userProfile', on_delete=models.CASCADE
    )

    create_on = models.DateTimeField(auto_now_add=True)
    img = models.ImageField(blank=True, null=True,
                            upload_to=upload_avatar_path)

    def __str__(self):
        return self.nickName


class Post(models.Model):
    title = models.CharField(max_length=255)
    """
    関連させるモデルのオブジェクトが一つしかないなら ForeignKey に、複数なら ManyToManyField にします。
    only many_to_one is allowed
    source url: https://docs.djangoproject.com/en/3.2/_modules/django/db/models/fields/related/#ForeignKey
    """
    userPost = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='userPost', on_delete=models.CASCADE
    )
    img = models.ImageField(blank=True, null=True, upload_to=upload_post_path)
    liked = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='liked', blank=True)
    create_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    text = models.CharField(max_length=1000)
    userComment = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='userComment', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.text
