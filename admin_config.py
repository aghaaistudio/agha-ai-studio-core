UNLIMITED_ADMINS = ["aghaaistudiosupport@gmail.com", "aghaaistoudio@gmail.com"]

def is_unlimited_admin(email):
    if not email: return False
    return email.lower() in UNLIMITED_ADMINS
