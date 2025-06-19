from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import ReadingGoal
from .forms import ReadingGoalForm
import datetime


@login_required
def goal_list(request):
    goals = ReadingGoal.objects.filter(user=request.user)

    # Get or create current year's goal
    current_year = datetime.datetime.now().year
    current_goal, created = ReadingGoal.objects.get_or_create(
        user=request.user, year=current_year, defaults={'target_books': 12})

    context = {
        'goals': goals,
        'current_goal': current_goal,
    }

    return render(request, 'goals/goal_list.html', context)


@login_required
def goal_create(request):
    if request.method == 'POST':
        form = ReadingGoalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = request.user

            # Check if goal for this year already exists
            existing_goal = ReadingGoal.objects.filter(user=request.user,
                                                       year=goal.year).first()

            if existing_goal:
                messages.warning(
                    request,
                    f'A goal for {goal.year} already exists. You can update it instead.'
                )
                return redirect('goal-update', pk=existing_goal.pk)

            goal.save()
            messages.success(
                request, f'Reading goal for {goal.year} created successfully!')
            return redirect('goal-list')
    else:
        form = ReadingGoalForm()

    return render(request, 'goals/goal_form.html', {
        'form': form,
        'title': 'Create Goal'
    })


@login_required
def goal_update(request, pk):
    goal = get_object_or_404(ReadingGoal, pk=pk, user=request.user)

    if request.method == 'POST':
        form = ReadingGoalForm(request.POST, instance=goal)
        if form.is_valid():
            form.save()
            messages.success(
                request, f'Reading goal for {goal.year} updated successfully!')
            return redirect('goal-list')
    else:
        form = ReadingGoalForm(instance=goal)

    return render(request, 'goals/goal_form.html', {
        'form': form,
        'title': 'Update Goal'
    })


@login_required
def goal_delete(request, pk):
    goal = get_object_or_404(ReadingGoal, pk=pk, user=request.user)

    if request.method == 'POST':
        goal.delete()
        messages.success(
            request, f'Reading goal for {goal.year} deleted successfully!')
        return redirect('goal-list')

    return render(request, 'goals/goal_confirm_delete.html', {'goal': goal})
