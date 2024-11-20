# ai_app/views.py

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import ChatSession, ChatMessage
import subprocess
import logging
from django.utils import timezone

logger = logging.getLogger('ai_app')

def chat_view(request):
    """
    Отображает страницу чата и передаёт список сессий.
    """
    # Если используется аутентификация, фильтруйте сессии по пользователю
    sessions = ChatSession.objects.all().order_by('-created_at')
    return render(request, 'ai_app/chat.html', {'sessions': sessions})

def get_response(request):
    """
    Обрабатывает отправку сообщения, создаёт новую сессию при необходимости,
    сохраняет сообщения и возвращает ответ от модели.
    """
    if request.method == 'POST':
        session_id = request.POST.get('session_id')
        message = request.POST.get('message')

        if not message:
            return JsonResponse({'response': 'Пустое сообщение не может быть отправлено.'}, status=400)

        if not session_id:
            # Создание новой сессии, если session_id не передан
            session = ChatSession.objects.create(title='Новый Чат')
            logger.debug(f"Создана новая сессия: {session.id}")
        else:
            session = get_object_or_404(ChatSession, id=session_id)

        # Сохранение сообщения пользователя
        ChatMessage.objects.create(session=session, sender='user', message=message, timestamp=timezone.now())
        logger.debug(f"Сохранено сообщение пользователя в сессии {session.id}: {message}")

        # Получение последних сообщений для контекста
        messages = session.messages.order_by('-timestamp')[:5]
        conversation = ""
        for msg in reversed(messages):
            if msg.sender == 'user':
                conversation += f"Вы: {msg.message}\n"
            else:
                conversation += f"Бот: {msg.message}\n"

        # Добавление инструкции
#        instruction = "Ты — чат-бот, который общается исключительно на русском языке.\n"
        instruction = ""
        full_message = instruction + conversation + f"Вы: {message}\nБот:"

        try:
            # Вызов модели Llama3.2 через Ollama с явной кодировкой
            process = subprocess.Popen(
                ['ollama', 'run', 'llama3.2'],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                encoding='utf-8',  # Явно указываем кодировку
                errors='replace'    # Заменяем некорректные символы
            )
            output, error = process.communicate(input=full_message, timeout=30)  # Передача пользовательского ввода в stdin

            if process.returncode != 0:
                logger.error(f"Ошибка при выполнении Ollama: {error}")
                response = f"Ошибка: {error.strip()}"
            else:
                response = output.strip() if output else "Нет ответа от модели."
                logger.debug(f"Получен ответ модели: {response}")

        except subprocess.TimeoutExpired:
            process.kill()
            output, error = process.communicate()
            logger.error("Ошибка: Превышено время ожидания ответа от модели.")
            response = "Ошибка: Превышено время ожидания ответа от модели."

        except Exception as e:
            logger.exception("Непредвиденная ошибка при выполнении Ollama.")
            response = f"Ошибка: {str(e)}"

        # Сохранение ответа бота
        ChatMessage.objects.create(session=session, sender='bot', message=response, timestamp=timezone.now())
        logger.debug(f"Сохранено сообщение бота в сессии {session.id}: {response}")

        return JsonResponse({'response': response, 'session_id': session.id})

    return JsonResponse({'response': 'Неверный метод запроса.'}, status=405)

def get_sessions(request):
    """
    Возвращает список всех сессий чата.
    """
    sessions = ChatSession.objects.all().order_by('-created_at').values('id', 'title', 'created_at')
    return JsonResponse({'sessions': list(sessions)})

def get_session_messages(request, session_id):
    """
    Возвращает все сообщения для конкретной сессии.
    """
    session = get_object_or_404(ChatSession, id=session_id)
    messages = session.messages.all().values('sender', 'message', 'timestamp')
    return JsonResponse({'messages': list(messages)})
