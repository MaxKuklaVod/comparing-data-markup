Отличный отчет! Давайте сделаем его еще более универсальным и понятным для пользователей Linux и Windows, с акцентом на Docker.

---

# Отчет по развертыванию, использованию и проверке Label Studio (с использованием Docker)

Этот документ описывает процесс установки, настройки, использования и проверки Label Studio для разметки данных. Инструкции адаптированы для пользователей **Windows** и **Linux** и предполагают установку исключительно через **Docker**.

## 1. Развертывание Label Studio

### 1.1. Предварительные требования
*   **Установленный Docker:**
    *   **Windows/macOS:** Docker Desktop.
    *   **Linux:** Docker Engine. Убедитесь, что ваш пользователь добавлен в группу `docker` или используйте `sudo` для команд Docker.
*   **Доступ в Интернет:** Необходим для скачивания Docker-образа Label Studio.
*   **Python 3.x (опционально, для скрипта проверки):** С установленными библиотеками `opencv-python` и `numpy`. Установить можно командой:
    ```bash
    pip install opencv-python numpy
    ```

### 1.2. Выбор способа развертывания
Для локального развертывания с сохранением данных используется запуск Docker-контейнера с монтированием тома (bind mount). Этот метод обеспечивает:
*   **Персистентность данных:** Ваши проекты, данные и конфигурации сохранятся между перезапусками контейнера.
*   **Прямой доступ к файлам:** Вы сможете легко получить доступ к данным Label Studio на вашем компьютере.

### 1.3. Шаги развертывания

1.  **Создание локальной директории для данных Label Studio:**
    Создайте на вашем компьютере директорию, где будут храниться все данные Label Studio. **Запомните этот путь, он понадобится на следующем шаге.**

    *   **Для Windows (в PowerShell):**
        Замените `C:\путь\к\вашей\папке` на реальный путь. Например, `C:\Users\YourUser\Documents\label_studio_projects`.
        ```powershell
        mkdir C:\путь\к\вашей\папке\label_studio_data
        # Пример:
        # mkdir C:\Users\maxku\Desktop\comparing-data-markup\label_studio_data
        ```
        Или создайте папку `label_studio_data` через Проводник Windows в выбранном вами месте.

    *   **Для Linux (в терминале):**
        Замените `/путь/к/вашей/папке` на реальный путь. Например, `/home/youruser/label_studio_projects`.
        ```bash
        mkdir -p /путь/к/вашей/папке/label_studio_data
        # Пример:
        # mkdir -p ~/projects/label_studio_data
        ```

2.  **Запуск контейнера Label Studio:**
    Откройте терминал (PowerShell для Windows, Bash/терминал для Linux) и выполните команду, соответствующую вашей ОС.

    *   **Для Windows (в PowerShell):**
        Замените `C:\путь\к\вашей\папке\label_studio_data` на путь, который вы создали на шаге 1.
        ```powershell
        docker run -d -p 8080:8080 -v C:\путь\к\вашей\папке\label_studio_data:/label-studio/data --name label-studio-container heartexlabs/label-studio
        # Пример из оригинального отчета:
        # docker run -d -p 8080:8080 -v C:\Users\maxku\Desktop\comparing-data-markup\label_studio_data:/label-studio/data --name label-studio-container heartexlabs/label-studio
        ```

    *   **Для Linux (в терминале):**
        Замените `/путь/к/вашей/папке/label_studio_data` на путь, который вы создали на шаге 1.
        ```bash
        docker run -d -p 8080:8080 -v /путь/к/вашей/папке/label_studio_data:/label-studio/data --name label-studio-container heartexlabs/label-studio
        # Пример:
        # docker run -d -p 8080:8080 -v ~/projects/label_studio_data:/label-studio/data --name label-studio-container heartexlabs/label-studio
        ```

    **Разбор команды:**
    *   `docker run`: Запуск нового контейнера.
    *   `-d`: Запуск в фоновом (detached) режиме.
    *   `-p 8080:8080`: Проброс порта 8080 вашего компьютера (хоста) на порт 8080 контейнера.
    *   `-v [ПУТЬ_НА_ХОСТЕ]:/label-studio/data`: Монтирование тома.
        *   `[ПУТЬ_НА_ХОСТЕ]`: Полный путь к созданной вами директории (`label_studio_data`) на вашем компьютере.
        *   `:/label-studio/data`: Путь внутри контейнера, где Label Studio хранит свои данные. **Эту часть не изменяйте.**
    *   `--name label-studio-container`: Присвоение имени контейнеру для удобства управления (например, для остановки: `docker stop label-studio-container`).
    *   `heartexlabs/label-studio`: Имя официального Docker-образа Label Studio.

