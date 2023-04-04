from django_filters.widgets import SuffixedMultiWidget
from django import forms

class OurDateRangeWidget(SuffixedMultiWidget):
    template_name = 'django_filters/widgets/multiwidget.html'
    suffixes = ['min', 'max']

    def __init__(self, attrs=None):
        widgets = (forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'style': 'font-size: 1.2em'}), forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'style': 'font-size: 1.2em'}))
        super().__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            return [value.start, value.stop]
        return [None, None]