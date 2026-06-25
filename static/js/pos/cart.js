// ============================================================
// POSERP — cart.js  |  Supermarket-grade Cart Engine
// ============================================================

let cart = [];
let discount = 0;

function addToCart(product) {
    let existing = cart.find(item => item.id === product.id);
    if (existing) {
        existing.qty++;
    } else {
        cart.push({
            id: product.id,
            name: product.name,
            price: parseFloat(product.price),
            tax: parseFloat(product.tax) || 0,
            qty: 1
        });
    }
    renderCart();
}

function increaseQty(id) {
    let item = cart.find(i => i.id === id);
    if (item) { item.qty++; renderCart(); }
}

function decreaseQty(id) {
    let item = cart.find(i => i.id === id);
    if (item) {
        item.qty--;
        if (item.qty <= 0) removeItem(id);
        else renderCart();
    }
}

function removeItem(id) {
    cart = cart.filter(i => i.id !== id);
    renderCart();
}

function clearCart() {
    cart = [];
    discount = 0;
    renderCart();
}

function applyDiscount(amount) {
    discount = parseFloat(amount) || 0;
    renderCart();
}

function renderCart() {
    let body = document.getElementById('cartBody');
    if (!body) return;
    body.innerHTML = '';

    let subtotal = 0;
    let vat = 0;

    cart.forEach(item => {
        let lineTotal = item.price * item.qty;
        let lineVat   = item.tax * item.qty;
        subtotal += lineTotal;
        vat      += lineVat;

        body.innerHTML += `
        <tr>
            <td>${item.name}</td>
            <td>
                <button class="btn btn-sm btn-outline-secondary" onclick="decreaseQty('${item.id}')">-</button>
                <span class="mx-1">${item.qty}</span>
                <button class="btn btn-sm btn-outline-secondary" onclick="increaseQty('${item.id}')">+</button>
            </td>
            <td>KES ${lineTotal.toFixed(2)}</td>
            <td><button class="btn btn-sm btn-danger" onclick="removeItem('${item.id}')">✕</button></td>
        </tr>`;
    });

    let grand = subtotal + vat - discount;

    let el = id => document.getElementById(id);
    if (el('subtotal'))  el('subtotal').innerText  = 'KES ' + subtotal.toFixed(2);
    if (el('vat'))       el('vat').innerText       = 'KES ' + vat.toFixed(2);
    if (el('discount'))  el('discount').innerText  = 'KES ' + discount.toFixed(2);
    if (el('grandTotal')) el('grandTotal').innerText = 'KES ' + grand.toFixed(2);

    // receipt panel sync
    updateReceipt();
}

function updateReceipt() {
    let panel = document.getElementById('receiptItems');
    if (!panel) return;
    panel.innerHTML = cart.map(i =>
        `<div class="d-flex justify-content-between">
            <span>${i.name} x${i.qty}</span>
            <span>KES ${(i.price * i.qty).toFixed(2)}</span>
        </div>`
    ).join('');
}

// Attach click handlers to product cards
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.product-card').forEach(card => {
        card.addEventListener('click', () => {
            addToCart({
                id:    card.dataset.id,
                name:  card.dataset.name,
                price: parseFloat(card.dataset.price),
                tax:   parseFloat(card.dataset.tax) || 0
            });
        });
    });
});
