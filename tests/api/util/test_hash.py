from src.api.util.hash import hash_dict, hash_string


def test_hash_dict_success():
    test_dict = {"test1": "test1", "test2": "test2"}
    response = hash_dict(test_dict)
    assert response is not None
    assert type(response) == str
    assert len(response) == 64  # response should be base64


def test_hash_dict_order_success():
    # The same dict, in a different order, should return the same hash.
    test_dict = {"atest1": "atest1", "ztest2": "ztest2"}
    test_dict_reverse = {"ztest2": "ztest2", "atest1": "atest1"}
    response = hash_dict(test_dict)
    response_reverse = hash_dict(test_dict_reverse)
    # Response should be the same, no mater the order of the dict.
    assert response == response_reverse


def test_hash_string_success():
    response = hash_string("test")
    assert response is not None
    assert type(response) == str
    assert len(response) == 64  # response should be base64
