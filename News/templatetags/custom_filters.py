from django import template

register = template.Library()


@register.filter()
def censor(text: str):

    censor_list = [
        'убить',
        'уничтожить',
        'ненавижу',
    ]

    words_list = text.split(' ')

    for i, word in enumerate(words_list):
        if word in censor_list:
            words_list[i] = ''.join([word[0], '*' * (len(word) - 1)])

    words_list = ' '.join(words_list)

    return words_list
