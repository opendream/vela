from account.models import User


def rewrite_username(username):

    _username_ = username.lower().split('@')[0].replace(' ', '.')
    username = _username_
    usernames = [u for u in User.objects.values_list('username', flat=True)]
    increment_number = 1
    while True:
        if username in usernames:
            username = "%s%s" % (_username_, increment_number)
            increment_number += 1
        else:
            break

    return username