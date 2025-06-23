import xml.etree.ElementTree as ET
from PIL import Image, ImageDraw, ImageFont
import os
import hashlib # Для получения стабильного цвета для метки

def get_color_for_label(label_text, available_colors):
    """
    Генерирует детерминированный цвет для данной метки на основе её текста.
    Это гарантирует, что одна и та же метка всегда будет иметь один и тот же цвет.
    """
    hash_object = hashlib.md5(label_text.encode())
    hex_dig = hash_object.hexdigest()
    hash_int = int(hex_dig, 16)
    color_index = hash_int % len(available_colors)
    return available_colors[color_index]

def visualize_annotations(xml_file_path, images_dir_path, output_dir_path):
    """
    Парсит XML-файл аннотаций CVAT, находит соответствующие изображения
    и рисует на них bounding box'ы с подписями разных цветов. Сохраняет результат.

    Args:
        xml_file_path (str): Путь к файлу annotations.xml.
        images_dir_path (str): Путь к директории с исходными изображениями.
        output_dir_path (str): Путь к директории для сохранения обработанных изображений.
    """
    if not os.path.exists(output_dir_path):
        os.makedirs(output_dir_path)

    try:
        tree = ET.parse(xml_file_path)
        root = tree.getroot()
    except ET.ParseError as e:
        print(f"Error parsing XML file: {e}")
        return
    except FileNotFoundError:
        print(f"XML file not found: {xml_file_path}")
        return

    # --- Настройка цветов и шрифта ---
    # (Red, Green, Blue, Yellow, Purple, Orange, Cyan, Magenta, Lime, Pink, Teal, Lavender, Brown, Beige, Maroon, Olive)
    available_colors = [
        (255, 0, 0), (0, 128, 0), (0, 0, 255), (255, 255, 0), (128, 0, 128),
        (255, 165, 0), (0, 255, 255), (255, 0, 255), (50, 205, 50), (255, 105, 180),
        (0, 128, 128), (230, 230, 250), (165, 42, 42), (245, 245, 220), (128, 0, 0), (128, 128, 0)
    ]
    
    font_size = 60
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except IOError:
        print(f"Font 'arial.ttf' not found. Using default PIL font (อาจดูไม่สวยงาม).")
        font = ImageFont.load_default()

    for image_tag in root.findall('image'):
        image_id = image_tag.get('id')
        image_name = image_tag.get('name')
       
        potential_image_path = os.path.join(images_dir_path, os.path.basename(image_name))

        if not os.path.exists(potential_image_path):
            print(f"Image file not found for {image_name} at {potential_image_path}. Skipping.")
            continue

        try:
            img = Image.open(potential_image_path).convert("RGB")
            draw = ImageDraw.Draw(img)
        except FileNotFoundError:
            print(f"Image file not found: {potential_image_path}")
            continue
        except Exception as e:
            print(f"Error opening image {potential_image_path}: {e}")
            continue

        for box_tag in image_tag.findall('box'):
            label = box_tag.get('label')
            xtl = float(box_tag.get('xtl'))
            ytl = float(box_tag.get('ytl'))
            xbr = float(box_tag.get('xbr'))
            ybr = float(box_tag.get('ybr'))

            # Получаем цвет для текущей метки
            box_color = get_color_for_label(label, available_colors)

            # Рисуем прямоугольник
            draw.rectangle([(xtl, ytl), (xbr, ybr)], outline=box_color, width=3)
            
            # Добавляем текст метки
            # Позиционируем текст немного выше и левее bounding box'а
            # или внутри, если сверху нет места
            text_y_position = ytl - font_size - 4 # 4 - небольшой отступ
            if text_y_position < 0: # Если текст уходит за верхний край картинки
                text_y_position = ytl + 4 # Рисуем внутри рамки, сверху
            
            text_x_position = xtl + 4

            try:
                draw.text((text_x_position, text_y_position), label, fill=box_color, font=font)
            except Exception as e:
                print(f"Could not draw text for label {label} on {image_name}: {e}")

        # Сохраняем изображение с аннотациями
        output_image_name = f"annotated_{os.path.basename(image_name)}"
        output_image_path = os.path.join(output_dir_path, output_image_name)
        try:
            img.save(output_image_path)
            print(f"Saved annotated image: {output_image_path}")
        except Exception as e:
            print(f"Error saving image {output_image_path}: {e}")

if __name__ == "__main__":
    
    # --- НАСТРОЙКИ ---
    cvat_export_dir = "./"  

    xml_file = os.path.join(cvat_export_dir, "annotations.xml")
    
    images_folder = os.path.join(cvat_export_dir, "images") 

    output_folder = os.path.join(cvat_export_dir, "visualized_annotations_color")
    # --- КОНЕЦ НАСТРОЕК ---

    if not os.path.isdir(cvat_export_dir):
        print(f"Ошибка: Директория экспорта CVAT '{cvat_export_dir}' не найдена.")
        print("Пожалуйста, укажи правильный путь к распакованной папке с экспортом из CVAT в переменной 'cvat_export_dir'.")
    elif not os.path.isfile(xml_file):
        print(f"Ошибка: Файл аннотаций '{xml_file}' не найден.")
        print("Убедись, что файл annotations.xml находится в указанной директории экспорта.")
    elif not os.path.isdir(images_folder):
        print(f"Ошибка: Директория с изображениями '{images_folder}' не найдена.")
        print("Убедись, что изображения находятся в указанной директории (переменная 'images_folder').")
    else:
        visualize_annotations(xml_file, images_folder, output_folder)
        print(f"Визуализация завершена. Результаты в папке: {output_folder}")