"""
Photo Metadata Extractor

Этот скрипт позволяет извлекать метаданные из HEIC-файлов, полученных с устройств iPhone. 
Он конвертирует HEIC в JPG для удобства работы с метаданными, 
включая GPS-координаты, данные устройства и информацию о изображении.

Создайте экземпляр, указав путь к вашему HEIC-файлу:

    photo = PhotoMetadata("путь_к_вашему_файлу.HEIC")

    
Получите различные виды информации о фотографии:

   print(photo.device_informations())  # Информация о устройстве
   print(photo.GPS_informations())     # GPS-данные
   print(photo.image_informations())   # Информация об изображении
   

Получите координаты и адрес местоположения:

   print(photo.get_location())          # Координаты местоположения
   print(photo.get_location_address())  # Адрес местоположения
   print(photo.get_location_url())      # Ссылки на карты
   

Экспортируйте информацию в CSV или текстовый файл:

   print(photo.get_csv_informations())  # Экспорт в CSV
   print(photo.get_text_file())         # Экспорт в текстовый файл
   

Дополнительные возможности

- convert_to_degrees(d, m, s): Преобразование координат из градусов, минут и секунд в десятичные градусы.
- informations_text(): Получение текстового описания всех данных о фотографии.
- __str__(): Вывод информации о классе `PhotoMetadata`.


Контакты

- Telegram: https://t.me/MarselleNaz
- Instagram: https://instagram.com/marselle.naz
"""

import os
import csv
import pyheif
import piexif
from PIL import Image
from pathlib import Path
from geopy import Nominatim


def create_folders_if_not_exists():
    folders_to_check = ['temp', 'document']
    
    for folder in folders_to_check:
        if not os.path.exists(folder):
            os.makedirs(folder)


