from django.forms import Form, CharField, FileField, TextInput, PasswordInput, FileInput
from django.contrib.auth.forms import *
class LoginForm(AuthenticationForm):
	username = CharField(widget=TextInput(attrs={'class':'mdl-textfield__input', 'id':'username'}))
	password = CharField(widget=PasswordInput(attrs={'class':'mdl-textfield__input', 'id':'password'}))
	def clean(self):
        	username = self.cleaned_data.get('username')
        	password = self.cleaned_data.get('password')
        	user = authenticate(username=username, password=password)
        	if not user or not user.is_active:
            		raise forms.ValidationError("Sorry, username or password incorrect!")
        	return self.cleaned_data

class SubmissionForm(Form):	
	fileuploaded=FileField(widget=FileInput(attrs={'placeholder':'Please upload a file','class':'mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect', 'id':'uploadBtn'}))

class ChangePasswordForm(SetPasswordForm):
    """
    A form that lets a user change their password by entering their old
    password.
    """
    error_messages = dict(SetPasswordForm.error_messages, **{
        'password_incorrect': ("Your old password was entered incorrectly. "
                                "Please enter it again."),
    })
    old_password = forms.CharField(
        label=("Old password"),
        widget=forms.PasswordInput(attrs={'autofocus': ''}),
    )

    field_order = ['old_password', 'new_password1', 'new_password2']

    def clean_old_password(self):
        """
        Validates that the old_password field is correct.
        """
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise forms.ValidationError(
                self.error_messages['password_incorrect'],
                code='password_incorrect',
            )
        return old_password

	


