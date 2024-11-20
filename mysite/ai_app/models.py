from django.db import models
from django.conf import settings  # Используем настройки, чтобы подставить кастомную модель пользователя

class ChatSession(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)  # Используем кастомную модель пользователя
    title = models.CharField(max_length=255, default='Новый Чат')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class ChatMessage(models.Model):
    session = models.ForeignKey(ChatSession, related_name='messages', on_delete=models.CASCADE)
    sender = models.CharField(max_length=10)  # 'user' или 'bot'
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']
