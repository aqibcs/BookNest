from django import forms
from .models import ReadingGoal
import datetime


class ReadingGoalForm(forms.ModelForm):
    current_year = datetime.datetime.now().year
    year = forms.ChoiceField(
        choices=[(r, r) for r in range(current_year - 5, current_year + 6)],
        initial=current_year
    )
    
    class Meta:
        model = ReadingGoal
        fields = ['year', 'target_books']
