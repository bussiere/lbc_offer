from .models import Token


def validateToken(token):
    try:
        t = Token.objects.get(value=token)
        return True
    except Token.DoesNotExist:
        return False
