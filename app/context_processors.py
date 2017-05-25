from app.models import DistanceDriven, Cost
from django.db.models import Sum
def footerRender(request):
    totalDistance = DistanceDriven.objects.aggregate(Sum('cumulativeMilesTraveled'))
    totalCost = Cost.objects.aggregate(Sum('cost'))
    return {
        'totalDistance' : totalDistance,
        'totalCost' : totalCost
        }
