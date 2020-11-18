from django import forms


class GenreForm(forms.Form):
    '''
    Form to obtain the genre entered by the user
    '''
    genre = forms.CharField(max_length=100)


class QuizForm(forms.Form):
    '''
    Form to obtain the answer and reference entered by the user
    '''
    answer = forms.CharField(max_length=100, required=False)
    reference_url = forms.CharField(max_length=500, required=False)
    reference_file = forms.FileField(required=False)
