from django import forms
from django.core.exceptions import ValidationError
from .models import Post, Response


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        widget = {'title': forms.TextInput(attrs={'size': '100'})}
        fields = ['title', 'category', 'text']
        labels = {
            'content': 'Содержание - форматируйте текст, сохраняйте изображения и ссылки на Youtube'
        }

        def __init__(self):
            super().__init__()
            self.fields['category'].label = 'Категория'
            self.fields['title'].label = 'Заголовок'
            self.fields['text'].label = 'Контент'

        def clean(self):
            cleaned_data = super().clean()
            title, content = cleaned_data.get('title', ''), cleaned_data.get('content', '')
            if title is not None and title.lower() in content.lower():
                err_text = 'Избегайте повтора текста объявления в содержании.'
                raise ValidationError({'title': err_text})
            return cleaned_data

        def clean_title(self):
            title = self.cleaned_data['title']
            if title and title[0].islower():
                raise ValidationError('Начните объявление с заглавной буквы.')
            return title


class RespondForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ('text',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['text'].label = "Текст отклика:"


class ResponsesForm(forms.Form):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'] = forms.ModelChoiceField(
            label='Объявление',
            queryset=Post.objects.filter(author_id=user.id).order_by('-date').values_list('title', flat=True),
            empty_label="Все",
            required=False
        )
