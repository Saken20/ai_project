// ai_app/static/ai_app/js/script.js

$(document).ready(function () {
    var currentSessionId = null;

    // Настройка CSRF-токена для AJAX
    $.ajaxSetup({
        headers: { "X-CSRFToken": csrfToken }
    });

    // Проверка сохранённой темы при загрузке страницы
    if (localStorage.getItem('theme') === 'dark') {
        $('body').addClass('dark-mode');
        $('#theme-toggle').text('Светлая тема');
    }

    // Загрузка существующих сессий при загрузке страницы
    loadSessions();

    // Создание новой сессии при нажатии на "Новый Чат"
    $('#new-session').click(function () {
        createNewSession();
    });

    // Отправка сообщения при нажатии на кнопку "Отправить"
    $('#send').click(function () {
        sendMessage();
    });

    // Отправка сообщения при нажатии клавиши Enter
    $('#message').keypress(function (event) {
        if (event.which === 13) {
            event.preventDefault();
            sendMessage();
        }
    });

    // Переключение темы при нажатии на кнопку "Тёмная тема"
    $('#theme-toggle').click(function () {
        $('body').toggleClass('dark-mode');
        if ($('body').hasClass('dark-mode')) {
            $('#theme-toggle').text('Светлая тема');
            localStorage.setItem('theme', 'dark');
        } else {
            $('#theme-toggle').text('Тёмная тема');
            localStorage.setItem('theme', 'light');
        }
    });

    // Переключение боковой панели при нажатии на кнопку "sidebar-toggle"
    $('#sidebar-toggle').click(function () {
        $('#sidebar').toggleClass('collapsed');
        $('#main-chat').toggleClass('expanded');
    });

    // Функция загрузки списка сессий
    function loadSessions() {
        $.ajax({
            url: '/ajax/get_sessions/',
            type: 'GET',
            success: function (data) {
                var sessionList = $('#session-list');
                sessionList.empty();
                data.sessions.forEach(function (session) {
                    var sessionItem = $('<li>')
                        .addClass('list-group-item')
                        .attr('data-session-id', session.id)
                        .text(session.title + ' - ' + formatDate(session.created_at));
                    sessionList.append(sessionItem);
                });

                // Автоматически выбрать первую сессию, если она существует
                if (data.sessions.length > 0) {
                    var firstSessionId = data.sessions[0].id;
                    selectSession(firstSessionId);
                } else {
                    createNewSession();
                }
            },
            error: function () {
                alert('Ошибка при загрузке сессий.');
            }
        });
    }

    // Функция создания новой сессии
    function createNewSession() {
        $.ajax({
            url: '/ajax/get_response/',
            type: 'POST',
            data: { 'message': 'Создание нового чата' },
            success: function (data) {
                currentSessionId = data.session_id;
                $('#session-list .list-group-item').removeClass('active');
                var sessionList = $('#session-list');
                var newSessionItem = $('<li>')
                    .addClass('list-group-item active')
                    .attr('data-session-id', currentSessionId)
                    .text('Новый Чат - ' + formatDate(new Date().toISOString()));
                sessionList.prepend(newSessionItem);
                loadMessages(currentSessionId);
            },
            error: function () {
                alert('Ошибка при создании новой сессии.');
            }
        });
    }

    // Обработка выбора сессии из списка
    $('#session-list').on('click', '.list-group-item', function () {
        var sessionId = $(this).data('session-id');
        selectSession(sessionId);
    });

    // Функция выбора сессии
    function selectSession(sessionId) {
        currentSessionId = sessionId;
        $('#session-list .list-group-item').removeClass('active');
        $('#session-list .list-group-item[data-session-id="' + sessionId + '"]').addClass('active');
        loadMessages(sessionId);
    }

    // Функция загрузки сообщений из сессии
    function loadMessages(sessionId) {
        $.ajax({
            url: '/ajax/get_session_messages/' + sessionId + '/',
            type: 'GET',
            success: function (data) {
                $('#chat-box').empty();
                data.messages.forEach(function (msg) {
                    if (msg.sender === 'user') {
                        var userMessageHtml = '<div class="user-message"><div class="message"><strong>Вы:</strong> ' + escapeHtml(msg.message) + '</div></div>';
                        $('#chat-box').append(userMessageHtml);
                    } else if (msg.sender === 'bot') {
                        var botMessageHtml = '<div class="bot-message"><div class="message"><strong>Бот:</strong> ' + escapeHtml(msg.message) + '</div></div>';
                        $('#chat-box').append(botMessageHtml);
                    }
                });
                $('#chat-box').scrollTop($('#chat-box')[0].scrollHeight);
            },
            error: function () {
                alert('Ошибка при загрузке сообщений.');
            }
        });
    }

    // Функция отправки сообщения
    function sendMessage() {
        var message = $('#message').val();
        if (message.trim() !== '' && currentSessionId) {
            var userMessageHtml = '<div class="user-message"><div class="message"><strong>Вы:</strong> ' + escapeHtml(message) + '</div></div>';
            $('#chat-box').append(userMessageHtml);
            $('#message').val('');
            $('#chat-box').scrollTop($('#chat-box')[0].scrollHeight);

            $.ajax({
                url: '/ajax/get_response/',
                type: 'POST',
                data: {
                    'message': message,
                    'session_id': currentSessionId
                },
                success: function (data) {
                    if (data.session_id !== currentSessionId) {
                        currentSessionId = data.session_id;
                        $('#session-list .list-group-item').removeClass('active');
                        $('#session-list .list-group-item[data-session-id="' + currentSessionId + '"]').addClass('active');
                    }

                    var botMessageHtml = '<div class="bot-message"><div class="message"><strong>Бот:</strong> <span class="message-text"></span></div></div>';
                    $('#chat-box').append(botMessageHtml);
                    $('#chat-box').scrollTop($('#chat-box')[0].scrollHeight);

                    typeText($('.message-text').last(), data.response, 0);
                },
                error: function () {
                    alert('Ошибка при отправке сообщения.');
                }
            });
        }
    }

    // Функция анимации набора текста
    function typeText(element, text, index) {
        if (index < text.length) {
            element.append(escapeHtml(text.charAt(index)));
            index++;
            setTimeout(function () {
                typeText(element, text, index);
                $('#chat-box').scrollTop($('#chat-box')[0].scrollHeight);
            }, 20); // Скорость набора (мс)
        }
    }

    // Функция экранирования HTML для предотвращения XSS
    function escapeHtml(text) {
        return text.replace(/[&<>"'`=\/]/g, function (s) {
            return ({
                '&': '&amp;',
                '<': '&lt;',
                '>': '&gt;',
                '"': '&quot;',
                "'": '&#39;',
                '/': '&#x2F;',
                '`': '&#x60;',
                '=': '&#x3D;'
            })[s];
        });
    }

    // Функция форматирования даты
    function formatDate(dateString) {
        var date = new Date(dateString);
        return date.toLocaleString();
    }
});
