// ============================================================
// POS CORE ENGINE
// ============================================================
let cart = [];
let currentCustomer = { id: 0, name: 'Walk-in Customer' };
let heldSales = [];
let currentPayMethod = 'cash';
const VAT_RATE = 0.16;

function money(value) {
    return 'KES ' + Number(value || 0).toFixed(2);
}

function escapeHtml(value) {
    const div = document.createElement('div');
    div.textContent = value ?? '';
    return div.innerHTML;
}

function escapeJsArg(value) {
    return String(value ?? '')
        .replace(/\\/g, '\\\\')
        .replace(/'/g, "\\'")
        .replace(/\r?\n/g, ' ');
}

function getCookie(name) {
    const cookies = document.cookie ? document.cookie.split(';') : [];
    for (const cookie of cookies) {
        const trimmed = cookie.trim();
        if (trimmed.startsWith(name + '=')) {
            return decodeURIComponent(trimmed.substring(name.length + 1));
        }
    }
    return '';
}

async function apiFetch(url, options = {}) {
    const headers = {
        'Accept': 'application/json',
        ...(options.headers || {}),
    };

    if (options.body && !headers['Content-Type']) {
        headers['Content-Type'] = 'application/json';
    }

    const response = await fetch(url, {
        credentials: 'same-origin',
        ...options,
        headers: {
            ...headers,
            'X-CSRFToken': getCookie('csrftoken'),
        },
    });

    const data = await response.json().catch(() => ({}));
    if (!response.ok) {
        throw new Error(data.detail || 'Request failed. Please try again.');
    }

    return data;
}

// ---- CART ----
function addToCart(id, name, price) {
    const existing = cart.find(i => String(i.id) === String(id));
    if (existing) {
        existing.qty += 1;
    } else {
        cart.push({ id, name, price: parseFloat(price), qty: 1, discount: 0 });
    }
    renderCart();
}

function addToCartDirect(name, price) {
    addToCart('d_' + name, name, price);
}

function removeFromCart(idx) {
    cart.splice(idx, 1);
    renderCart();
}

function updateQty(idx, val) {
    cart[idx].qty = parseInt(val, 10) || 1;
    if (cart[idx].qty < 1) cart[idx].qty = 1;
    renderCart();
}

function clearCart() {
    if (cart.length === 0) return;
    if (confirm('Clear all items?')) {
        cart = [];
        currentCustomer = { id: 0, name: 'Walk-in Customer' };
        renderCart();
        updateCustomerDisplay();
    }
}

function renderCart() {
    const body = document.getElementById('cartBody');
    if (!body) return;

    body.innerHTML = '';
    if (cart.length === 0) {
        body.innerHTML = '<tr id="emptyCart"><td colspan="4" class="text-center py-12 text-gray-400"><div class="text-4xl mb-2">&#128722;</div><p class="text-sm">Cart is empty</p><p class="text-xs">Click a product or scan barcode</p></td></tr>';
        recalculate();
        return;
    }

    cart.forEach((item, idx) => {
        const row = document.createElement('tr');
        row.className = 'border-b hover:bg-gray-50';
        row.innerHTML = `
            <td class="px-3 py-2">
                <p class="text-sm font-medium">${escapeHtml(item.name)}</p>
                <p class="text-xs text-gray-400">${money(item.price)}</p>
            </td>
            <td class="px-2 py-2 text-center">
                <div class="flex items-center justify-center gap-1">
                    <button onclick="updateQty(${idx}, ${item.qty - 1})" class="w-6 h-6 rounded bg-gray-200 text-sm hover:bg-gray-300">-</button>
                    <input type="number" value="${item.qty}" min="1"
                        onchange="updateQty(${idx}, this.value)"
                        class="w-10 text-center border rounded text-sm py-0.5">
                    <button onclick="updateQty(${idx}, ${item.qty + 1})" class="w-6 h-6 rounded bg-gray-200 text-sm hover:bg-gray-300">+</button>
                </div>
            </td>
            <td class="px-3 py-2 text-right text-sm font-medium">${money(item.price * item.qty)}</td>
            <td class="px-2 py-2">
                <button onclick="removeFromCart(${idx})" class="text-red-400 hover:text-red-600 text-lg">&times;</button>
            </td>`;
        body.appendChild(row);
    });
    recalculate();
}

function recalculate() {
    const discount = parseFloat(document.getElementById('discountInput')?.value) || 0;
    const subtotal = cart.reduce((s, i) => s + i.price * i.qty, 0);
    const afterDiscount = Math.max(0, subtotal - discount);
    const vat = afterDiscount * VAT_RATE;
    const total = afterDiscount + vat;
    setText('subtotal', money(subtotal));
    setText('vatAmount', money(vat));
    setText('grandTotal', money(total));
    setText('payDue', money(total));
    return { subtotal, discount, vat, total };
}

function setText(id, val) {
    const el = document.getElementById(id);
    if (el) el.textContent = val;
}

// ---- CUSTOMER ----
function selectCustomer(id, name, phone) {
    currentCustomer = { id, name, phone };
    updateCustomerDisplay();
    closeModal('customerModal');
}

function updateCustomerDisplay() {
    const el = document.getElementById('customerDisplay');
    if (el) el.innerHTML = '<span class="text-gray-400">&#128100;</span> ' + escapeHtml(currentCustomer.name);
}

async function searchCustomers(q) {
    const list = document.getElementById('customerList');
    if (!list) return;

    list.innerHTML = customerRow({ id: 0, name: 'Walk-in Customer', phone: 'No account' });
    if (!q || q.trim().length < 2) return;

    try {
        const data = await apiFetch('/api/customers/?search=' + encodeURIComponent(q.trim()));
        const customers = data.results || data;
        list.innerHTML = customerRow({ id: 0, name: 'Walk-in Customer', phone: 'No account' }) +
            customers.map(customerRow).join('');
    } catch (error) {
        list.insertAdjacentHTML('beforeend', '<p class="text-sm text-red-500 p-3">' + escapeHtml(error.message) + '</p>');
    }
}

function customerRow(customer) {
    const rawName = customer.name || '';
    const rawPhone = customer.phone || 'No account';
    const name = escapeHtml(rawName);
    const phone = escapeHtml(rawPhone);
    return `
        <div onclick="selectCustomer(${customer.id || 0}, '${escapeJsArg(rawName)}', '${escapeJsArg(rawPhone)}')"
            class="flex items-center gap-3 p-3 rounded-lg border hover:bg-blue-50 cursor-pointer">
            <div class="w-10 h-10 rounded-full bg-gray-200 flex items-center justify-center text-lg">&#128100;</div>
            <div>
                <p class="font-medium text-sm">${name}</p>
                <p class="text-xs text-gray-400">${phone}</p>
            </div>
        </div>`;
}

// ---- HOLD SALE ----
function holdSale() {
    if (cart.length === 0) { alert('Cart is empty'); return; }
    const note = prompt('Hold sale note (optional):') || 'Held Sale';
    heldSales.push({ id: Date.now(), note, cart: [...cart], customer: { ...currentCustomer }, time: new Date().toLocaleTimeString() });
    cart = [];
    renderCart();
    renderHeldSales();
    alert('Sale held: ' + note);
}

function resumeSale(idx) {
    if (cart.length > 0 && !confirm('Replace current cart with held sale?')) return;
    const held = heldSales[idx];
    cart = [...held.cart];
    currentCustomer = { ...held.customer };
    heldSales.splice(idx, 1);
    renderCart();
    updateCustomerDisplay();
    renderHeldSales();
    closeModal('holdSalesModal');
}

function renderHeldSales() {
    const el = document.getElementById('heldSalesList');
    if (!el) return;
    if (heldSales.length === 0) {
        el.innerHTML = '<p class="text-center text-gray-400 py-8">No held sales</p>';
        return;
    }
    el.innerHTML = heldSales.map((h, i) => `
        <div class="border rounded-lg p-3 flex justify-between items-center">
            <div>
                <p class="font-medium text-sm">${escapeHtml(h.note)}</p>
                <p class="text-xs text-gray-400">${escapeHtml(h.time)} &bull; ${escapeHtml(h.customer.name)} &bull; ${h.cart.length} items</p>
            </div>
            <div class="flex gap-2">
                <button onclick="resumeSale(${i})" class="bg-blue-600 text-white px-3 py-1 rounded text-xs">Resume</button>
                <button onclick="deleteHeld(${i})" class="bg-red-100 text-red-600 px-3 py-1 rounded text-xs">Delete</button>
            </div>
        </div>`).join('');
}

function deleteHeld(idx) {
    heldSales.splice(idx, 1);
    renderHeldSales();
}

// ---- PAYMENT ----
function setPayMethod(method) {
    currentPayMethod = method;
    ['cash','mpesa','card'].forEach(m => {
        const sec = document.getElementById(m + 'Section');
        if (sec) sec.classList.add('hidden');
        const btn = document.getElementById('btn' + m.charAt(0).toUpperCase() + m.slice(1));
        if (btn) btn.className = 'pay-method-btn bg-gray-100 text-gray-700 py-3 rounded-lg text-sm font-medium';
    });
    const activeSection = document.getElementById(method === 'split' ? 'cashSection' : method + 'Section');
    if (activeSection) activeSection.classList.remove('hidden');
    const activeBtn = document.getElementById('btn' + method.charAt(0).toUpperCase() + method.slice(1));
    if (activeBtn) activeBtn.className = 'pay-method-btn bg-green-600 text-white py-3 rounded-lg text-sm font-medium';
}

function calcChange() {
    const due = recalculate().total;
    const tendered = parseFloat(document.getElementById('cashTendered')?.value) || 0;
    const change = Math.max(0, tendered - due);
    setText('changeAmount', money(change));
}

async function completeSale() {
    if (cart.length === 0) { alert('Cart is empty'); return; }
    const totals = recalculate();
    if (currentPayMethod === 'cash') {
        const tendered = parseFloat(document.getElementById('cashTendered')?.value) || 0;
        if (tendered < totals.total) { alert('Amount tendered is less than total'); return; }
    }

    const checkoutButton = document.querySelector('#paymentModal button[onclick="completeSale()"]');
    if (checkoutButton) {
        checkoutButton.disabled = true;
        checkoutButton.textContent = 'Saving...';
    }

    try {
        const sale = await apiFetch('/api/pos-sales/', {
            method: 'POST',
            body: JSON.stringify({
                customer: currentCustomer.id || null,
                items: cart.map(item => ({
                    product: item.id,
                    quantity: item.qty,
                    unit_price: item.price,
                })),
                discount: totals.discount,
                vat: totals.vat,
                payment_method: currentPayMethod,
            }),
        });
        buildReceipt(totals, sale);
        closeModal('paymentModal');
        openModal('receiptModal');
    } catch (error) {
        alert(error.message);
    } finally {
        if (checkoutButton) {
            checkoutButton.disabled = false;
            checkoutButton.innerHTML = '&#10003; Complete Sale';
        }
    }
}

// ---- RECEIPT ----
function buildReceipt(totals, sale = {}) {
    const tendered = parseFloat(document.getElementById('cashTendered')?.value) || totals.total;
    const change = Math.max(0, tendered - totals.total);
    const mpesaCode = document.getElementById('mpesaCode')?.value || '';
    document.getElementById('receiptDate').textContent = new Date().toLocaleString();
    document.getElementById('receiptItems').innerHTML = cart.map(i =>
        '<div class="flex justify-between"><span>' + escapeHtml(i.name) + ' x' + i.qty + '</span><span>' + money(i.price * i.qty) + '</span></div>'
    ).join('');
    setText('rSubtotal', money(totals.subtotal));
    setText('rVat', money(totals.vat));
    setText('rTotal', money(totals.total));
    setText('rPaid', money(tendered));
    setText('rChange', money(change));
    setText('rPayMethod', sale.sale_number ? sale.sale_number + ' / ' + currentPayMethod.toUpperCase() : currentPayMethod.toUpperCase());
    const mpesaRow = document.getElementById('rMpesaRow');
    if (mpesaCode && mpesaRow) {
        mpesaRow.classList.remove('hidden');
        setText('rMpesa', mpesaCode);
    }
    cart = [];
    renderCart();
}

function printReceipt() {
    window.print();
}

// ---- SEARCH / BARCODE ----
function searchProducts(q) {
    document.querySelectorAll('.product-card').forEach(card => {
        card.style.display = card.dataset.name?.includes(q.toLowerCase()) ? '' : 'none';
    });
}

async function handleBarcode(e) {
    if (e.key !== 'Enter') return;

    const val = e.target.value.trim();
    if (!val) return;

    try {
        const data = await apiFetch('/api/products/?barcode=' + encodeURIComponent(val));
        const products = data.results || data;
        if (!products.length) {
            alert('Product not found for barcode: ' + val);
            return;
        }
        const product = products[0];
        addToCart(product.id, product.name, product.selling_price);
        e.target.value = '';
    } catch (error) {
        alert(error.message);
    }
}

function filterCategory(id) {
    document.querySelectorAll('.product-card').forEach(card => {
        card.style.display = (id === 'all' || card.dataset.category == id) ? '' : 'none';
    });
    document.querySelectorAll('.cat-btn').forEach(b => b.classList.remove('bg-blue-600','text-white'));
    event.target.classList.add('bg-blue-600','text-white');
}

// ---- MODALS ----
function openModal(id) {
    const m = document.getElementById(id);
    if (m) m.classList.remove('hidden');
}

function closeModal(id) {
    const m = document.getElementById(id);
    if (m) m.classList.add('hidden');
}

// ---- KEYBOARD SHORTCUTS ----
document.addEventListener('keydown', e => {
    if (e.target.tagName === 'INPUT') return;
    switch(e.key) {
        case 'F1': e.preventDefault(); document.getElementById('productSearch')?.focus(); break;
        case 'F2': e.preventDefault(); openModal('customerModal'); break;
        case 'F3': e.preventDefault(); holdSale(); break;
        case 'F5': e.preventDefault(); openModal('paymentModal'); break;
        case 'F6': e.preventDefault(); openModal('paymentModal'); break;
        case 'F7': e.preventDefault(); openModal('receiptModal'); break;
        case 'Escape': ['paymentModal','customerModal','holdSalesModal','receiptModal'].forEach(closeModal); break;
    }
});

document.addEventListener('DOMContentLoaded', () => {
    renderCart();
    setPayMethod('cash');
    document.getElementById('receiptDate') && (document.getElementById('receiptDate').textContent = new Date().toLocaleString());
});
