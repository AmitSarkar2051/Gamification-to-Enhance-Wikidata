from django import forms


class HandleForm(forms.Form):
    handle = forms.CharField(max_length=40, label='Git Handle')
    handle_confirm = forms.CharField(max_length=40, label='Confirm Git Handle')

    def clean(self):
        cleaned_data = super().clean()  # inbuilt clean.

        handle_form = cleaned_data.get('handle')
        handle_form_confirm = cleaned_data.get('handle_confirm')

        if handle_form != handle_form_confirm:
            print('Not Equal')
            raise forms.ValidationError('Fields Do NOT match')

        # return handle_form


class GenreForm(forms.Form):
    genre = forms.CharField(max_length=100)
