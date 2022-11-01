from flask import g


def current_user():
    return dict(current_user=g.user)
