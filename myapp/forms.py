from django import forms
from .models import Job

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['company', 'role', 'status']

    def clean_status(self):
        status = self.cleaned_data.get('status')

        valid_status = ['Applied', 'Interview', 'Rejected', 'Selected']

        if status not in valid_status:
            raise forms.ValidationError("Invalid status selected")

        return status