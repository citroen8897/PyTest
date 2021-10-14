# Проверьте, что метод List Breweries корректно сортирует пивоварни по возрастанию/убыванию по postal_code

import requests


def get_sorted_list_by_field_and_param(end_point, sort_field, sort_param):
    """
    Метод возвращает ответ со списком элементов, полученных с указанного эндпоинта,
    отсортированных по указанному в запросе полю,
    а также указывает прямую/обратную сортировку списка.
    элементов.
    :param end_point: str;
    :param sort_field: str;
    :param sort_param: str;
    :return: requests;
    """
    response = requests.get(f'{end_point}?sort={sort_field}:{sort_param}')
    return response


def test_get_response():
    """
    Проверка доступности эндпоинта. Если тест провален - возращается False.
    :return:
    """
    assert get_sorted_list_by_field_and_param(
        'https://api.openbrewerydb.org/breweries',
        'postal_code',
        'asc').status_code == 200


def test_answer_postal_code_asc():
    """
    Метод проверки сортировки элементов по возрастанию.
    Если тест провален - возращается False.
    :return: bool;
    """
    response = get_sorted_list_by_field_and_param(
        'https://api.openbrewerydb.org/breweries',
        'postal_code',
        'asc')

    list_of_postal_codes = []
    for item in response.json():
        list_of_postal_codes.append(item['postal_code'])
    list_of_postal_codes_2 = sorted(list_of_postal_codes)
    if list_of_postal_codes_2 == list_of_postal_codes:
        assert True
    else:
        assert False


def test_answer_postal_code_desc():
    """
        Метод проверки сортировки элементов по убыванию.
        Если тест провален - возращается False.
        :return: bool;
        """
    response = get_sorted_list_by_field_and_param(
        'https://api.openbrewerydb.org/breweries',
        'postal_code',
        'desc')

    list_of_postal_codes = []
    for item in response.json():
        list_of_postal_codes.append(item['postal_code'])
    list_of_postal_codes_2 = sorted(list_of_postal_codes)
    if list_of_postal_codes_2[::-1] == list_of_postal_codes:
        assert True
    else:
        assert False


# _____________________________________________________________________________
# _____________________________________________________________________________

# Проверьте, что метод Get Brewery корректно возвращает пивоварню по id


def get_item_by_id(end_point, item_id):
    """
    Метод возвращает ответ с элементом по указанному ID элемента,
    полученным с указанного эндпоинта.
    :param end_point: str;
    :param item_id: str;
    :return: requests;
    """
    response = requests.get(f'{end_point}/{item_id}')
    return response


def test_answer_get_by_id():
    """
    Метод проверки корректного возврата элемента по его ID.
    В качестве эталонного элемента взят 1-й элемент общего списка.
    :return: bool;
    """
    response_from_id = get_item_by_id(
        'https://api.openbrewerydb.org/breweries',
        'bnaf-llc-austin')
    response_from_list = requests.get(
        'https://api.openbrewerydb.org/breweries?by_name=Bnaf, LLC')

    if response_from_id.json() == response_from_list.json()[0]:
        assert True
    else:
        assert False
