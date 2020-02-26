from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from .models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['tear', 'lol_id']
        widgets={
            'tear': forms.Select(
                attrs={'class':'tearbox'}
            ),
            'lol_id': forms.TextInput(
                attrs={'class':'tearbox'}
            )
        }

    def clean_renewal_date(self):
        tear = self.cleaned_data['tear']
        id = self.cleaned_data['lol_id']

        # Check if a date is not in the past.
        if tear is None:
            raise ValidationError(_('티어를 입력해 주세요.'))

        if id is None:
            raise ValidationError(_('롤 아이디를 입력해 주세요.'))

        # Remember to always return the cleaned data.
        return tear, id
