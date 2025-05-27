from django import forms


class PasswordlessAuthForm(forms.Form):
    name = forms.CharField()
    contact = forms.CharField()
    
    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        contact = cleaned_data.get('contact')
        
        if name and contact:
            # No password needed - we'll generate it automatically
            return cleaned_data
        raise forms.ValidationError("Both name and contact are required")