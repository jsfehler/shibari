import time

import pytest

import shibari


rig = shibari.Rig('ebi', 'hishi')


@rig.bind('ebi')
def timestamp():
    return str(time.time())


@rig.bind('ebi')
def timestamp_with_args(a, b):
    return f"{a}_{str(time.time())}_{b}"


@rig.free('ebi')
def finish():
    pass


@rig.free('ebi')
def finish_fail():
    raise ValueError('ded')


class BoundClass:
    method_rig = shibari.Rig('ebi', 'hishi')

    @method_rig.bind('ebi')
    def timestamp(self):
        return str(time.time())

    @method_rig.bind('ebi')
    def timestamp_with_args(self, a, b):
        return f"{a}_{str(time.time())}_{b}"

    @method_rig.free('ebi')
    def finish(self):
        pass


@pytest.fixture
def bound_class():
    return BoundClass()


def test_bind_function(request):
    """
    Given I have a bound function
    When I call the bound function for a second time
    Then the results are identical
    """
    result = timestamp()

    time.sleep(0.1)

    assert result == timestamp()

    def fin():
        rig.free('ebi')

    request.addfinalizer(fin)


def test_bind_function_with_args(request):
    """
    Given I have a bound function with arguments
    When I call the bound function for a second time
    Then the results are identical
    """
    result = timestamp_with_args('000', 'ZZZ')

    time.sleep(0.1)

    assert result == timestamp_with_args('000', 'ZZZ')

    def fin():
        rig.free('ebi')

    request.addfinalizer(fin)


def test_bind_method(request, bound_class):
    """
    Given I have a bound method
    When I call the bound method for a second time
    Then the results are identical
    """
    result = bound_class.timestamp()

    time.sleep(0.1)

    assert result == bound_class.timestamp()

    def fin():
        bound_class.finish()

    request.addfinalizer(fin)


def test_bind_method_with_args(request, bound_class):
    """
    Given I have a bound method with arguments
    When I call the bound method for a second time
    Then the results are identical
    """
    result = bound_class.timestamp_with_args('000', 'ZZZ')

    time.sleep(0.1)

    assert result == bound_class.timestamp_with_args('000', 'ZZZ')

    def fin():
        bound_class.finish()

    request.addfinalizer(fin)


def test_free_direct():
    """Given I have a bound function
    With I call a function that frees the bind
    And I call the function for a second time
    Then the results are not identical
    """
    result = timestamp()

    finish()

    time.sleep(0.1)

    assert result != timestamp()


def test_free_method(request, bound_class):
    """
    Given I have a bound method
    With I call a function that frees the bind
    And I call the bound method for a second time
    Then the results are not identical
    """
    result = bound_class.timestamp()

    time.sleep(0.1)

    bound_class.finish()

    result2 = bound_class.timestamp()

    assert result != result2

    def fin():
        bound_class.finish()

    request.addfinalizer(fin)


def test_free_on_fail():
    """
    Given I have a bound function
    With I call a function that frees the bind but raises an Exception
    Then the bound functions are still freed
    """
    result = timestamp()

    with pytest.raises(ValueError):
        finish_fail()

    time.sleep(0.1)

    assert result != timestamp()