3.  **Проверка статуса контейнера:**
    Убедитесь, что контейнер успешно запущен.
    ```bash
    docker ps
    ```
    Вы должны увидеть контейнер `label-studio-container` со статусом `Up`.

4.  **Доступ к Label Studio и создание аккаунта:**
    Откройте веб-браузер и перейдите по адресу `http://localhost:8080`.
    При первом входе вам будет предложено создать аккаунт администратора. Заполните форму и войдите в систему.

### 1.4. Структура хранения данных на хосте
После запуска Label Studio и работы с проектами (например, импорта данных), в созданной вами директории (например, `C:\путь\к\вашей\папке\label_studio_data` или `/путь/к/вашей/папке/label_studio_data`) будет сформирована структура, подобная этой:
```
[ВАША_ДИРЕКТОРИЯ_НА_ХОСТЕ]/label_studio_data/
├── media/
│   └── upload/
│       └── 1/  # PROJECT_ID (идентификатор проекта)
│           ├── example-image1.jpg
│           └── ... (другие загруженные файлы)
├── export/
│   └── project-1-at-....json # Экспортированные аннотации
└── label_studio.sqlite3      # База данных Label Studio (конфигурации, проекты и т.д.)
└── config.json               # Конфигурационные файлы
... (другие файлы и папки)
```
**Важно:** Путь к загруженным файлам внутри Label Studio (например, в экспортированном JSON) будет начинаться с `/data/upload/...`. При доступе к этим файлам с вашего хост-компьютера, вам нужно будет сопоставить этот путь с вашей локальной директорией: `[ВАША_ДИРЕКТОРИЯ_НА_ХОСТЕ]/label_studio_data/media/upload/...`.

### 1.5. Сложности и решения при развертывании и настройке

*   **Проблема с отображением изображений в интерфейсе разметки (часто встречается при первом запуске):**
    *   **Симптом:** Ошибка "There was an issue loading URL from $undefined$ value" (или подобная) при попытке открыть изображение для разметки.
    *   **Причина:** Некорректное значение переменной для данных в XML-конфигурации интерфейса разметки для тега, отображающего данные (например, `<Image>`). По умолчанию может стоять `$undefined$` или некорректное имя переменной.
    *   **Решение:**
        1.  В Label Studio, откройте ваш проект.
        2.  Перейдите в "Settings" (Настройки) -> "Labeling Interface" (Интерфейс разметки).
        3.  На вкладке "Code" (Код) найдите тег, отвечающий за отображение ваших данных (например, `<Image name="image" value="$image"/>`).
        4.  Убедитесь, что атрибут `value` (или аналогичный, зависящий от типа данных) установлен в `$[имя_поля_с_данными]`. По умолчанию для загруженных файлов имя поля часто `image` (для изображений), `text` (для текста), `audio` (для аудио). Если вы импортировали JSON с кастомными ключами, используйте ваш ключ. Например, если ваши данные хранятся под ключом `my_image_url`, то должно быть `value="$my_image_url"`. Для стандартной загрузки файлов обычно достаточно `value="$image"`.

## 2. Тестовая разметка

### 2.1. Создание проекта
*   В интерфейсе Label Studio нажмите "Create Project".
*   Введите имя проекта, например, `Cat Detection Test`.
*   Цель проекта: разметка изображений для задачи детекции объектов (выделение прямоугольниками).

### 2.2. Подготовка и импорт датасета
*   **Данные:** Было подготовлено 14 изображений кошек.
*   **Источник:** Изображения были скачаны с ресурса Pexels.com.
*   **Формат:** `.jpg`.
*   **Импорт:**
    1.  В созданном проекте нажмите кнопку "Import".
    2.  Выберите метод "File Upload".
    3.  Перетащите или выберите файлы изображений для загрузки.

### 2.3. Настройка интерфейса разметки
Для задачи детекции объектов (bounding boxes) используется XML-конфигурация.
1.  В проекте перейдите в "Settings" -> "Labeling Interface".
2.  На вкладке "Code" вставьте или модифицируйте XML. Пример для детекции кошек:
    ```xml
    <View>
      <Image name="image" value="$image"/>
      <RectangleLabels name="label" toName="image">
        <Label value="Cat" background="blue"/>
        <Label value="Cats" background="green"/> 
      </RectangleLabels>
    </View>
    ```
    *   `<Image name="image" value="$image"/>`: Отображает изображение. `value="$image"` означает, что данные для изображения берутся из поля `image` (стандартное для загруженных файлов).
    *   `<RectangleLabels name="label" toName="image">`: Определяет инструмент для рисования прямоугольников (`RectangleLabels`) на элементе с именем `image`.
    *   `<Label value="Cat" background="blue"/>`: Определяет метку "Cat" с синим цветом.
    *   `<Label value="Cats" background="green"/>`: Определяет метку "Cats" (для группы кошек) с зеленым цветом.
