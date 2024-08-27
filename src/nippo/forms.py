from django import forms


class NippoFormClass(forms.Form):
    title = forms.CharField(
        label="タイトル", widget=forms.TextInput(attrs={"placeholder": "タイトル..."})
    )
    content = forms.CharField(
        widget=forms.Textarea(attrs={"placeholder": "内容..."}), label="内容"
    )
