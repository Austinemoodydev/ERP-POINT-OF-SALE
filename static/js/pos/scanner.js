// ============================================================
// POSERP — scanner.js  |  Barcode Scanner Engine
// ============================================================

document.addEventListener('DOMContentLoaded', () => {
    const barcodeInput = document.getElementById('barcodeInput');
    if (!barcodeInput) return;

    barcodeInput.addEventListener('keypress', e => {
        if (e.key === 'Enter') {
            e.preventDefault();
            searchBarcode(barcodeInput.value.trim());
            barcodeInput.value = '';
        }
    });
});

function searchBarcode(code) {
    if (!code) return;
    fetch(`/api/products/search/?barcode=${encodeURIComponent(code)}`)
        .then(res => {
            if (!res.ok) throw new Error('Product not found');
            return res.json();
        })
        .then(product => {
            addToCart({
                id:    product.id,
                name:  product.name,
                price: parseFloat(product.price),
                tax:   parseFloat(product.tax) || 0
            });
            showToast(`✅ ${product.name} added`, 'success');
        })
        .catch(() => {
            showToast(`❌ Barcode "${code}" not found`, 'danger');
        });
}

function showToast(message, type = 'info') {
    let container = document.getElementById('toastContainer');
    if (!container) {
        container = document.createElement('div');
        container.id = 'toastContainer';
        container.style.cssText = 'position:fixed;top:1rem;right:1rem;z-index:9999;';
        document.body.appendChild(container);
    }
    const toast = document.createElement('div');
    toast.className = `alert alert-${type} py-2 px-3 mb-1`;
    toast.innerText = message;
    container.appendChild(toast);
    setTimeout(() => toast.remove(), 2500);
}
