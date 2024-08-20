def test_create_movie(client, app):
    # Primero, obtener token de autenticación
    client.post('/auth/register', json={
        'username': 'testuser',
        'password': 'testpassword'
    })
    login_response = client.post('/auth/login', json={
        'username': 'testuser',
        'password': 'testpassword'
    })
    token = login_response.get_json()['access_token']
    
    # Crear una película
    response = client.post('/movie/', 
                           json={
                               'name': 'Test Movie',
                               'actors': 'Actor 1, Actor 2',
                               'director': 'Test Director',
                               'genre': 'Drama',
                               'rating': '90%',
                               'realeseDate': '2024-12-12'
                           },
                           headers={'Authorization': f'Bearer {token}'})
    
    assert response.status_code == 200
    assert response.get_json()['name'] == 'Test Movie'

def test_get_movies(client, app):
    # Crear una película para probar
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
                    'rating': '90%',
                    'realeseDate': '2024-12-12'
                },
                headers={'Authorization': f'Bearer {token}'})
    
    # Obtener todas las películas
    response = client.get('/movie/', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    assert len(response.get_json()) > 0
