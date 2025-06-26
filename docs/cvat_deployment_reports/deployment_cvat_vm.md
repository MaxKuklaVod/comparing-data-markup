# Развертывание CVAT на виртуальной машине

Это руководство описывает шаги по развертыванию CVAT (Computer Vision Annotation Tool) на виртуальной машине (ВМ) с использованием Docker Compose, как рекомендовано официальной документацией.

## Предварительные требования

1.  **Виртуальная машина:** С установленной операционной системой Linux (например, Ubuntu Server 20.04 LTS или новее). Рекомендуется минимум 4 ГБ RAM, для комфортной работы – 8 ГБ+.
2.  **Доступ с правами `sudo`:** Для установки программного обеспечения и управления Docker.
3.  **Установленный Docker и Docker Compose:**
    *   Инструкции по установке Docker: [https://docs.docker.com/engine/install/](https://docs.docker.com/engine/install/)
    *   Инструкции по установке Docker Compose (версия 1.29.0 или выше, для Compose V2 – `docker compose`): [https://docs.docker.com/compose/install/](https://docs.docker.com/compose/install/)
4.  **Установленный Git:** Для клонирования репозитория CVAT.
    ```bash
    sudo apt update
    sudo apt install git -y
    ```

## Шаги развертывания

1.  **Клонирование репозитория CVAT:**
    ```bash
    git clone https://github.com/cvat-ai/cvat
    cd cvat
    ```

2.  **Настройка переменной `CVAT_HOST`:**
    Эта переменная окружения должна содержать публичный IP-адрес или доменное имя вашей виртуальной машины, по которому CVAT будет доступен извне.
    ```bash
    export CVAT_HOST=<IP_АДРЕС_ВАШЕЙ_ВМ>
    ```
    **Важно:** Для постоянной установки эту переменную лучше добавить в `~/.bashrc` или `~/.profile` и перезагрузить сессию, либо передавать ее при каждом запуске `docker-compose`. Либо можно создать файл `.env` в директории `cvat` и прописать там `CVAT_HOST=ВАШ_IP_АДРЕС`.

3.  **Возможный фикс для Open Policy Agent (OPA):**
    Иногда могут возникать проблемы с инициализацией сервиса OPA, который используется для управления доступом. Если стандартный запуск не удается, можно попробовать следующий обходной путь (выполняется *перед* `docker compose up -d`):
    ```bash
    # Сначала остановите все возможные запущенные ранее сервисы CVAT
    docker compose down 
    
    # Запустите OPA в отладочном режиме с нужными параметрами
    docker run -d --rm --name cvat_opa_debug -p 8181:8181 openpolicyagent/opa:0.60.0-rootless \
     run --server \
     --set=decision_logs.console=true \
     --set=services.cvat.url=http://cvat_server:8080/api/auth/rules \
     --set=bundles.cvat.service=cvat \
     --set=bundles.cvat.resource=/api/auth/rules \
     --set=plugins.envoy_ext_authz_grpc.addr=:9001 \
     --set=plugins.envoy_ext_authz_grpc.query=data.cvat.authz.allow
    ```

4.  **Сборка и запуск контейнеров CVAT:**
    Или для более простого запуска без компонентов для разработки:
    ```bash
    docker compose up -d --build
    ```
    *   `--build`: Пересобрать образы, если они изменились или это первый запуск.
    *   `-d`: Запустить в фоновом режиме.

5.  **Создание суперпользователя:**
    После того как все контейнеры запустятся (это может занять несколько минут), необходимо создать аккаунт суперпользователя.
    ```bash
    docker compose exec cvat_server bash -ic 'python3 ~/manage.py createsuperuser'
    ```
    Вам будет предложено ввести имя пользователя, email и пароль.

6.  **Проверка работы:**
    *   CVAT должен быть доступен в вашем веб-браузере по адресу `http://<IP_АДРЕС_ВАШЕЙ_ВМ>:8080` (если порт по умолчанию не изменен).
    *   Войдите, используя созданные учетные данные суперпользователя.

7.  **Управление сервисами:**
    *   Посмотреть логи всех сервисов: `docker compose logs -f`
    *   Остановить сервисы: `docker compose down`
    *   Остановить без удаления томов (данные сохранятся): `docker compose stop`
    *   Запустить остановленные: `docker compose start`
