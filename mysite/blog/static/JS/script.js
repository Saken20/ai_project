function toggleSidebar(event) {
    event.stopPropagation(); // Предотвращаем всплытие клика
    const sidebar = document.getElementById("sidebar");
    sidebar.classList.toggle("sidebar-open");
}

function closeSidebar(event) {
    event.stopPropagation(); // Предотвращаем всплытие клика
    const sidebar = document.getElementById("sidebar");
    sidebar.classList.remove("sidebar-open");
}

// Закрытие меню при клике вне панели
document.addEventListener("click", function(event) {
    const sidebar = document.getElementById("sidebar");
    const openBtn = document.getElementById("open-btn");
    const closeBtn = document.getElementById("close-btn");
    const isClickInsideSidebar = sidebar.contains(event.target);
    const isClickOnOpenBtn = openBtn.contains(event.target);
    const isClickOnCloseBtn = closeBtn.contains(event.target);
    const isSidebarOpen = sidebar.classList.contains("sidebar-open");

    // Закрываем панель, если клик был за ее пределами и меню открыто
    if (!isClickInsideSidebar && !isClickOnOpenBtn && isSidebarOpen) {
        sidebar.classList.remove("sidebar-open");
    }
});

