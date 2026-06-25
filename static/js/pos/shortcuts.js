// ============================================================
// POSERP — shortcuts.js  |  F1-F7 Keyboard Shortcuts
// ============================================================

document.addEventListener('keydown', e => {
    switch (e.key) {
        case 'F1':
            e.preventDefault();
            document.getElementById('barcodeInput')?.focus();
            break;
        case 'F2':
            e.preventDefault();
            document.getElementById('customerSearchInput')?.focus();
            break;
        case 'F3':
            e.preventDefault();
            holdSale();
            break;
        case 'F4':
            e.preventDefault();
            let d = prompt('Enter discount amount (KES):');
            if (d !== null) applyDiscount(d);
            break;
        case 'F5':
            e.preventDefault();
            let payModal = document.getElementById('paymentModal');
            if (payModal) new bootstrap.Modal(payModal).show();
            break;
        case 'F6':
            e.preventDefault();
            completeSale();
            break;
        case 'F7':
            e.preventDefault();
            printReceipt();
            break;
        case 'Escape':
            clearCart();
            break;
    }
});

function holdSale() {
    if (cart.length === 0) { alert('Cart is empty.'); return; }
    let held = JSON.parse(localStorage.getItem('heldSales') || '[]');
    held.push({ timestamp: new Date().toISOString(), items: [...cart] });
    localStorage.setItem('heldSales', JSON.stringify(held));
    clearCart();
    showToast('Sale held. Press F3 to resume.', 'warning');
}

function resumeSale() {
    let held = JSON.parse(localStorage.getItem('heldSales') || '[]');
    if (held.length === 0) { alert('No held sales.'); return; }
    let last = held.pop();
    localStorage.setItem('heldSales', JSON.stringify(held));
    cart = last.items;
    renderCart();
    showToast('Sale resumed.', 'info');
}

function completeSale() {
    if (cart.length === 0) { alert('Cart is empty.'); return; }
    let payModal = document.getElementById('paymentModal');
    if (payModal) new bootstrap.Modal(payModal).show();
}

function printReceipt() {
    window.print();
}
