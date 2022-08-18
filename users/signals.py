from django.contrib.auth.models import User
from .models import Profile

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from django.core.mail import send_mail
from django.conf import settings

def profileCreate(sender, instance, created, **kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(
            user = user,
            email = user.email,
        )

        subject = 'Welcome'
        message = 'Super'

        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [profile.email],
            fail_silently=False,
        )


def userDelete(sender, instance, **kwargs):
    user = instance.user
    user.delete()

post_save.connect(profileCreate, sender=User)
post_delete.connect(userDelete, sender=Profile)

@receiver(post_save, sender=Profile)
def profileUpdated(sender, instance, created, **kwargs):
    print('Profile Saved!')
    print('Instance: ', instance)
    print('Created: ', created)

def profileDelete(sender, instance, **kwargs):
    print('Deleting user')

# post_save.connect(profileUpdated, sender=Profile)
# post_delete.connect(profileDelete, sender=Profile)