3.  Нажмите "Save".

### 2.4. Выполнение разметки
*   Вернитесь на главную страницу проекта (кликнув по его имени вверху или через "Data Manager").
*   Нажмите "Label All Tasks" или выбирайте задачи по одной.
*   Для каждого изображения:
    1.  Выберите инструмент "Rectangle" (Прямоугольник).
    2.  Выберите нужную метку ("Cat" или "Cats").
    3.  Нарисуйте прямоугольник вокруг объекта.
    4.  Нажмите "Submit" (Отправить) для сохранения разметки и перехода к следующей задаче.
*   Разметьте все 14 изображений.

## 3. Экспорт и проверка разметки

### 3.1. Экспорт данных
*   После завершения разметки, на странице проекта нажмите кнопку "Export".
*   Выберите формат экспорта. **JSON** является наиболее полным и часто используемым.
*   Файл с аннотациями будет скачан на ваш компьютер.
*   Пример структуры экспортированного JSON для одной задачи (фрагмент):
    ```json
    [
      {
        "id": 1, // ID задачи в Label Studio
        "annotations": [
          {
            "id": 1, // ID аннотации
            "completed_by": 1, // ID пользователя, выполнившего разметку
            "result": [ // Массив результатов разметки
              {
                "original_width": 3606,
                "original_height": 5409,
                "image_rotation": 0,
                "value": {
                  "x": 29.471544715447155,  // Координаты в % от ширины/высоты
                  "y": 17.615176151761517,
                  "width": 47.76422764227644,
                  "height": 69.64769647696477,
                  "rotation": 0,
                  "rectanglelabels": ["Cat"] // Присвоенная метка
                },
                "id": "awOF7HsKlJ", // Уникальный ID элемента разметки
                "from_name": "label", // Имя тега RectangleLabels из XML
                "to_name": "image",   // Имя тега Image из XML
                "type": "rectanglelabels",
                "origin": "manual"
              }
            ],
            // ... другие поля аннотации ...
          }
        ],
        "file_upload": "48c220e9-pexels-fox-58267-762986.jpg", // Имя загруженного файла
        "data": {
          "image": "/data/upload/1/48c220e9-pexels-fox-58267-762986.jpg" // Ключевой путь ВНУТРИ КОНТЕЙНЕРА!
        },
        // ... другие поля задачи ...
      }
      // ... другие задачи ...
    ]
    ```

### 3.2. Проверка разметки с помощью Python-скрипта
Для визуальной проверки корректности экспортированных аннотаций можно использовать Python-скрипт с библиотекой OpenCV.

**Ключевые моменты для скрипта:**

1.  **Путь к данным Label Studio на хосте:** Скрипту нужно знать, где на вашем компьютере находится директория `label_studio_data`, которую вы монтировали в контейнер.
2.  **Формирование пути к изображениям:**
    *   В JSON-файле путь к изображению указан относительно внутренней структуры контейнера (например, `/data/upload/PROJECT_ID/filename.jpg`).
    *   Скрипт должен преобразовать этот путь в реальный путь на вашем хост-компьютере. Это делается путем замены префикса `/data/` на путь к поддиректории `media/` внутри вашей основной директории `label_studio_data`.
    *   Использование `os.path.join` и `os.sep` делает скрипт кроссплатформенным (работает и на Windows, и на Linux).
3.  **Координаты:** Координаты в JSON (`x`, `y`, `width`, `height`) даны в процентах от оригинальных размеров изображения. Их нужно пересчитать в пиксели.
4.  **Отображение:** Для удобства просмотра больших изображений может потребоваться их масштабирование.

**Пример Python-скрипта для визуализации:**

