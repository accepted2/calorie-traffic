from django.shortcuts import redirect, render
from .models import Food, Consume
from django.contrib.auth.models import AnonymousUser

# Create your views here.


def index(request):
    foods = Food.objects.all()
    total_carbs = 0
    total_protein = 0
    total_calories = 0
    total_fats = 0

    # Если пользователь анонимный, мы не используем его как ссылку на пользователя, а просто None
    user = request.user if request.user.is_authenticated else None

    # Получаем все потребленные продукты для текущего пользователя
    if user:  # Если пользователь аутентифицирован
        consumed_food = Consume.objects.filter(user=user)
    else:  # Если пользователь анонимный, фильтруем только по None
        consumed_food = Consume.objects.filter(user=None)

    # Подсчёт общих макронутриентов
    for consumption in consumed_food:
        food_item = (
            consumption.food_consumed
        )  # Теперь это ForeignKey, поэтому это один объект
        total_carbs += food_item.carbs
        total_protein += food_item.protein
        total_calories += food_item.calories
        total_fats += food_item.fats

    context = {
        "total_carbs": total_carbs,
        "total_protein": total_protein,
        "total_calories": total_calories,
        "total_fats": total_fats,
        "foods": foods,
        "consumed_food": consumed_food,
    }

    if request.method == "POST":
        food_ids = request.POST.getlist(
            "food_consumed"
        )  # Получаем все выбранные ID продуктов

        for food_id in food_ids:
            food_item = Food.objects.get(id=food_id)
            consume = Consume(
                user=user, food_consumed=food_item, quantity=1
            )  # Создание новой записи
            consume.save()

        return redirect("home")

    return render(request, "mysite/index.html", context)


def delete_consume(request, pk):
    try:
        # Используем None для анонимных пользователей
        user = request.user if request.user.is_authenticated else None

        # Найти объект Consume по его ID и пользователю
        consume_food = Consume.objects.get(id=pk, user=user)

        if request.method == "POST":
            consume_food.delete()  # Удалить запись
            return redirect("home")

        return render(request, "mysite/delete.html", {"consume_food": consume_food})

    except Consume.DoesNotExist:
        return redirect("home")
    except MultipleObjectsReturned:
        return redirect("home")
