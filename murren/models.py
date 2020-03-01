from PIL import Image
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import AbstractUser
from django.db import models


class Murren(AbstractUser):

    email = models.EmailField(unique=True)
    murren_avatar = models.ImageField(default='default_murren_avatar.png', upload_to='murren_pics',
                                      verbose_name='Аватар Муррена')

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.murren_avatar.path)

        if img.mode in ('RGBA', 'LA'):
            fill_color = '#A36FFF'
            background = Image.new(img.mode[:-1], img.size, fill_color)
            background.paste(img, img.split()[-1])
            img = background

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.murren_avatar.path)


class PasswordResetManager(models.Manager):
    def create_token(self, murren, password, token):
        password_reset = PasswordReset()
        password_reset.murren = murren
        password_reset.password = password
        password_reset.token = token
        password_reset.save()
        
        return password_reset
    
    def is_last_password_match(self, murren, raw_password, replay: 5):
        password = self.filter(murren=murren).order_by('-created_at')[:replay]
        
        return any(check_password(raw_password, p.password) for p in password)


class PasswordReset(models.Model):
    murren = models.ForeignKey(Murren, on_delete=models.CASCADE)
    token = models.CharField(max_length=64)
    password = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    
    objects = PasswordResetManager()
    
    def __str__(self):
        return self.murren.username
    
    def set_password(self, password):
        self.murren.set_password(password)
        self.murren.save()
    
    def is_password_changed(self):
        return self.murren.password != self.password