class PhotoMetadata:
    def __init__(self, file: str, *args, **kwargs):
        self.file = file
        self.args = args
        self.kwargs = kwargs

    def __heic_to_jpg_converter(self):
        heif_file = pyheif.read(self.file)
        image = Image.frombytes(
                heif_file.mode,
                heif_file.size,
                heif_file.data,
                "raw",
                heif_file.mode,
                heif_file.stride,
            )

        for metadata in heif_file.metadata or []:
            if metadata['type'] == 'Exif':
                exif_dict = piexif.load(metadata['data'])

        exif_dict['0th'][274] = 0
        exif_bytes = piexif.dump(exif_dict)
        exportName = "temp/" + Path(self.file).stem + '.jpg'
        image.save(exportName, "JPEG", exif=exif_bytes)
        image.close()
    
        return exportName


    def __get_metadata(self):
        metadata = {}
        exif_data = Image.open(self.__heic_to_jpg_converter())._getexif()

        for tag, value in exif_data.items():
            metadata[tag] = value

        return metadata
    
    def convert_to_degrees(self, d: int = None, m: int = None, s: int = None):
        if d and m and s:
            return d + (m / 60.0) + (s / 3600.0)
        else:
            return None
    
    def GPS_informations(self) -> dict:
        metadata = self.__get_metadata()
        gps_data: dict = metadata.get(34853, None) or metadata.get(34851, None)

        if gps_data is None:
            return None
        
        latitude = gps_data.get(2, None)
        longitude = gps_data.get(4, None)
        date = gps_data.get(29, None).split(":") if gps_data.get(29, None) else None, None, None

        data_dict = {
            'latitude_direction': gps_data.get(1, None),
            'latitude': self.convert_to_degrees(*latitude if latitude else None),
            'longitude_direction': gps_data.get(3, None),
            'longitude': self.convert_to_degrees(*longitude if longitude else None),
            'altitude': gps_data.get(5, None),
            'altitude_accuracy': gps_data.get(6, None),
            'time_fixed': gps_data.get(7, None),
            'quality_code': gps_data.get(12, None),
            'accuracy': gps_data.get(13, None),
            'orientation1': gps_data.get(16, None),
            'speed1': gps_data.get(17, None),
            'orientation2': gps_data.get(23, None),
            'speed2': gps_data.get(24, None),
            'capture_date': f'{date[0]}.{date[1]}.{date[2]}',
            'magnetic_declination': gps_data.get(31, None)
        }

        return data_dict
    
    def get_location(self) -> tuple[str]:
        metadata = self.__get_metadata()
        location_data = metadata.get(34853, None) or metadata.get(34851, None)
        latitude_components = location_data[2]
        longitude_components = location_data[4]

        if latitude_components and longitude_components:
            latitude = self.convert_to_degrees(*latitude_components)
            longitude = self.convert_to_degrees(*longitude_components)

            return latitude, longitude
        else:
            return None, None
    
    def get_location_address(self) -> str:
        geolocator = Nominatim(user_agent="my_geolocator")
        location = geolocator.reverse(self.get_location(), language="ru")

        if location is None:
            return "Адрес не найден."
        else:
            return location.address
        
    def get_location_url(self) -> tuple[str]:
        location = self.get_location()
        latitude = location[0]
        longitude = location[1]

        google_maps = f"https://www.google.kz/maps/place/{latitude},{longitude}",
        twogis = f"https://2gis.kz/almaty/search/{latitude}%2C{longitude}",
        yandex_maps = f"https://yandex.kz/maps/162/almaty/?ll=76.839462%2C43.239393&mode=search&sll={longitude}%2C{latitude}&text={latitude}%2C{longitude}&z=18",
        
        return google_maps, twogis, yandex_maps

    def device_informations(self) -> dict:
        metadata = self.__get_metadata()
        data_dict = {
            "device_model": metadata.get(316, None),
            "model": metadata.get(272, None),
            "firmware_version": metadata.get(305, None),
            "shutter_speed": metadata.get(37377, None),
            "camera_manufacturer": metadata.get(42035, None),
            "lens_info": metadata.get(42036, None),
        }
        return data_dict
    
    def image_informations(self) -> dict:
        metadata = self.__get_metadata()
        data_dict = {
            "image_width": metadata.get(322, None),
            "image_height": metadata.get(323, None),
            "orientation": metadata.get(296, None),
            "exif_offset": metadata.get(34665, None),
            "manufacturer": metadata.get(271, None),
            "compression": metadata.get(274, None),
            "date_and_time": metadata.get(306, None),
            "x_resolution": metadata.get(282, None),
            "y_resolution": metadata.get(283, None),
            "exif_version": metadata.get(36864, None),
            "aperture_value": metadata.get(37378, None),
            "date_and_time_original": metadata.get(36867, None),
            "date_and_time_digitized": metadata.get(36868, None),
            "iso_speed_rating": metadata.get(37379, None),
            "brightness_value": metadata.get(37380, None),
            "exposure_mode": metadata.get(37383, None),
            "color_space": metadata.get(40961, None),
            "flash": metadata.get(37385, None),
            "focal_length": metadata.get(37386, None),
            "pixel_x_dimension": metadata.get(40962, None),
            "pixel_y_dimension": metadata.get(40963, None),
            "contrast": metadata.get(41989, None),
            "offset_time": metadata.get(36880, None),
            "offset_time_original": metadata.get(37521, None),
            "offset_time_digitized": metadata.get(37522, None),
            "exposure_time": metadata.get(33434, None),
            "f_number": metadata.get(33437, None),
            "scene_type": metadata.get(41729, None),
            "exposure_program": metadata.get(34850, None),
            "iso_rating": metadata.get(34855, None),
            "custom_rendered": metadata.get(41986, None),
            "exposure_mode": metadata.get(41987, None),
            "exposure_bias": metadata.get(42034, None),
        }
        return data_dict

    def informations(self) -> dict:
        data_dict = {}
        data_dict.update(self.GPS_informations())
        data_dict.update(self.device_informations())
        data_dict.update(self.image_informations())
        return data_dict

    def informations_text(self) -> str:
        latitude = ""
        longitude = ""
        text = ""
        for key, value in self.informations().items():
            if key == 'latitude':
                latitude = value
            if key == 'longitude':
                longitude = value
            
            k_str = str(key).replace('_', ' ').title().ljust(30, " ")
            value_str = str(value).title()
            text += f"{k_str} | ->\t {value_str}\n"

        urls = {
            "google_maps": f"https://www.google.kz/maps/place/{latitude},{longitude}",
            "twogis": f"https://2gis.kz/almaty/search/{latitude}%2C{longitude}",
            "yandex_maps": f"https://yandex.kz/maps/162/almaty/?ll=76.839462%2C43.239393&mode=search&sll={longitude}%2C{latitude}&text={latitude}%2C{longitude}&z=18",
        }

        for key, value in urls.items():
            k_str = str(key).replace('_', ' ').title().ljust(30, " ")
            value_str = str(value)
            text += f"{k_str} | ->\t {value_str}\n"

        return text
    
    def get_csv_informations(self) -> Path:
        with open(f"document/{self.file.split('.')[0]}.csv", 'w', newline='') as csvfile:
            fieldnames = ['Ключи', 'Значения']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for key, value in self.informations().items():
                k_str = str(key).replace('_', ' ').title().ljust(30, " ")
                value_str = str(value).title()
                writer.writerow({'Ключи': k_str, 'Значения': value_str})
        return f"document/{self.file.split('.')[0]}.csv"

    def get_text_file(self) -> Path:
        with open(f"document/{self.file.split('.')[0]}.txt", 'w') as text_file:
            text_file.write(self.informations_text())
        return f"document/{self.file.split('.')[0]}.txt"

    def __str__(self) -> str:
        return f"PhotoMetadata('{self.file}')\nat: {self.__dir__()}"


def main():
    create_folders_if_not_exists()

    photo = PhotoMetadata("IMG_8850.HEIC")

    # print(photo.device_informations())
    # print(photo.GPS_informations())
    # print(photo.image_informations())

    # print(photo.get_location())
    # print(photo.get_location_address())
    # print(photo.get_location_url())
    
    # print(photo.informations())
    # print(photo.informations_text())
    print(photo.get_csv_informations())
    print(photo.get_text_file())


if __name__ == "__main__":
    main()