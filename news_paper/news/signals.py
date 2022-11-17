from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from .models import Post, PostCategory
from .tasks import news_created


@receiver(m2m_changed, sender=Post.categories.through)
def notify_subscribers(sender, instance, **kwargs):
    #news_created.apply_async([instance.id])
    news_created.delay(instance.id)




