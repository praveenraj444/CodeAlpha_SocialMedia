from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Post, Comment


# ─────────────────────────────────────────────────────────
# REGISTER FORM (User Registration)
# ─────────────────────────────────────────────────────────
class UserRegisterForm(UserCreationForm):
    """
    User register panna form.
    Inherits from UserCreationForm (username, password1, password2).
    """
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email address'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Bootstrap styling for all fields
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Username'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm password'
        })


# ─────────────────────────────────────────────────────────
# USER UPDATE FORM (Username, Email edit)
# ─────────────────────────────────────────────────────────
class UserUpdateForm(forms.ModelForm):
    """Profile page-la username, email edit panna."""
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }


# ─────────────────────────────────────────────────────────
# PROFILE UPDATE FORM (Bio, Profile pic)
# ─────────────────────────────────────────────────────────
class ProfileUpdateForm(forms.ModelForm):
    """Bio + profile pic edit panna."""
    class Meta:
        model = Profile
        fields = ['bio', 'profile_pic']
        widgets = {
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Tell us about yourself...'
            }),
            'profile_pic': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
        }


# ─────────────────────────────────────────────────────────
# POST FORM (Create new post)
# ─────────────────────────────────────────────────────────
class PostForm(forms.ModelForm):
    """
    Post create panna form.
    Media options: Image upload, YouTube video, Instagram URL.
    Hidden fields: youtube_video_id, youtube_title, youtube_thumbnail
    """
    class Meta:
        model = Post
        fields = [
            'image',
            'instagram_url',
            'caption',
            'youtube_video_id',    # Hidden — JS fill pannum
            'youtube_title',       # Hidden
            'youtube_thumbnail',   # Hidden
        ]
        widgets = {
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
                'id': 'id_image'
            }),
            'instagram_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://www.instagram.com/reel/...',
                'id': 'id_instagram_url'
            }),
            'caption': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Write a caption...',
                'maxlength': 500
            }),
            # Hidden fields
            'youtube_video_id': forms.HiddenInput(attrs={'id': 'id_youtube_video_id'}),
            'youtube_title': forms.HiddenInput(attrs={'id': 'id_youtube_title'}),
            'youtube_thumbnail': forms.HiddenInput(attrs={'id': 'id_youtube_thumbnail'}),
        }

    # ─────────────────────────────────────────────────────
    # VALIDATION
    # ─────────────────────────────────────────────────────
    def clean_image(self):
        """Image size limit 5MB."""
        image = self.cleaned_data.get('image')
        if image:
            if image.size > 5 * 1024 * 1024:
                raise forms.ValidationError("Image size must be under 5 MB.")
        return image

    def clean_instagram_url(self):
        """Instagram URL validate pannu."""
        url = self.cleaned_data.get('instagram_url')
        if url:
            if 'instagram.com' not in url.lower():
                raise forms.ValidationError("Please enter a valid Instagram URL.")
        return url

    def clean(self):
        """
        Overall validation:
        At least ONE of these must be present:
        - image
        - youtube_video_id
        - instagram_url
        """
        cleaned_data = super().clean()
        image = cleaned_data.get('image')
        youtube_id = cleaned_data.get('youtube_video_id')
        instagram_url = cleaned_data.get('instagram_url')

        if not image and not youtube_id and not instagram_url:
            raise forms.ValidationError(
                "Please upload an image, select a YouTube video, or paste an Instagram URL."
            )
        return cleaned_data


# ─────────────────────────────────────────────────────────
# COMMENT FORM (Add comment)
# ─────────────────────────────────────────────────────────
class CommentForm(forms.ModelForm):
    """Comment add panna form (AJAX-ku)."""
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Add a comment...',
                'maxlength': 300,
                'autocomplete': 'off'
            }),
        }