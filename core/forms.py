from django import forms
from django.forms import widgets

from core.models import City, Theme, Event


class FilterForm(forms.Form):
    city = forms.ModelChoiceField(label='Город', queryset=City.objects.all())
    start_bound = forms.DateTimeField(label='Начало с', input_formats=['%Y/%m/%d %H:%M'])
    end_bound = forms.DateTimeField(label='Начало до', input_formats=['%Y/%m/%d %H:%M'])
    themes = forms.ModelMultipleChoiceField(label='Темы', queryset=Theme.objects.all(),
                                            widget=widgets.CheckboxSelectMultiple())
