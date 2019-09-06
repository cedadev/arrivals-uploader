""" Rsync app forms. """

__author__ = "William Tucker"
__date__ = "2019-09-06"
__copyright__ = "Copyright 2019 United Kingdom Research and Innovation"
__license__ = "BSD - see LICENSE file in top-level package directory"


from django import forms


class RsyncPasswordChangeForm(forms.Form):
    
    password = forms.CharField(max_length=30, widget=forms.PasswordInput)
    password_repeat = forms.CharField(max_length=30, widget=forms.PasswordInput)
    
    def clean(self):
        password = self.cleaned_data.get('password')
        password_repeat = self.cleaned_data.get('password_repeat')
        
        if password != password_repeat:
            raise forms.ValidationError("Passwords don't match")
        
        return self.cleaned_data
