import asyncio

import httpx

from exceptions.obis import ObisLoginError

__all__ = ('login_to_obis',)


async def login_to_obis(*, login: str, password: str) -> str:
    url = 'http://obis.manas.edu.kg/index.php'
    request_data = {
        'frm_kullanici': login,
        'frm_sifre': password,
    }
    async with httpx.AsyncClient() as http_client:
        try:
            response = await http_client.post(url, data=request_data)
        except httpx.HTTPError:
            raise ObisLoginError('Ошибка соедниения с OBIS\'ом')

        try:
            session_id = http_client.cookies['PHPSESSID']
        except KeyError:
            raise ObisLoginError(
                'Не удалось авторизоваться в OBIS\'е.'
                ' Проверьте логин и пароль.'
            )

    if 'Cep Telefon' not in response.text:
        raise ObisLoginError(
            'Не удалось авторизоваться в OBIS\'е.'
            ' Проверьте логин и пароль.'
        )

    return f'{url}?page=bilgiler&PHPSESSID={session_id}'
