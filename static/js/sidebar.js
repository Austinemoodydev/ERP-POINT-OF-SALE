// Dropdown menus
document.querySelectorAll('.dropdown-btn').forEach(button => {
    button.addEventListener('click', () => {
        const submenu = button.nextElementSibling;
        submenu.classList.toggle('active');
        const icon = button.querySelector('.fa-chevron-down');
        if (icon) icon.classList.toggle('rotate-180');
    });
});

// Mobile sidebar toggle
const menuBtn = document.getElementById('menuBtn');
const sidebar = document.getElementById('sidebar');
if (menuBtn && sidebar) {
    menuBtn.addEventListener('click', () => {
        sidebar.classList.toggle('open');
    });
}
