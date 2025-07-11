# Generated by Django 5.2.3 on 2025-07-06 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_alter_choice_options_alter_question_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='correct_answer_text',
            field=models.TextField(blank=True, null=True, verbose_name='Правильный текстовый ответ'),
        ),
        migrations.AlterField(
            model_name='question',
            name='question_type',
            field=models.CharField(choices=[('text', 'Текстовый ответ'), ('single', 'Один вариант'), ('multiple', 'Несколько вариантов')], max_length=10, verbose_name='Тип вопроса'),
        ),
        migrations.AlterField(
            model_name='question',
            name='text',
            field=models.TextField(verbose_name='Текст вопроса'),
        ),
    ]
