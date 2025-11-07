import cloudinary
import cloudinary.uploader
import requests
from pathlib import Path

cloudinary.config(
    cloud_name = "XXXXX",
    api_key = "XXXXXX",
    api_secret = "XXXXXXX",
    secure=True)

def upscale_image(image_path, output_path, scale_factor=2.0):
        # Загружаем и увеличиваем изображение
        result = cloudinary.uploader.upload(
                    image_path,
                    transformation=[
                        {
                            "width": scale_factor,
                            "crop": "scale",
                            "quality": "auto:good"
                        }])
        # Скачиваем и сохраняем результат
        response = requests.get(result['url'])
        if response.status_code == 200:
            with open(output_path, 'wb') as f:
                f.write(response.content)

def process_all_images(source_folder="source", output_folder="output", scale_factor=2.0):
    supported_formats = {'.jpg', '.jpeg', '.png', '.JPG', '.JPEG', '.PNG'}
    # Получаем список файлов
    image_files = []
    for file_path in Path(source_folder).iterdir():
        if file_path.is_file() and file_path.suffix in supported_formats:
            image_files.append(file_path)

    # Обрабатываем каждое изображение
    successful = 0
    for image_path in image_files:
        # Создаем имя выходного файла с буквой "u" в начале
        output_filename = "u" + image_path.name
        output_path = Path(output_folder) / output_filename

        if upscale_image(str(image_path), str(output_path), scale_factor):
            successful += 1

    print(f"🎉 Обработка завершена! Успешно: {successful}/{len(image_files)}")


if __name__ == "__main__":
    process_all_images(
        source_folder="source",
        output_folder="output",
        scale_factor=2.0
    )
