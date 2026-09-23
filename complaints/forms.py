from django import forms
from .models import Complaint

class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ["title", "category", "location", "description"]
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "e.g. Projector not working"}),
            "location": forms.TextInput(attrs={"placeholder": "e.g. Block B, Room 204"}),
            "description": forms.Textarea(attrs={"rows": 5, "placeholder": "Tell us what happened and what needs attention…"}),
        }

class UpdateForm(forms.Form):
    status = forms.ChoiceField(choices=Complaint.Status.choices)
    comment = forms.CharField(required=False, widget=forms.Textarea(attrs={"rows": 3, "placeholder": "Add a progress note for the student…"}))
