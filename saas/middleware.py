from .models import TenantDomain


class TenantMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        host = request.get_host()

        domain = TenantDomain.objects.filter(
            domain=host
        ).first()

        request.tenant = (
            domain.tenant
            if domain
            else None
        )

        return self.get_response(request)
