from celery import shared_task
import os
from .models import Post, PostCategory
from .func import get_email_list, send_email, send_weekly_email


@shared_task
def news_created(post_id, pickup):
    post = Post.objects.get(pk=post_id)
    post_cats = PostCategory.objects.filter(post=post)
    if len(post_cats) > 0:
        email_list = get_email_list(post_cats, post)
        send_email(post, email_list, pickup)


@shared_task
def inform_weekly():
    pickup = os.environ.get("PICKUP")
    send_weekly_email(pickup)
