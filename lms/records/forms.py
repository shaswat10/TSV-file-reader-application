from . import models
from django import forms

# Form for taking the tsv file input
class TsvFileForm(forms.Form):
    tsv_file = forms.FileField( label="Upload File", widget= forms.FileInput(attrs={'name':'tsv_file', 'class':'form-control'}))