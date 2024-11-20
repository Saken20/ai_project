function toggleSidebar(event) {
    event.stopPropagation(); // Останавливает всплытие события
    const sidebar = document.getElementById("sidebar");
    sidebar.classList.toggle("sidebar-open"); // Переключаем класс
}

function closeSidebar(event) {
    event.stopPropagation(); // Останавливает всплытие события
    const sidebar = document.getElementById("sidebar");
    sidebar.classList.remove("sidebar-open"); // Закрываем панель
}

// Закрытие при клике вне панели
document.addEventListener("click", function (event) {
    const sidebar = document.getElementById("sidebar");
    const openBtn = document.getElementById("open-btn");
    const closeBtn = document.getElementById("close-btn");

    const isClickInsideSidebar = sidebar.contains(event.target);
    const isClickOnOpenBtn = openBtn.contains(event.target);
    const isSidebarOpen = sidebar.classList.contains("sidebar-open");

    if (!isClickInsideSidebar && !isClickOnOpenBtn && isSidebarOpen) {
        sidebar.classList.remove("sidebar-open");
    }
});

window.addEventListener('resize', () => {
    document.documentElement.style.setProperty('--vh', `${window.innerHeight * 0.01}px`);
});

// Устанавливаем переменную при загрузке страницы
document.addEventListener('DOMContentLoaded', () => {
    document.documentElement.style.setProperty('--vh', `${window.innerHeight * 0.01}px`);
});


const input = document.getElementById('search');
const button = document.getElementById('btn_search');

// Добавляем обработчик события на нажатие клавиш в инпуте
input.addEventListener('keydown', function (event) {
    if (event.key === 'Enter') {  // Проверяем, что нажата клавиша Enter
        event.preventDefault();     // Предотвращаем стандартное действие (если нужно)
        button.click();             // Выполняем клик на кнопке
    }
});

// Обработчик нажатия на кнопку (для примера)
button.addEventListener('click', function () {
    alert('Отправлено: ' + input.value);  // Показать значение инпута в алерте
});


