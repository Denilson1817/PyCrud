def test_register_user(client):
    response = client.post('/auth/register', json={
        'username': 'testuser',
        'password': 'testpassword'
    })
    assert response.status_code == 201
    assert response.get_json()['msg'] == 'User created successfully'

def test_login_user(client):
    client.post('/auth/register', json={
        'username': 'testuser',
        'password': 'testpassword'
    })
    response = client.post('/auth/login', json={
        'username': 'testuser',
        'password': 'testpassword'
    })
    assert response.status_code == 200
    assert 'access_token' in response.get_json()
