from django import template

register = template.Library()


@register.filter(name="user_value")
def user_value(question, user):
    if not user.is_authenticated:
        return 0
    return question.user_value(user)


@register.filter(name="user_likes")
def user_likes(question, user):
    if not user.is_authenticated:
        return False
    return question.user_likes(user)


@register.filter(name="user_dislikes")
def user_dislikes(question, user):
    if not user.is_authenticated:
        return False
    return question.user_dislikes(user)
