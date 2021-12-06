from django import forms

class CommentForm(forms.Form):
    message = forms.CharField(widget = forms.Textarea)
    name = forms.CharField(label='Your name', max_length=100)
    email = forms.EmailField(max_length=100)
    # phone_number = forms.CharField(widget = forms.NumberInput)
