from ernestas_biblioteka.classes_dto.login_user_data import LoginUserDataDTO, UserTakenBookDTO


def create_login_user_data_DTO(query_results):
    if not query_results:
        return None
    # login_user_data = {}
    # login_user = None
    books_list = []
    for res in query_results:
        taken_book = UserTakenBookDTO(**res)
        if taken_book.uuid:
            books_list.append(taken_book)
        login_user = LoginUserDataDTO(**res)

    login_user.taken_books_list = books_list

    return login_user


def create_books_DTO(query_results):
    books_list = []
    if not query_results:
        return books_list
    for res in query_results:
        taken_book = UserTakenBookDTO(**res)
        if taken_book:
            books_list.append(taken_book)

    return books_list
