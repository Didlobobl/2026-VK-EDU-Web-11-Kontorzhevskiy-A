from django import forms
from .models import Question, Answer, Tag

class AskForm(forms.ModelForm):
    tag_string = forms.CharField(label="Теги", required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Question
        fields = ['title', 'text']

    def clean_tag_string(self):
        tags = self.cleaned_data.get('tag_string', '')
        tag_list = [t.strip() for t in tags.split(',') if t.strip()]
        if len(tag_list) > 3:
            raise forms.ValidationError("Нельзя указать больше 3 тегов.")
        return tag_list

    def save(self, user, commit=True):
        question = super().save(commit=False)
        question.author = user 
        if commit:
            question.save()
            tag_list = self.cleaned_data['tag_string']
            for tag_name in tag_list:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                question.tags.add(tag)
        return question

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text']