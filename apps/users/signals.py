from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify
from django.contrib.auth import get_user_model

User = get_user_model()


@receiver(post_save, sender=User)
def populate_username(sender, instance, created, **kwargs):
    if created and not instance.username:
        instance.username = slugify(f"{instance.first_name}-{instance.id}")
        instance.save()

