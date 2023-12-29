from httpx import AsyncClient

from src.application.user.schemas.user import UserCreateDTO


async def test_create_user(
        ac: AsyncClient,
        create_user_schema: UserCreateDTO,
        erase_users):
    response = await ac.post('/users/', json={
        **create_user_schema.model_dump()
    })

    assert response.status_code == 201
    assert response.json().get('username') == create_user_schema.username
    assert response.json().get('name') == create_user_schema.name
    assert response.json().get('email') == create_user_schema.email
    return response.json().get('id')


async def test_get_user(
        ac: AsyncClient,
        create_user_schema: UserCreateDTO,
        erase_users):
    user_id = await test_create_user(ac, create_user_schema, erase_users)
    res = await ac.get(f'/users/{user_id}')
    assert res.status_code == 200
    assert create_user_schema.name == res.json().get('name')
    assert create_user_schema.email == res.json().get('email')
    assert create_user_schema.username == res.json().get('username')


async def test_login(
        ac: AsyncClient,
        create_user_schema: UserCreateDTO,
        erase_users):
    await test_create_user(ac, create_user_schema, erase_users)
    res = await ac.post('/users/login', data={
        'username': create_user_schema.email,
        'password': create_user_schema.password
    })
    assert res.status_code == 200, 'login with email'
    res = await ac.post('/users/login', data={
        'username': create_user_schema.username,
        'password': create_user_schema.password
    })
    assert res.status_code == 200, 'login with username'

