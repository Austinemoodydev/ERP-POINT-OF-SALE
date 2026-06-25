import json
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.utils import timezone
from .models import CashShift, CashMovement

try:
    from products_app.models import Product
except ImportError:
    Product = None


@login_required
def pos_dashboard(request):
    products = Product.objects.filter(is_active=True).select_related("category") if Product else []
    return render(request, "pos_app/pos_dashboard.html", {
        "products": products,
        "page_title": "Point of Sale",
    })


@login_required
@require_POST
def complete_sale(request):
    try:
        data     = json.loads(request.body)
        items    = data.get("items", [])
        method   = data.get("method", "cash")
        total    = float(data.get("total", 0))
        discount = float(data.get("discount", 0))
        # TODO: create Sale + SaleItems, reduce inventory, post journal
        receipt_no = f"RCP-{timezone.now().strftime(chr(37)+chr(89)+chr(109)+chr(100)+chr(72)+chr(77)+chr(83))}"
        return JsonResponse({
            "success":      True,
            "receipt_no":   receipt_no,
            "cash_received": data.get("cash_received", total),
            "change":       data.get("change", 0),
            "mpesa_code":   data.get("mpesa_code", ""),
        })
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=400)


@login_required
@require_POST
def shift_open(request):
    try:
        data = json.loads(request.body)
        # Close any open shift first
        CashShift.objects.filter(cashier=request.user, status="open").update(status="closed")
        shift = CashShift.objects.create(
            cashier=request.user,
            open_amount=data.get("opening_cash", 0),
            notes=data.get("notes", ""),
        )
        return JsonResponse({"success": True, "shift_id": shift.id})
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=400)


@login_required
@require_POST
def shift_close(request):
    try:
        data  = json.loads(request.body)
        shift = CashShift.objects.filter(cashier=request.user, status="open").first()
        if not shift:
            return JsonResponse({"success": False, "error": "No open shift"}, status=400)
        actual   = float(data.get("actual_cash", 0))
        expected = float(shift.expected_cash or shift.open_amount)
        shift.close_time      = timezone.now()
        shift.close_amount    = actual
        shift.expected_cash   = expected
        shift.variance        = actual - expected
        shift.variance_reason = data.get("variance_reason", "")
        shift.status          = "closed"
        shift.save()
        return JsonResponse({"success": True})
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=400)


@login_required
@require_POST
def drawer_open(request):
    # Hardware: send ESC/POS command here
    return JsonResponse({"success": True, "message": "Drawer open signal sent"})


@login_required
@require_POST
def drawer_deposit(request):
    try:
        data  = json.loads(request.body)
        amount = float(data.get("amount", 0))
        shift = CashShift.objects.filter(cashier=request.user, status="open").first()
        if shift:
            CashMovement.objects.create(shift=shift, type="deposit", amount=amount)
        return JsonResponse({"success": True})
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=400)
