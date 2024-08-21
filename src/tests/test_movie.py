def test_create_movie(client, app):
    # obtener token de auth
    client.post('/auth/register', json={
        'username': 'testuser',
        'password': 'testpassword'
    })
    login_response = client.post('/auth/login', json={
        'username': 'testuser',
        'password': 'testpassword'
    })
    token = login_response.get_json()['access_token']
    
    # crear una película para el test
    response = client.post('/movie/', 
                           json={
                               'name': 'Test Movie',
                               'actors': 'Actor 1, Actor 2',
                               'director': 'Test Director',
                               'genre': 'Drama',
                               'rating': '8',
                               'realeseDate': '2024-12-12'
                           },
                           headers={'Authorization': f'Bearer {token}'})
    
    assert response.status_code == 200
    assert response.get_json()['name'] == 'Test Movie'

def test_get_movies(client, app):
    client.post('/auth/register', json={
        'username': 'testuser',
        'password': 'testpassword'
    })
    login_response = client.post('/auth/login', json={
        'username': 'testuser',
        'password': 'testpassword'
    })
    token = login_response.get_json()['access_token']

    client.post('/movie/', 
                json={
                    'name': 'Test Movie',
                    'actors': 'Actor 1, Actor 2',
                    'director': 'Test Director',
                    'genre': 'Drama',
                    'rating': '8',
                    'realeseDate': '2024-12-12'
                },
                headers={'Authorization': f'Bearer {token}'})
    
    # obtener todas las películas
    response = client.get('/movie/', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    assert len(response.get_json()) > 0
