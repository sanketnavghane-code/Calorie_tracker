from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Food, Consume


def index(request):

    if request.method == "POST":
        food_consumed = request.POST.get('food_consumed')
        quantity = request.POST.get('quantity', 1.0)
        try:
            quantity = float(quantity)
        except ValueError:
            quantity = 1.0
        if food_consumed:
            try:
                food_obj = Food.objects.get(name=food_consumed)
            except Food.DoesNotExist:
                food_obj = None
            
            if request.user.is_authenticated and food_obj is not None:
                consume = Consume(user=request.user, food_consumed=food_obj, date=timezone.now().date(), quantity=quantity)
                consume.save()
                
        return redirect('/')

    foods = Food.objects.all()
   
    if request.user.is_authenticated:
        consumed_food = Consume.objects.filter(user=request.user, date=timezone.now().date())
    else:
        consumed_food = Consume.objects.none()

    return render(request, 'myapp/index.html', {'foods': foods, 'consumed_food': consumed_food})


def delete_consume(request, id):
    consumed_food = Consume.objects.get(id=id)
    if request.method == 'POST':
        consumed_food.delete()
        return redirect('/')
    return render(request, 'myapp/delete.html')
