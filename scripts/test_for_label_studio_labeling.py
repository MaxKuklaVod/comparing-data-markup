import json
import cv2
import os

json_file_path = os.path.expanduser("label_studio_data/export/project-1-at-2025-06-19-14-54-b0c66fa7.json") 
base_data_path_on_host = os.path.join(os.path.expanduser("~"), "label_studio_data")

# --- Проверка существования файлов ---
if not os.path.isfile(json_file_path):
    print(f"Ошибка: JSON файл не найден по пути: {json_file_path}")
    exit()

if not os.path.isdir(base_data_path_on_host):
    print(f"Ошибка: Базовая папка данных Label Studio '{base_data_path_on_host}' не найдена.")
    script_dir = os.path.dirname(os.path.abspath(__file__))
    alt_base_path = os.path.join(script_dir, "label_studio_data")
    if os.path.isdir(alt_base_path):
        base_data_path_on_host = alt_base_path
        print(f"Найдена альтернативная базовая папка: {base_data_path_on_host}")
    else:
        print(f"Ошибка: Альтернативная базовая папка данных Label Studio '{alt_base_path}' также не найдена.")
        exit()
# --- Конец проверки ---

# Максимальные размеры для отображаемого окна
MAX_DISPLAY_WIDTH = 1280
MAX_DISPLAY_HEIGHT = 720

WINDOW_NAME = "Label Studio Annotation Viewer"

with open(json_file_path, 'r', encoding='utf-8') as f:
    tasks = json.load(f)

print(f"Загружено {len(tasks)} задач из JSON.")

for task_index, task in enumerate(tasks):
    task_id_str = str(task.get('id', f'index {task_index}'))
    print(f"\nОбработка задачи ID: {task_id_str}")

    if 'data' not in task or 'image' not in task['data']:
        print(f"  Пропуск задачи {task_id_str}: поле 'data.image' не найдено.")
        continue
        
    image_path_from_json = task['data']['image']
    print(f"  Путь из JSON: {image_path_from_json}")
    
    full_image_path_on_host = None
    if image_path_from_json.startswith('/data/upload/'):
        path_suffix = image_path_from_json[len('/data/'):].lstrip('/') 
        path_suffix = path_suffix.replace('/', os.sep)
        full_image_path_on_host = os.path.join(base_data_path_on_host, "media", path_suffix)
    else:
        print(f"  Предупреждение: Нестандартный формат пути к изображению в JSON: {image_path_from_json}.")
        continue
    
    print(f"  Полный путь на хосте: {full_image_path_on_host}")

    if not os.path.exists(full_image_path_on_host):
        print(f"  Изображение не найдено на хосте: {full_image_path_on_host}")
        continue

    original_image = cv2.imread(full_image_path_on_host)
    if original_image is None:
        print(f"  Не удалось прочитать изображение: {full_image_path_on_host}")
        continue
    print(f"  Изображение {os.path.basename(full_image_path_on_host)} успешно загружено (ориг. размер: {original_image.shape[1]}x{original_image.shape[0]}).")

    display_image = original_image.copy()
    
    img_height, img_width = original_image.shape[:2]

    annotations_key = None
    if 'annotations' in task and task['annotations']:
        annotations_key = 'annotations'
    
    if annotations_key:
        annotation_data_list = task[annotations_key]
        if annotation_data_list:
            annotation_data = annotation_data_list[0] 
            if 'result' in annotation_data and annotation_data['result']:
                print(f"  Найдено {len(annotation_data['result'])} результатов в аннотации.")
                for res_idx, result in enumerate(annotation_data['result']):
                    if result.get('type') == 'rectanglelabels':
                        value = result.get('value')
                        if not value or not all(k in value for k in ['x', 'y', 'width', 'height', 'rectanglelabels']):
                            print(f"    Пропуск результата {res_idx}: отсутствуют необходимые ключи в 'value'.")
                            continue

                        x_percent = value['x']
                        y_percent = value['y']
                        width_percent = value['width']
                        height_percent = value['height']
                        labels = value['rectanglelabels'] 

                        x1 = int(x_percent / 100.0 * img_width)
                        y1 = int(y_percent / 100.0 * img_height)
                        w = int(width_percent / 100.0 * img_width)
                        h = int(height_percent / 100.0 * img_height)
                        x2 = x1 + w
                        y2 = y1 + h

                        label_text = ", ".join(labels)
                        color = (0, 255, 0) 
                        
                        if any(l.lower() == "cat" for l in labels):
                            color = (255, 0, 0) 
                        
                        elif any(l.lower() == "cats" for l in labels):
                            color = (0, 0, 255) 
                        
                        print(f"    Рисуем рамку на display_image: {label_text} at [{x1},{y1},{w},{h}] (относительно оригинала)")
                        cv2.rectangle(display_image, (x1, y1), (x2, y2), color, 2) 
                        font_scale = min(img_width, img_height) / 1000.0
                        line_thickness = max(1, int(min(img_width, img_height) / 500.0))
                        
                        cv2.putText(display_image, label_text, (x1, y1 - 10 if y1 - 10 > 10 else y1 + int(20*font_scale)), 
                                    cv2.FONT_HERSHEY_SIMPLEX, font_scale, color, line_thickness)
            else:
                print("  В аннотации нет поля 'result' или оно пустое.")
    else:
        print("  В задаче нет ключа 'annotations'.")

    h_orig, w_orig = display_image.shape[:2]
    scale_w = MAX_DISPLAY_WIDTH / w_orig
    scale_h = MAX_DISPLAY_HEIGHT / h_orig
    scale = min(scale_w, scale_h)

    if scale < 1:
        new_w = int(w_orig * scale)
        new_h = int(h_orig * scale)
        resized_display_image = cv2.resize(display_image, (new_w, new_h), interpolation=cv2.INTER_AREA)
    else:
        resized_display_image = display_image

    current_window_name = f"{WINDOW_NAME} - Task: {task_id_str} ({os.path.basename(full_image_path_on_host)})"
    cv2.imshow(current_window_name, resized_display_image)
    key = cv2.waitKey(0) 
    
    try:
        cv2.destroyWindow(current_window_name)
    except cv2.error as e:
        print(f"  Не удалось закрыть окно '{current_window_name}': {e}")

    if key == 27:
        print("Выход по нажатию ESC.")
        break

cv2.destroyAllWindows()
print("\nПросмотр завершен.")