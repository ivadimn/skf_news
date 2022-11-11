from datetime import datetime, timedelta
import logging
from news_paper.news.models import Post, CategoryUser
from news_paper.news.mail import Mail
from django.conf import settings
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution


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


logger = logging.getLogger(__name__)


def send_weekly_email():
    users = get_weekly_mail()
    with Mail("pickup.music@mail.ru") as mail:
        for email, body in users.items():
            content = "\n".join(body)
            mail.prepare_text("Новостные новинки", content)
            mail.send(email)


def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # добавляем работу нашему задачнику
        scheduler.add_job(
            send_weekly_email,
            trigger=CronTrigger(day_of_week="sun", hour="00", minute="00"),
            id="send_weekly_email",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'send_weekly_email'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")