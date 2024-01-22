Описание проекта:
Модель классификации определяющая ценовую категорию (low, medium, high)
поддержанного автомобиля в зависимости от его характеристик.

Содержимое:
- DAG-файл, описывающий пайплайн проекта (dags/hw_dag.py);
- код ML-модели (modules/pipeline.py);
- скрипт для выполнения предикта моделью (modules/predict.py);
- данные для обучения и тестирования (data/train, data/test).

Пайплайн модели состоит из двух шагов:

    1. pipeline:
    - обрабатывает тренировочные данные;
    - обучает на обработанных данных логистическую регрессию, случайный лес и метод
      опорных векторов;
    - сохраняет модель с лучшей точностью в pickle-файл.

    2. predict:
    - делает предикт на тестовых данных моделью из pipeline;
    - сохраняет предсказания в .csv файл.

Запуск пайплайна локально и в Airflow:

    1. Локальный запуск:
    - клонировать удалённый репозиторий на свой компьютер и поочерёдно запустить
      pipeline.py и predict.py;
    - в папке predictions появится .csv файл с id автомобиля и его ценовой категорией.

    2. Запуск через Airflow:
    - скопировать даг из папки со скриптами в папку для дагов в директории Airflow:
      cp ~/airflow_hw/dags/hw_dag.py ~/airflow-docker/dags
    - Скопировать исполняемый код и данные в контейнеры worker и scheduler:
      docker cp ~/airflow_hw <id контейнера worker>:/home/airflow/airflow_hw
      docker cp ~/airflow_hw <id контейнера scheduler>:/home/airflow/airflow_hw
    - зайти в командную строку контейнеров и доустановить используемые в пайплайне
      библиотеки:
      docker exec -it <id контейнера worker> bash
      pip install <название библиотеки>
      docker exec -it <id контейнера scheduler> bash
      pip install <название библиотеки>
    - Иногда при запуске пайплайна может возникать ошибка при сохранении pkl-дампа
      модели. Чтобы избежать этого, нужно зайти в контейнеры worker и scheduler от
      имени root-пользователя и дать права командой chmod:
      docker exec -it -u root <id контейнера worker> bash
      cd /home/airflow/airflow_hw
      chmod -R 777 data dags modules
      docker exec -it -u root <id контейнера scheduler> bash
      cd /home/airflow/airflow_hw
      chmod -R 777 data dags modules
    - после запуска пайплайна из интерфейса Airflow, предикты будут находится в папках
      airflow_hw/predictions, перемещенных в worker и scheduler.