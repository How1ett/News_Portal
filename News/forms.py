from django import forms
from django.core.exceptions import ValidationError
from .models import Post
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'type',
            'title',
            'text',
            'mat_rating',
            'author',
            'category'
        ]

        def clean(self):
            cleaned_data = super().clean()
            text = cleaned_data.get("text")
            if text is not None and len(text) < 20:
                raise ValidationError({
                    "text": "Текст не может быть менее 20 символов."
                })
            name = cleaned_data.get("name")
            if name == text:
                raise ValidationError({
                    "name": "Текст не должен быть идентичным заголовку."}
                )

            return cleaned_data


class NewsForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'type',
            'title',
            'text',
            'mat_rating',
            'author',
            'category'
        ]
        widgets = {'type': forms.HiddenInput()}

        def clean(self):
            cleaned_data = super().clean()
            text = cleaned_data.get("text")
            if text is not None and len(text) < 20:
                raise ValidationError({
                    "text": "Текст не может быть менее 20 символов."
                })
            name = cleaned_data.get("name")
            if name == text:
                raise ValidationError({
                    "name": "Текст не должен быть идентичным заголовку."}
                )

            return cleaned_data


class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user




#f = PostForm({'title': 'Заголовок формы тест', 'category': [1], 'mat_rating': 0, 'author': 1, 'text': 'Тест текста формы'})
