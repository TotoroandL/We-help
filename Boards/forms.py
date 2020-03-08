from django import forms
from Login.models import Topic,Post,Report,Contact

class NewTopicForm(forms.ModelForm):
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 5, 'placeholder': '想说点什么？'}
        ),
        max_length=3000,
        help_text='最大字数为3000。'
    )


    class Meta:
        model = Topic
        fields = ['subject', 'message',]

class PostForm(forms. ModelForm):
    class Meta:
        model = Post
        fields = ['message', ]

class ReportForm(forms. ModelForm):
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 5, 'placeholder': '您的举报原因？'}
        ),
        max_length=3000,
        help_text='最大字数为3000。')

    class Meta:
        model = Report
        fields = ['message',  ]

class ContactForm(forms. ModelForm):
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 3, 'placeholder': '您想对我们说点什么？'}
        ),
        max_length=400,
        help_text='最大字数为400.')

    class Meta:
        model = Contact
        fields = ['message']





