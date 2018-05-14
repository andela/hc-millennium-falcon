from django import forms
from hc.help.models import Faqs

class FaqForm(forms.Form):
    question = forms.CharField(max_length=500, required=False)
    answer = forms.CharField(max_length=1000, required=False)
    class Meta:
        model = Faqs
        fields = ('question', 'answer',)

