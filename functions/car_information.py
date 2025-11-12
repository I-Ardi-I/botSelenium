import config
from lang.texts import DATA_GET_ERROR, PLACE_NOT_RESERVED, STATUSES


def get_all_auto_info(soup_):   # /list в боте
    try:
        if soup_ is None:
            return DATA_GET_ERROR

        divs = soup_.find_all('div', class_='_4MZlMfg8')

        statuses = []
        dates = []
        plates = []

        for div in divs:
            text = div.get_text(strip=True)
            statuses_var = STATUSES
            if text in statuses_var:  # статус
                statuses.append(text)
            elif ":" in text:  # дата время
                dates.append(text)
            elif config.PLATE_PATTERN.match(text):  # номер авто
                plates.append(text)

        info = ''
        for i in range(min(len(statuses), len(dates), len(plates))):
            info += (f"╔ 🚛 Номер авто: {plates[i]}\n"
                     f"╠ ⌛️ Дата: {dates[i]}\n"
                     f"╚ ⚙️ Статус: {statuses[i]}\n")
            info += '\n'
        return info

    except Exception as ex:
        print(ex)
        return DATA_GET_ERROR


def get_auto_info(soup_, plate_):   # /auto в боте
    try:
        if soup_ is None:
            return DATA_GET_ERROR

        divs = soup_.find_all('div', class_='_4MZlMfg8')

        # списки для хранения данных
        statuses = []
        dates = []
        plates = []

        for div in divs:
            text = div.get_text(strip=True)
            statuses_var = STATUSES
            if text in statuses_var:  # статус
                statuses.append(text)
            elif ":" in text:  # дата время
                dates.append(text)
            elif config.PLATE_PATTERN.match(text.upper()):  # номер авто
                plates.append(text.upper())

        plate_upper = plate_.upper()
        if plate_upper in plates:
            indx = plates.index(plate_upper)
            info = (f"╔ 🚛 Номер авто: {plate_upper}\n"
                    f"╠ ⌛️ Дата: {dates[indx]}\n"
                    f"╚ ⚙️ Статус: {statuses[indx]}\n")
        else:
            info = PLACE_NOT_RESERVED
        return info

    except Exception as ex:
        print(ex)
        return DATA_GET_ERROR
