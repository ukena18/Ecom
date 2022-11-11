from django import forms

#add some styles
def add_bootstrap(*frmObject):
    for i in frmObject:
        i.widget.attrs.update({'class':'form-control'});

class LoginForm(forms.Form):
    username = forms.CharField(max_length=25,label='Username')
    password = forms.CharField(max_length=20,label="Password",widget=forms.PasswordInput)
    add_bootstrap(username,password)
    


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=25, label="Username");
    
    password = forms.CharField(max_length=20 , label="Password",widget=forms.PasswordInput);
    confirm = forms.CharField(max_length=20,label='Confirm Password',widget=forms.PasswordInput)
    add_bootstrap(username,password,confirm);
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        confirm = self.cleaned_data.get('confirm')
        if password and confirm and password!=confirm:
            raise forms.ValidationError('Password is not the same');
        values={
            "username" : username,
            "password" : password
        }
        return values


