from django import forms

from .models import Contact, Comments


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'


class SubscriptionForm(forms.Form):
    name = forms.CharField(max_length=250)
    msg = forms.Textarea()
    email = forms.EmailField()


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['comment']
