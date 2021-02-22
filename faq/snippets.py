import secrets

ALL_URL_CHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
def create_random_slug(size=10):
    """amount of characters you want generated for random_slug"""
    res=''.join(secrets.choice(ALL_URL_CHARS) for _ in range(size))
    return str(res)
