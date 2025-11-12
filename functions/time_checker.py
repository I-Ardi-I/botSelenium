import asyncio
import requests
import bot_init
from lang.texts import NO_PLACES
from config import ADMIN_CHAT_ID
from config import CHECK_DATES_JSON
from datetime import datetime, timedelta
from functions.authorization import get_random_chrome_user_agent


async def next_two_weeks():
    current_date = datetime.now()
    date_list_ = []
    for i in range(1, 15):
        next_date = current_date + timedelta(days=i)
        formatted_next_date = str(next_date.strftime('%Y-%m-%d')).replace('-', '')
        date_list_.append(formatted_next_date)
    return date_list_


async def check_dates():
    date_ = await next_two_weeks()
    result = ''

    for i in date_:
        url = f'{CHECK_DATES_JSON}{i}/list.json'

        headers = {
            'User-Agent': get_random_chrome_user_agent()
        }
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()

            for item in data:
                status = "свободно" if item['free'] else "занято"
                if status == 'свободно':
                    from_time = item['from']
                    to_time = item['to']
                    result += f"С {from_time} до {to_time} - свободно\n"
            # print(f'{result} - {datetime.now()}')
            if 'свободно' in result:
                return result
        except requests.exceptions.HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'Other error occurred: {err}')
        return NO_PLACES


async def periodic_check_dates():
    while True:
        info = await check_dates()  # в среднем 0.24 секунды на выполнение
        if info != NO_PLACES:
            await bot_init.bot.send_message(ADMIN_CHAT_ID, info)
        await asyncio.sleep(5)
