const notificationBtn = document.getElementById('notificationBtn');
const notificationPanel = document.getElementById('notificationPanel');
const userBtn = document.getElementById('userBtn');
const userMenu = document.getElementById('userMenu');

if (notificationBtn) {
    notificationBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        notificationPanel.classList.toggle('hidden');
        if (userMenu) userMenu.classList.add('hidden');
    });
}

if (userBtn) {
    userBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        userMenu.classList.toggle('hidden');
        if (notificationPanel) notificationPanel.classList.add('hidden');
    });
}

// Close dropdowns when clicking outside
document.addEventListener('click', () => {
    if (notificationPanel) notificationPanel.classList.add('hidden');
    if (userMenu) userMenu.classList.add('hidden');
});
