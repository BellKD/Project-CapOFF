from main.models import Basket

def basket_count(request):
    if request.user.is_authenticated:
        return {"basket_count": Basket.objects.filter(user=request.user).count()}
    return {"basket_count": 0}
