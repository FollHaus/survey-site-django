# Generated by Django 5.2.3 on 2025-07-06 14:33

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='choice',
            options={},
        ),
        migrations.AlterModelOptions(
            name='question',
            options={},
        ),
        migrations.AlterModelOptions(
            name='survey',
            options={},
        ),
        migrations.AlterModelOptions(
            name='userresponse',
            options={},
        ),
        migrations.RemoveField(
            model_name='choice',
            name='order',
        ),
        migrations.RemoveField(
            model_name='question',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='question',
            name='order',
        ),
        migrations.RemoveField(
            model_name='question',
            name='updated_at',
        ),
        migrations.RemoveField(
            model_name='survey',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='survey',
            name='updated_at',
        ),
        migrations.AlterField(
            model_name='choice',
            name='is_correct',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='choice',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='choices', to='polls.question'),
        ),
        migrations.AlterField(
            model_name='choice',
            name='text',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='question',
            name='correct_answer_text',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='question_type',
            field=models.CharField(choices=[('text', 'Текстовый ответ'), ('single', 'Один вариант'), ('multiple', 'Несколько вариантов')], max_length=10),
        ),
        migrations.AlterField(
            model_name='question',
            name='text',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='survey',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='survey',
            name='end_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='survey',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='survey',
            name='start_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='survey',
            name='title',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='userresponse',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='userresponse',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='responses', to='polls.question'),
        ),
        migrations.AlterField(
            model_name='userresponse',
            name='selected_choices',
            field=models.ManyToManyField(related_name='user_responses', to='polls.choice'),
        ),
        migrations.AlterField(
            model_name='userresponse',
            name='survey',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='responses', to='polls.survey'),
        ),
        migrations.AlterField(
            model_name='userresponse',
            name='text_answer',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='userresponse',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='responses', to=settings.AUTH_USER_MODEL),
        ),
    ]
