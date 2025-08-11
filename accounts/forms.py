from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserAddress, UserBankAccount
from django import forms 
from .constants import ACCOUNT_TYPE, GENDER_TYPE

# *** 3ta model er data ke combined kore ekta form(Registration_form) e convert kore fela ***

class UserRegistrationForm(UserCreationForm):
    account_type = forms.ChoiceField(
        choices=ACCOUNT_TYPE,
        required=True,
        widget=forms.Select(attrs={'required': 'required'})
    )
    birth_date = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={'required': 'required', 'type': 'date'})
    )
    gender = forms.ChoiceField(
        choices=GENDER_TYPE,
        required=True,
        widget=forms.Select(attrs={'required': 'required'})
    )
    street_address = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={'required': 'required'})
    )
    city = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'required': 'required'})
    )
    postal_code = forms.IntegerField(
        required=True,
        widget=forms.NumberInput(attrs={'required': 'required'})
    )
    country = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'required': 'required'})
    )
    # for css design ,, required field is needed
    first_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'required': 'required'})
    )
    last_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'required': 'required'})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'required': 'required'})
    )  
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email',
                  'account_type','birth_date','gender','street_address','postal_code','city','country',
                  'password1','password2'] # built-in field + manually fields combined
    
    # form.save()
    def save(self, commit=True):
        our_user = super().save(commit=False)    # ami database e data save krbona ekhn
        if commit == True:
            our_user.save()                      # user model e data save korlam
            account_type = self.cleaned_data.get('account_type')
            gender = self.cleaned_data.get('gender')
            street_address = self.cleaned_data.get('street_address')
            postal_code = self.cleaned_data.get('postal_code')
            city = self.cleaned_data.get('city')
            country = self.cleaned_data.get('country')
            birth_date = self.cleaned_data.get('birth_date')

            UserAddress.objects.create(
                user = our_user,
                street_address = street_address,
                postal_code = postal_code,
                city = city,
                country = country,
            )
            UserBankAccount.objects.create(
                user = our_user,
                account_type = account_type,
                gender = gender,
                birth_date = birth_date,
                account_no = 100000+ our_user.id
            )

        return our_user
    
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)

    #     for field in self.fields:
    #         self.fields[field].widget.attrs.update({
    #             'class': (
    #                 'appearance-none block w-full bg-gray-200 '
    #                 'text-gray-700 border border-gray-200 rounded '
    #                 'py-3 px-4 leading-tight focus:outline-none '
    #                 'focus:bg-white focus:border-gray-500'
    #             )
    #         })

    

class UserUpdateForm(forms.ModelForm):  #  ekhon combined hoye ekta model hoye geche
        account_type = forms.ChoiceField(
        choices=ACCOUNT_TYPE,
        required=True,
        widget=forms.Select(attrs={'required': 'required'})
        )
        birth_date = forms.DateField(
            required=True,
            widget=forms.DateInput(attrs={'required': 'required', 'type': 'date'})
        )
        gender = forms.ChoiceField(
            choices=GENDER_TYPE,
            required=True,
            widget=forms.Select(attrs={'required': 'required'})
        )
        street_address = forms.CharField(
            max_length=150,
            required=True,
            widget=forms.TextInput(attrs={'required': 'required'})
        )
        city = forms.CharField(
            max_length=100,
            required=True,
            widget=forms.TextInput(attrs={'required': 'required'})
        )
        postal_code = forms.IntegerField(
            required=True,
            widget=forms.NumberInput(attrs={'required': 'required'})
        )
        country = forms.CharField(
            max_length=100,
            required=True,
            widget=forms.TextInput(attrs={'required': 'required'})
        )
        first_name = forms.CharField(
            required=True,
            widget=forms.TextInput(attrs={'required': 'required'})
        )
        last_name = forms.CharField(
            required=True,
            widget=forms.TextInput(attrs={'required': 'required'})
        )
        email = forms.EmailField(
            required=True,
            widget=forms.EmailInput(attrs={'required': 'required'})
        )

        class Meta:
            model = User
            fields = ['username','first_name','last_name','email'] # egulai just change/update korte dilam
        

        # jodi user er account thake setai instance
        def __init__(self, *args, **kwargs):
           super().__init__(*args, **kwargs)

           if self.instance:
                try:
                   user_account = self.instance.account
                   user_address = self.instance.address
                except UserBankAccount.DoesNotExist:
                    user_account = None
                    user_address = None

                if user_account:
                    self.fields['account_type'].initial = user_account.account_type
                    self.fields['gender'].initial = user_account.gender
                    self.fields['birth_date'].initial = user_account.birth_date
                    self.fields['street_address'].initial = user_address.street_address
                    self.fields['city'].initial = user_address.city
                    self.fields['postal_code'].initial = user_address.postal_code
                    self.fields['country'].initial = user_address.country


        def save(self, commit=True):
            user = super().save(commit=False)    # ami database e data save krbona ekhn
            if commit == True:
                user.save()  

                user_account, created = UserBankAccount.objects.get_or_create(user = user)
                user_address, created = UserAddress.objects.get_or_create(user = user)

                user_account.account_type = self.cleaned_data['account_type']
                user_account.gender = self.cleaned_data['gender']
                user_account.birth_date = self.cleaned_data['birth_date']
                user_account.save()

                user_address.street_address = self.cleaned_data['street_address']
                user_address.city = self.cleaned_data['city']
                user_address.postal_code = self.cleaned_data['postal_code']
                user_address.country = self.cleaned_data['country']
                user_address.save()

            return user