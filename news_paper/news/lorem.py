from random import choice, randint
from .models import *
from random import randint, choice
from django.contrib.auth.models import User
from datetime import datetime, timedelta
import json
import string

one = [
    "Товарищи! ",
    "С другой стороны ",
    "Равным образом ",
    "Не следует однако забывать, что ",
    "Таким образом ",
    "Повседневная практика показывает, что ",
]
two = [
    "реализация намеченных плановых заданий ",
    "рамки и место обучения кадров ",
    "постоянный количественный рост и сфера нашей активности ",
    "сложившаяся структура организации ",
    "новая модель организационной деятельности ",
    "дальнейшее развитие различных форм деятельности ",
]
three = [
    "играет важную роль в формировании ",
    "требует от нас анализа ",
    "требует определения и уточнения ",
    "способствует подготовке и реализации ",
    "обеспечивает широкому кругу (специалистов) участие в формировании ",
    "позволяет выполнить важные задания по разработке ",
]
four = [
    "существенных финансовых и административных условий. ",
    "дальнейших направлений развития. ",
    "системы массового участия. ",
    "позиций, занимаемых участниками в отношении поставленных задач. ",
    "новых предложений. ",
    "направлений прогрессивного развития. ",
]

sentences = [
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit. ",
    "Quisque vitae varius ex, eu volutpat orci. ",
    "Aenean ullamcorper orci et vulputate fermentum. ",
    "Cras erat dui, finibus vel lectus ac, pharetra dictum odio. ",
    "Nullam tempus scelerisque purus, sed mattis elit condimentum nec. ",
    "Etiam risus sapien, auctor eu volutpat sit amet, porta in nunc. ",
    "Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. ",
    "Proin ipsum purus, laoreet quis dictum a, laoreet sed ligula. ",
    "Integer ultricies malesuada quam. ",
    "Cras vel elit sed mi placerat pharetra eget vel odio. ",
    "Duis ac nulla varius diam ultrices rutrum. ",
]


def get_sentence(s_lst: list, mat_lst: list) -> str:
    n = randint(0, 1)
    if n == 1:
        mat = choice(mat_lst)
        pos = randint(1, len(s_lst) - 1)
        s_lst.insert(pos, mat)
    return " ".join(s_lst)


def get_content(scount: int = 2) -> str:
    with open("cenz.json", "r", encoding="utf-8") as ef:
        j_list = json.load(ef)
    content = [one[0]]
    for s in range(scount):
        ss = []
        if s > 0:
            ss.append(one[randint(1, 5)])
        ss.append(choice(two))
        ss.append(choice(three))
        ss.append(choice(four))
        sentence = get_sentence(" ".join(ss).split(), j_list)
        content.append(sentence)
    return " ".join(content)


def get_text(pcount: int = 2) -> str:
    length = [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
    paragraphs = [sentences[0]]
    for i in range(1, pcount + 1):
        paragraph = ""
        numofsentences = choice(length)
        for j in range(1, numofsentences + 1):
            sentence = choice(sentences)
            paragraph = paragraph + sentence
        paragraphs.append(paragraph)
    return "\n".join(paragraphs)


def get_title() -> str:
    with open("cenz.json", "r", encoding="utf-8") as ef:
        j_list = json.load(ef)
    return get_sentence(choice(sentences).split(), j_list)


def replace(word: str) -> str:
    return "{0}{1}".format(word[0], "*" * (len(word) - 1))


def censor(content: str) -> str:
    with open("cenz.json", "r", encoding="utf-8") as ef:
        j_list = json.load(ef)
    raw_words = content.split()
    words = [word for word in content.translate(str.maketrans("", "", string.punctuation)).split()]
    for i, word in enumerate(words):
        if word in j_list:
            raw_word = raw_words[i]
            last_symbol = raw_word[-1]
            if last_symbol.isalpha():
                raw_words[i] = replace(raw_word)
            else:
                raw_words[i] = "{0}{1}".format(replace(raw_word[:-1]), last_symbol)
    return " ".join(raw_words)


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
