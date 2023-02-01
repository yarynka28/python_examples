import pytest

@pytest.fixture(scope='function')
def some_resource(request):
    stuff_i_setup = ["I setup"]

    def some_teardown():
        stuff_i_setup[0] += " ... but now I'm torn down..."
        print(stuff_i_setup[0])
    request.addfinalizer(some_teardown)

    return stuff_i_setup[0]

def test_1_that_needs_resource(some_resource):
    print(some_resource + "... and now I'm testing things...")