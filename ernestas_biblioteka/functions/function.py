def check_is_user_unique(users: set, name) -> bool:
    if name not in [user.name for user in users]:
        return True
    return False


def check_is_librarian_unique(librarians: set, name) -> bool:
    if name not in [user.name for user in librarians]:
        return True
    return False
