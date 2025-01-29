import segno
import base64
from io import BytesIO

def generate_qr_code(bid):
    info = f"Заявка №{bid.id}\nКомментарий:{bid.comment or 'нету'}\n"

    info += f"Добавить животное:\nИмя:{bid.animal.name}\nГруппа:{bid.animal.group}\n"

    info += f"В следующие периоды:\n"

    for index, bid_item in enumerate(bid.periods.all()):
        info += f"{index+1}. {bid_item.period.name.capitalize()}\n"

    info += f"Дата создания: {bid.created_at}\n"
    info += f"Дата завершения: {bid.finished_at if bid.finished_at else '-'}"

    # Генерация QR-кода
    qr = segno.make(info)
    buffer = BytesIO()
    qr.save(buffer, kind='png')
    buffer.seek(0)

    # Конвертация изображения в base64
    qr_image_base64 = base64.b64encode(buffer.read()).decode('utf-8')

    return qr_image_base64