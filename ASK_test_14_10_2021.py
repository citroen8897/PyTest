# Проверьте, что метод List Breweries корректно сортирует пивоварни по возрастанию/убыванию по postal_code

import requests


def get_sorted_list_by_field_and_param(end_point, sort_field, sort_param):
    response = requests.get(f'{end_point}?sort={sort_field}:{sort_param}')
    return response


def test_get_response():
    assert get_sorted_list_by_field_and_param(
        'https://api.openbrewerydb.org/breweries',
        'postal_code',
        'asc').status_code == 200


def test_answer_postal_code_asc():
    response = get_sorted_list_by_field_and_param(
        'https://api.openbrewerydb.org/breweries',
        'postal_code',
        'asc')

    list_of_postal_codes = []
    for item in response.json():
        list_of_postal_codes.append(item['postal_code'])
    list_of_postal_codes_2 = sorted(list_of_postal_codes)
    if list_of_postal_codes_2 == list_of_postal_codes:
        test_passed = 1
    else:
        test_passed = 0

    assert test_passed == 1


def test_answer_postal_code_desc():
    response = get_sorted_list_by_field_and_param(
        'https://api.openbrewerydb.org/breweries',
        'postal_code',
        'desc')

    list_of_postal_codes = []
    for item in response.json():
        list_of_postal_codes.append(item['postal_code'])
    list_of_postal_codes_2 = sorted(list_of_postal_codes)
    if list_of_postal_codes_2[::-1] == list_of_postal_codes:
        test_passed = 1
    else:
        test_passed = 0

    assert test_passed == 1


# _____________________________________________________________________________
# _____________________________________________________________________________

# Проверьте, что метод Get Brewery корректно возвращает пивоварню по id


def get_item_by_id(end_point, item_id):
    response = requests.get(f'{end_point}/{item_id}')
    return response


def test_answer_get_by_id():
    response_from_id = get_item_by_id(
        'https://api.openbrewerydb.org/breweries',
        'bnaf-llc-austin')
    response_from_list = requests.get(
        'https://api.openbrewerydb.org/breweries?by_name=Bnaf, LLC')

    if response_from_id.json() == response_from_list.json()[0]:
        test_passed = 1
    else:
        test_passed = 0

    assert test_passed == 1
