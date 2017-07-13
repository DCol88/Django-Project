from django import forms
from .models import Post
 
 
class BlogPostForm(forms.ModelForm):
 
    class Meta:
        model = Post
        fields = ('title', 'content','image')


        #{'title': forms.TextInput(attrs={'placeholder': 'Title'}),
         #       'content': forms.Textarea(attrs={'placeholder': 'Your Submission..'}),
          #      'image'}