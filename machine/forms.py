from django.forms import ModelForm
from .models import MachineCategory


class MachineCategoryForm(ModelForm):
    class Meta:
        model = MachineCategory
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add custom CSS classes to form fields
        self.fields['parent'].widget.attrs = {
            'class': 'form-control',
        }
        self.fields['name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter name'})
        self.fields['description'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter description'})

