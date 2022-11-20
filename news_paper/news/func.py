from django.template.loader import render_to_string
from django.core.mail import  send_mail
from datetime import datetime, timedelta
from .models import Post, CategoryUser
from .mail import Mail


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


def send_weekly_email(pickup):
    users = get_weekly_mail()
    # for email, body in users.items():
    #     send_mail(
    #         subject="Новостные новинки",
    #         message=content,
    #         from_email="ivadimn65@yandex.ru",
    #         recipient_list=[email, ]
    #     )
    with Mail("pickup.music@mail.ru", pickup) as mail:
        for email, body in users.items():
            content = "\n".join(body)
            mail.prepare_text("Новостные новинки", content)
            mail.send(email)


def get_email_list(categories, post: Post):
    emails_list = []
    for cat in categories:
        for cat_user in CategoryUser.objects.filter(category=cat.category):
            emails_list.append((cat_user.user.email, post.title, render_to_string(
                'news_created.html',
                {
                    'hello': "Здравствуй, {0}. Новая статья в твоём любимом разделе!".format(cat_user.user.username),
                    'post': post,
                }
            )))
    return emails_list


def send_email(post: Post, email_list: list, pickup: str):
    print(post)
    # for email in email_list:
    #     send_mail(
    #         subject="Добавлена новост: {0}".format(post.title),
    #         message=post.content,
    #         from_email="ivadimn65@yandex.ru",
    #         recipient_list=[email[0], ]
    #     )
    with Mail("pickup.music@mail.ru", pickup) as mail:
        for email in email_list:
            mail.prepare_html(email[1], email[2])
            mail.send(email[0])
