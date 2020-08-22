import pytest


@pytest.mark.parametrize("n, output",
                         [
                             [1, 1],
                             [1, 1],
                             [2, 2],
                             [3, 3],
                             [5, 5],
                             [8, 8],
                         ])
def test_simple(n,output):
    assert n == output

def test_create_new_user(user):
    user.create({'first_name': 'John', 'last_name': 'Doe', 'email': 'john.doe@gmail.com', 'password': 'root'})
    query = f'SELECT * FROM User where email="john.doe@gmail.com"'
    result = user.conn.execute(query).fetchone()
    assert result['first_name'] == 'John'
    assert result['last_name'] == 'Doe'
    assert result['email'] == 'john.doe@gmail.com'
