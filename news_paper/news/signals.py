from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Post, PostCategory
from .tasks import news_created


@receiver(m2m_changed, sender=Post.categories.through)
def notify_subscribers(sender, instance, **kwargs):
    post_cats = PostCategory.objects.filter(post=instance)
    if len(post_cats) > 0:
        news_created.apply_async([instance.id])

