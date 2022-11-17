from celery import shared_task
import time
from .models import Post, PostCategory
from .func import get_email_list, send_email


@shared_task
def news_created(post_id):
    post = Post.objects.get(pk=post_id)
    post_cats = PostCategory.objects.filter(post=post)
    if len(post_cats) > 0:
        email_list = get_email_list(post_cats, post)
        send_email(post, email_list)


@shared_task
def printer(n):
    for i in range(n):
        time.sleep(1)
        print(i+1)
