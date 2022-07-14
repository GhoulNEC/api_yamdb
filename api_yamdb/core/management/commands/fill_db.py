import csv
import inspect
import os

from reviews import models
from django.core.management.base import BaseCommand

from api_yamdb.settings import BASE_DIR


class Command(BaseCommand):
    help = u'Заполнить таблицы БД'

    def add_arguments(self, parser):
        parser.add_argument('-m',
                            '--model',
                            type=str,
                            help=u'Модель'
                            )
        parser.add_argument('-f',
                            '--file',
                            type=str,
                            help=u'Путь файла с данными csv'
                            )

    def get_csv_file(self, filename):
        name_file = filename + '.csv'
        path = os.path.join(BASE_DIR, 'static', 'data', name_file)
        if not os.path.exists(path):
            self.stderr.write(self.style.WARNING('Файл не найден!'))
        return path

    def get_obj_models(self, model):
        """Добавить проверку на наличие классов в модуле."""
        classes = [obj for obj in inspect.getmembers(models, inspect.isclass)]
        for name, obj in classes:
            if name == model:
                return obj
        self.stderr.write(self.style.WARNING('Такой модели нет!'))

    def handle(self, *args, **kwargs):
        model = kwargs['model']
        filename = kwargs['file']
        file_path = self.get_csv_file(filename)
        obj = self.get_obj_models(model)

        with open(file_path, 'r', encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=",")
            # for column in csv_reader:
                # obj.ojects.get_or_create(column=value)

