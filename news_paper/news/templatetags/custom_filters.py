from django import template
import json
import string


class Censor:

    def __init__(self):
        self.__mat = self.load_mat()

    def cencor(self, content: str) -> str:
        raw_words = content.split()
        words = [word for word in content.translate(str.maketrans("", "", string.punctuation)).split()]
        for i, word in enumerate(words):
            if word in self.__mat:
                raw_word = raw_words[i]
                last_symbol = raw_word[-1]
                if last_symbol.isalpha():
                    raw_words[i] = self.__replace(raw_word)
                else:
                    raw_words[i] = "{0}{1}".format(self.__replace(raw_word[:-1]), last_symbol)
        return " ".join(raw_words)

    def __replace(self, word: str) -> str:
        return "{0}{1}{2}".format(word[0], "*" * (len(word) - 2), word[-1])

    def load_mat(self) -> list:
        with open("cenz.json", "r", encoding="utf-8") as ef:
            return json.load(ef)


register = template.Library()
cens = Censor()


@register.filter()
def censor(value: str) -> str:
    return cens.cencor(value)