```python
import json
import cv2
import os

# --- НАСТРОЙКИ ---
# !!! ЗАМЕНИТЕ ЭТО НА ВАШ РЕАЛЬНЫЙ ПУТЬ К ДИРЕКТОРИИ, СОЗДАННОЙ НА ШАГЕ 1.3.1 !!!
# Например:
#   Windows: r"C:\Users\YourUser\Documents\label_studio_projects\label_studio_data"
#   Linux:   "/home/youruser/projects/label_studio_data"
BASE_HOST_PATH_TO_LABEL_STUDIO_DATA = r"C:\Users\maxku\Desktop\comparing-data-markup\label_studio_data" # ИЛИ /путь/к/вашей/папке/label_studio_data

# Путь к экспортированному JSON файлу
EXPORTED_JSON_PATH = "project-1-at-....json" # Замените на имя вашего файла

# Максимальные размеры для отображаемого окна (если 0, то без масштабирования)
MAX_DISPLAY_WIDTH = 1280
MAX_DISPLAY_HEIGHT = 720
WINDOW_NAME_PREFIX = "Label Studio Annotation Viewer"
# --- КОНЕЦ НАСТРОЕК ---

def visualize_annotations(json_path, base_data_path):
    if not os.path.exists(json_path):
        print(f"Ошибка: Файл аннотаций не найден: {json_path}")
        return
    if not os.path.exists(base_data_path):
        print(f"Ошибка: Базовая директория данных Label Studio не найдена: {base_data_path}")
        return

    with open(json_path, 'r', encoding='utf-8') as f:
        tasks = json.load(f)

    for i, task in enumerate(tasks):
        task_id = task.get("id", f"unknown_task_{i}")
        task_id_str = str(task_id)
        print(f"\nОбработка задачи ID: {task_id_str}")

        # Формирование пути к изображению на хосте
        image_path_from_json = task.get("data", {}).get("image")
        if not image_path_from_json:
            print(f"  Предупреждение: Путь к изображению не найден в задаче ID: {task_id_str}")
            continue

        full_image_path_on_host = None
        # Путь в JSON обычно /data/upload/PROJECT_ID/filename.jpg
        # На хосте это BASE_HOST_PATH_TO_LABEL_STUDIO_DATA/media/upload/PROJECT_ID/filename.jpg
        if image_path_from_json.startswith('/data/'):
            # Убираем '/data/' и заменяем разделители на системные
            relative_path_in_container = image_path_from_json[len('/data/'):].lstrip('/')
            # На хосте файлы лежат в подпапке media относительно корня данных LS
            # Для Windows могут быть проблемы с / в пути, поэтому заменяем на os.sep
            path_parts = relative_path_in_container.split('/')
            correct_relative_path = os.path.join("media", *path_parts)
            full_image_path_on_host = os.path.join(base_data_path, correct_relative_path)
        else:
            # Попытка использовать путь как есть, если он не стандартный
            # Это может потребовать доработки в зависимости от того, как данные были импортированы
            print(f"  Предупреждение: Нестандартный путь к изображению: {image_path_from_json}. Попытка использовать как есть.")
            full_image_path_on_host = os.path.join(base_data_path, image_path_from_json.lstrip('/'))


        if not os.path.exists(full_image_path_on_host):
            print(f"  Ошибка: Файл изображения не найден на хосте: {full_image_path_on_host}")
            print(f"  Проверьте BASE_HOST_PATH_TO_LABEL_STUDIO_DATA и структуру папок.")
            continue
        
        print(f"  Загрузка изображения: {full_image_path_on_host}")
        original_image = cv2.imread(full_image_path_on_host)
        if original_image is None:
            print(f"  Ошибка: Не удалось загрузить изображение: {full_image_path_on_host}")
            continue

        display_image = original_image.copy()
        img_height, img_width = original_image.shape[:2]

        for annotation in task.get("annotations", []):
            for result in annotation.get("result", []):
                if result.get("type") == "rectanglelabels":
                    value = result["value"]
                    label_text = ", ".join(value["rectanglelabels"])
                    
                    # Координаты в % от размеров изображения
                    x_percent = value["x"]
                    y_percent = value["y"]
                    width_percent = value["width"]
                    height_percent = value["height"]

                    # Пересчет в пиксели
                    x1 = int((x_percent / 100.0) * img_width)
                    y1 = int((y_percent / 100.0) * img_height)
                    x2 = int(((x_percent + width_percent) / 100.0) * img_width)
                    y2 = int(((y_percent + height_percent) / 100.0) * img_height)

                    color = (0, 255, 0) # Зеленый цвет для рамок
                    line_thickness = 2
                    font_scale = 0.7

                    cv2.rectangle(display_image, (x1, y1), (x2, y2), color, line_thickness)
                    cv2.putText(display_image, label_text, (x1, y1 - 10 if y1 > 20 else y1 + 20),
                                cv2.FONT_HERSHEY_SIMPLEX, font_scale, color, line_thickness)
        
        # Масштабирование display_image для отображения, если необходимо
        if MAX_DISPLAY_WIDTH > 0 and MAX_DISPLAY_HEIGHT > 0:
            h_orig, w_orig = display_image.shape[:2]
            scale = min(MAX_DISPLAY_WIDTH / w_orig, MAX_DISPLAY_HEIGHT / h_orig)
            if scale < 1: # Масштабируем только если изображение больше окна
                new_w, new_h = int(w_orig * scale), int(h_orig * scale)
                resized_display_image = cv2.resize(display_image, (new_w, new_h), interpolation=cv2.INTER_AREA)
            else:
                resized_display_image = display_image
        else:
            resized_display_image = display_image

        current_window_name = f"{WINDOW_NAME_PREFIX} - Task: {task_id_str} ({i+1}/{len(tasks)})"
        cv2.imshow(current_window_name, resized_display_image)
        
        print(f"  Отображена задача {task_id_str}. Нажмите любую клавишу для следующей, ESC для выхода.")
        key = cv2.waitKey(0)
        
        try:
            cv2.destroyWindow(current_window_name)
        except cv2.error as e:
            # Это может произойти, если пользователь закрыл окно вручную крестиком
            print(f"  Info: Не удалось закрыть окно '{current_window_name}' (возможно, закрыто пользователем): {e}")

        if key == 27:  # ESC
            print("Выход по требованию пользователя.")
            break
    
    cv2.destroyAllWindows() # Закрыть все оставшиеся окна OpenCV
    print("\nПроверка завершена.")

if __name__ == "__main__":
    visualize_annotations(EXPORTED_JSON_PATH, BASE_HOST_PATH_TO_LABEL_STUDIO_DATA)
```

