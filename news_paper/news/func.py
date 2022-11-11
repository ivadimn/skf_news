from .models import Post, CategoryUser
from datetime import datetime, timedelta


def get_weekly_mail():
    users = dict()
    dt = datetime.now() - timedelta(days=7)
    posts = Post.objects.filter(created_at__gt=dt)
    for post in posts:
        cats = post.categories.all()
        for cat in cats:
            us = CategoryUser.objects.filter(category=cat)
            for u in us:
                email = users.get(u.user.email)
                if email:
                    email.append(post.title)
                else:
                    users[u.user.email] = [post.title]
    return users



