from django.shortcuts import redirect, render
from .models import Food, Consume


# Create your views here.
def index(request):
    foods = Food.objects.all()
    total_carbs = 0
    total_protein = 0
    total_calories = 0
    total_fats = 0

    # Получаем все потребленные продукты для текущего пользователя
    consumed_food = Consume.objects.filter(user=request.user)

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
        )  # Изменено на getlist для получения всех выбранных ID

        for food_id in food_ids:
            food_item = Food.objects.get(id=food_id)
            consume = Consume(
                user=request.user, food_consumed=food_item, quantity=1
            )  # Создание новой записи
            consume.save()

        return redirect("home")

    return render(request, "mysite/index.html", context)


def delete_consume(request, pk):
    try:
        # Найти объект Consume по его ID и пользователю
        consume_food = Consume.objects.get(id=pk, user=request.user)

        if request.method == "POST":
            consume_food.delete()  # Удалить запись
            return redirect("home")

        return render(request, "mysite/delete.html", {"consume_food": consume_food})

    except Consume.DoesNotExist:
        return redirect("home")
    except MultipleObjectsReturned:
        return redirect("home")
