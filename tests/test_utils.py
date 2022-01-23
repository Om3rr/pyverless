from collections import OrderedDict

import yaml

from pyverless import remove_non_values, capitalize_str


def test_ordered_yaml():
    from pyverless.gen import setup_yaml
    setup_yaml()
    ordered_dict = OrderedDict([('a', 1), ('b', 2)])
    ordered_yaml = yaml.dump(ordered_dict)
    assert ordered_yaml.index('a') < ordered_yaml.index('b')


def test_remove_non_values():
    a = {'a': None, 'b': 2}
    assert "a" not in remove_non_values(a)
    b = {'b': 3, 'c': 4}
    assert "b" in remove_non_values(b)


def test_capitalize_str():
    assert capitalize_str("test") == "test"
    assert capitalize_str("test", with_first=True) == "Test"
    assert capitalize_str("test_me", with_first=True) == "TestMe"
    assert capitalize_str("test_me", with_first=False) == "testMe"


def test_convert_snake_keys_to_capitalize():
    from pyverless import convert_snake_keys_to_capitalize
    a = {'a_b': 1, 'a_c': 2}
    assert convert_snake_keys_to_capitalize(a) == {'aB': 1, 'aC': 2}
