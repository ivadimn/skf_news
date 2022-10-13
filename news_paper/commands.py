from news.models import *
from news.lorem import get_text, get_title, get_content
from random import randint, choice
from django.contrib.auth.models import User
# Создать пользователей (с помощью метода User.objects.create_user('username')).
names = ["John", "Sara", "Pete", "Ann", "Olga"]
users = []
for name in names:
    users.append(User.objects.create_user(name))
# Создать модели Author, связанные с пользователями.
authors = []
for user in users:
    authors.append(Author.objects.create(user = user))

# Добавить категории
politics = Category.objects.create(name = "Политические события")
sport = Category.objects.create(name = "Спортивные соревнования")
science = Category.objects.create(name = "Научные открытия")
cinema = Category.objects.create(name = "Новинки кинематографа")
theatre = Category.objects.create(name = "Театральная жизнь")
categories = [politics, sport, science, cinema, theatre]

# Добавить статьи и новости
posts = []
for author in authors:
    title = get_title()
    content = get_content(randint(2, 8))
    posts.append(Post.objects.create(author = author, type_post=Post.article, title=title, content=content))
    title = get_title()
    content = get_content(randint(2, 8))
    posts.append(Post.objects.create(author = author, type_post=Post.article, title=title, content=content))
    title = get_title()
    content = get_content(randint(2, 8))
    posts.append(Post.objects.create(author=author, type_post=Post.news, title=title, content=content))
    title = get_title()
    content = get_content(randint(2, 8))
    posts.append(Post.objects.create(author=author, type_post=Post.news, title=title, content=content))

# Присвоить статьям и новостям категории
for post in posts:
    cats = categories.copy()
    cat = choice(cats)
    PostCategory.objects.create(post=post, category=cat)
    cats.remove(cat)
    PostCategory.objects.create(post=post, category=choice(cats))

# Создать комментарии
for post in posts:
    for author in authors:
        for n in range(randint(1, 3)):
            content = get_text(1)
            Comment.objects.create(post=post, user=author.user, content=content)

# Применяя функции like() и dislike() к статьям/новостям и комментариям, скорректировать рейтинги этих объектов.
like_dislike()

# Обновить рейтинги пользователей.
for author in authors:
    update_rating(author)

# Вывести username и рейтинг лучшего пользователя (применяя сортировку и возвращая поля первого объекта).
authors_sort = Author.objects.order_by("-rating")
print("Лучший пользователь: {0}, его рейтинг: {1}".format(authors_sort[0].user.username, authors_sort[0].rating))

# Вывести дату добавления, username автора, рейтинг,
# заголовок и превью лучшей статьи, основываясь на лайках/дислайках к этой статье.
post = Post.objects.order_by("-rating")[0]
print("Лучшая статья: ")
print("Дата добавления: {0}, Автор: {1}, рейтинг: {2}, название: {3}".
        format(post.created_at.strftime("%d.%m.%Y"), post.author.user.username, post.rating, post.title))
print("Предпросмотр:\n {0}".format(post.preview()))

