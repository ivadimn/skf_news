from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver # импортируем нужный декоратор
from .mail import Mail
from django.template.loader import render_to_string
from .models import Post, PostCategory, CategoryUser


def get_email_list(post_cats, instance) -> list:
    emails_list = []
    for cat in post_cats:
        for cat_user in CategoryUser.objects.filter(category=cat.category):
            print(cat_user.user.email)
            emails_list.append((cat_user.user.email, instance.title, render_to_string(
                'news_created.html',
                {
                    'post': instance,
                    'user': cat_user.user.username
                }
            )))
    return emails_list


def send_email(email_list: list):
    with Mail("pickup.music@mail.ru") as mail:
        for email in email_list:
            mail.prepare_html(email[1], email[2])
            mail.send(email[0])


@receiver(m2m_changed, sender=Post.categories.through)
def notify_subscribers(sender, instance, **kwargs):
    post_cats = PostCategory.objects.filter(post=instance)
    if len(post_cats) > 0:
        email_list = get_email_list(post_cats, instance)
        print(email_list)
        send_email(email_list)



