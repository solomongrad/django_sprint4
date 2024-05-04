from django.db import models


class CreatedAtModel(models.Model):
    created_at = models.DateTimeField(
        'Добавлено',
        auto_now_add=True,
        help_text='Если установить дату и'
        'время в будущем — можно делать отложенные публикации.'
    )

    class Meta:
        abstract = True


class IsPublishedCreatedAtModel(CreatedAtModel):
    """Абстрактная модель. Добавляет флаг is_published и created_at."""

    is_published = models.BooleanField(
        'Опубликовано',
        default=True,
        help_text='Снимите галочку, чтобы скрыть публикацию.'
    )

    class Meta:
        abstract = True
