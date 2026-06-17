from .models import BranchUser


class BranchMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if request.user.is_authenticated:

            branch = (
                BranchUser.objects
                .filter(
                    user=request.user,
                    is_default=True
                )
                .first()
            )

            request.branch = (
                branch.branch
                if branch
                else None
            )

        return self.get_response(request)
