from django.contrib.auth import get_user_model
from .models import UserProfile, RequestModel, MessageModel, CommentModel, SupportTicketModel,RemoveBan,UserTicketModel
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('email', 'username')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ('email', 'username')


class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ('first_name', 'last_name','image', 'bio')


class RequestForm(ModelForm):
    class Meta:
        model = RequestModel
        fields = ('title', 'description' )

class RequestChangeForm(ModelForm):
    class Meta:
        model = RequestModel
        fields = ('title', 'description' )

class MessageForm(ModelForm):
    class Meta:
        model = MessageModel
        fields = ('message',)


class CommentForm(ModelForm):
    class Meta:
        model = CommentModel
        fields = ('comment',)

class CommentChangeForm(ModelForm):
    class Meta:
        model = CommentModel
        fields = ('comment',)

# support ticket form
class SupportTicketForm(ModelForm):
    class Meta:
        model = SupportTicketModel
        fields = ('request_user','request','comment','message','description',)

class UserTicketForm(ModelForm):
    class Meta:
        model = UserTicketModel
        fields = ('description',)

class RemoveBanForm(ModelForm):
    class Meta:
        model = RemoveBan
        fields = ('message',)