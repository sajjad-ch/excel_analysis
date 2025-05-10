from django import forms
from .models import UserFiles


class FileForm(forms.ModelForm):
    class Meta:
        model = UserFiles
        fields = ['file',]


class PlotForm(forms.Form):
    kind = forms.ChoiceField(
        choices=[
            ('scatter', 'Scatter Plot'),
            ('hist', 'Histogram'),
            ('pie', 'Pie Chart'),
            ('bar', 'Bar Chart'),
        ]
    )
    x_axis = forms.CharField(max_length=120, required=True)
    y_axis = forms.CharField(max_length=120, required=True)

    def clean(self):
        cleaned_data = super().clean()
        kind = cleaned_data.get("kind")
        x_axis = cleaned_data.get("x_axis")
        y_axis = cleaned_data.get("y_axis")

        if kind == 'pie' and not x_axis:
            raise forms.ValidationError("Pie plots require an x-axis field.")
        elif kind != 'pie' and (not x_axis or not y_axis):
            raise forms.ValidationError(f"{kind.capitalize()} plots require both x-axis and y-axis fields.")
        return cleaned_data
