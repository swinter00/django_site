from django import forms
from django.core.files.uploadedfile import InMemoryUploadedFile
from jamup.humanize import naturalsize
from jamup.models import Post, Profile, Message


# Create the form class.
class CreateForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'city', 'state', 'reason', 'text']

class ReplyForm(forms.Form):
    reply = forms.CharField(required=True, max_length=500, min_length=3, strip=True)

class ProfileCreateForm(forms.ModelForm):
    max_upload_limit = 2 * 1024 * 1024
    max_upload_limit_text = naturalsize(max_upload_limit)

    # Call this 'picture' so it gets copied from the form to the in-memory model
    # It will not be the "bytes", it will be the "InMemoryUploadedFile"
    # because we need to pull out things like content_type
    picture = forms.FileField(required=False, label='File to Upload <= '+max_upload_limit_text)
    upload_field_name = 'picture'

    class Meta:
        model = Profile
        fields = ['name', 'picture', 'city', 'state', 'bio', 'genres', 'instruments', 'private']
        labels = {'picture': 'Upload a profile picture (portrait images look best!)', 'private': 'Checking this box will prevent your profile from appearing on the profiles page'}


    # Validate the size of the picture
    def clean(self):
        cleaned_data = super().clean()
        pic = cleaned_data.get('picture')
        if pic is None:
            return
        if len(pic) > self.max_upload_limit:
            self.add_error('picture', "File must be < "+self.max_upload_limit_text+" bytes")

    # Convert uploaded File object to a picture
    def save(self, commit=True):
        instance = super(ProfileCreateForm, self).save(commit=False)

        # We only need to adjust picture if it is a freshly uploaded file
        f = instance.picture   # Make a copy
        if isinstance(f, InMemoryUploadedFile):  # Extract data from the form to the model
            bytearr = f.read()
            instance.content_type = f.content_type
            instance.picture = bytearr  # Overwrite with the actual image data

        if commit:
            instance.save()

        return instance

class MessageCreateForm(forms.ModelForm):

    class Meta:
        model = Message
        fields = ['recipient', 'text']