**Как использовать скрипт:**
1.  Сохраните код выше как Python-файл (например, `view_annotations.py`).
2.  **Обязательно** измените значение `BASE_HOST_PATH_TO_LABEL_STUDIO_DATA` на ваш реальный путь к директории `label_studio_data`.
3.  Измените `EXPORTED_JSON_PATH` на имя вашего экспортированного JSON-файла (поместите его в ту же папку, что и скрипт, или укажите полный путь).
4.  Запустите скрипт из терминала: `python view_annotations.py`.
5.  Изображения с наложенными рамками будут отображаться по очереди. Нажимайте любую клавишу для перехода к следующему, ESC для выхода.

**Результат проверки:** Визуализация с помощью скрипта подтвердила, что аннотации были сделаны в целом корректно. Рамки соответствовали объектам на изображениях.

## 4. Впечатления от первого опыта использования Label Studio

*   **Удобство интерфейса:**
    *   **Положительно:** Основной интерфейс для создания проектов, импорта данных и разметки достаточно интуитивен. Процесс рисования bounding box'ов простой и удобный. Возможность настройки горячих клавиш является плюсом.

*   **Понятность настроек:**
    *   **Положительно:** Выбор шаблонов для интерфейса разметки значительно упрощает старт. Базовые настройки проекта понятны.
    *   **Сложности:** Глубокая кастомизация интерфейса через XML требует изучения документации по тегам Label Studio. Формат экспортируемых данных (особенно пути к файлам и структура JSON) требует внимания при последующей программной обработке.

*   **Возникшие вопросы или трудности при самой разметке и работе:**
    *   **Пути к файлам:** Понимание того, как Label Studio хранит файлы (внутри контейнера `/data/...`) и как эти пути соотносятся с файловой системой хоста (через подпапку `media/` в смонтированном томе), стало ключевым моментом для внешней обработки данных и отладки скрипта проверки.
    *   **Масштабирование изображений:** При ручной проверке в Label Studio или при внешней визуализации больших изображений необходимо учитывать масштабирование, чтобы корректно оценить разметку.
    *   **Выбор метки:** Для задачи с небольшим количеством классов это не проблема, но при большом количестве меток может потребоваться более эффективный способ их выбора (например, поиск по меткам, горячие клавиши для часто используемых).

*   **Общее впечатление:** Label Studio является мощным и гибким инструментом для разметки данных. Локальное развертывание через Docker с монтированием тома работает надежно и обеспечивает персистентность данных. Основные задачи разметки выполняются легко. Для эффективной интеграции в пайплайны обработки данных важно разобраться со структурой экспорта и путями к файлам. Возможность проверки разметки с помощью внешних скриптов является важным этапом контроля качества.

## 5. Заключение
Задача по развертыванию Label Studio через Docker, выполнению тестовой разметки, экспорту и проверке данных успешно выполнена. Получен ценный практический опыт работы с инструментом, выявлены потенциальные сложности (особенно связанные с путями к файлам при работе с Docker-контейнером) и способы их решения. Процесс задокументирован в данном отчете, который может служить руководством для новых пользователей на платформах Windows и Linux.

---
