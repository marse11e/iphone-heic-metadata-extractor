# Photo Metadata Extractor

Этот скрипт позволяет извлекать метаданные из HEIC-файлов, полученных с устройств iPhone. Он конвертирует HEIC в JPG для удобства работы с метаданными, включая GPS-координаты, данные устройства и информацию о изображении.

## Установка

1. Установите необходимые библиотеки с помощью команды:

   ```bash
   pip install pyheif piexif Pillow geopy
   ```

2. Клонируйте репозиторий:

   ```bash
   git clone git@github.com:marse11e/iphone-heic-metadata-extractor.git
   cd iphone-heic-metadata-extractor
   ```

## Использование

1. Импортируйте класс `PhotoMetadata` и создайте экземпляр, указав путь к вашему HEIC-файлу:

   ```python
   from photo_metadata_extractor import PhotoMetadata

   photo = PhotoMetadata("путь_к_вашему_файлу.HEIC")
   ```

2. Получите различные виды информации о фотографии:

   ```python
   print(photo.device_informations())  # Информация о устройстве
   print(photo.GPS_informations())     # GPS-данные
   print(photo.image_informations())   # Информация об изображении
   ```

3. Получите координаты и адрес местоположения:

   ```python
   print(photo.get_location())          # Координаты местоположения
   print(photo.get_location_address())  # Адрес местоположения
   print(photo.get_location_url())      # Ссылки на карты
   ```

4. Экспортируйте информацию в CSV или текстовый файл:

   ```python
   print(photo.get_csv_informations())  # Экспорт в CSV
   print(photo.get_text_file())         # Экспорт в текстовый файл
   ```

## Дополнительные возможности

- `convert_to_degrees(d, m, s)`: Преобразование координат из градусов, минут и секунд в десятичные градусы.
- `informations_text()`: Получение текстового описания всех данных о фотографии.
- `__str__()`: Вывод информации о классе `PhotoMetadata`.

## Лицензия

Этот проект лицензирован под MIT License - см. файл [LICENSE](LICENSE) для деталей.

## Контакты

- Telegram: [@MarselleNaz](https://t.me/MarselleNaz)
- Instagram: [@marselle.naz](https://instagram.com/marselle.naz)

## Пример фотографии

- [PHOTO HEIC](IMG_8850.HEIC)
<img src='temp/IMG_8850.jpg' />