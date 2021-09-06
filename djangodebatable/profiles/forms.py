from django import forms

from .models import Profile

class ProfileForm(forms.ModelForm):
	bio = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Bio here"}))

	class Meta:
		model = Profile
		fields = [
		'username',
		'bio'
		]

	def clean_username(self, *args, **kwargs):
		username = self.cleaned_data.get("username")
		if "ye" not in username:
			raise forms.ValidationError("nope.")
		return username
class RawProfileForm(forms.Form):
	username = forms.CharField()
	bio =  forms.CharField(required=False,
						widget=forms.Textarea(
							attrs={
								"rows": 10,
								"cols": 50,
								"placeholder": "Your bio..."
								}
							)
						)
