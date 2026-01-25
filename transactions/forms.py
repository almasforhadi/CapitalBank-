from django import forms 
from .models import TransactionModel, UserBankAccount

class TransactionForm(forms.ModelForm):     # ei transaction form ta sudu inherit er jonno toiri kora
    class Meta:
        model = TransactionModel                   
        fields = ['amount', 'transaction_type']

    def __init__(self, *args, **kwargs):
        self.account = kwargs.pop('account')     # account value ke pop kore anlam
        super().__init__(*args, **kwargs)
        self.fields['transaction_type'].disabled = True              # ei field disable thakbe
        self.fields['transaction_type'].widget = forms.HiddenInput() # user er theke hide kora thakbe
    

    def save(self, commit = True):
        self.instance.account = self.account
        self.instance.balance_after_transaction = self.account.balance # initially koto rakhte cacchi :0 ---> 5000
        return super().save(commit=commit)
    



class DepositForm(TransactionForm):
     def clean_amount(self):  # clean diye inherit kore amount attribute take filter korlam
         min_diposit_amount = 100
         amount = self.cleaned_data.get('amount')  # user er amount ke catch korlam
         if amount < min_diposit_amount:
             raise forms.ValidationError(
                 f'You nedd to deposit al least {min_diposit_amount}'
             )
         return amount


class WithdrawForm(TransactionForm):

    def clean_amount(self):
         account = self.account
         min_withdraw_amount = 500
         max_withdraw_amount = 20000
         balance = account.balance
         amount = self.cleaned_data.get('amount')
         if amount < min_withdraw_amount:
             raise forms.ValidationError(
                 f'You can withdraw at least {min_withdraw_amount}$'
             )
         if amount > max_withdraw_amount:
             raise forms.ValidationError(
                 f'You can withdraw at most {max_withdraw_amount}$'
             )
         if amount > balance:
             raise forms.ValidationError(
                 f'You have {balance} $ in your account.'
                 'You cannot withdraw more than your account balance.'
             )
        
         return amount
    

class LoanRequestForm(TransactionForm):
    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        return amount
    



class TransferForm(TransactionForm):
    to_account_number = forms.CharField(label="Recipient Account Number")

    def clean_to_account_number(self):
        to_account_number = self.cleaned_data.get('to_account_number')
        try:
            self.to_account = UserBankAccount.objects.get(account_no=to_account_number)
        except UserBankAccount.DoesNotExist:
            raise forms.ValidationError("Recipient account not found.")
        if self.to_account == self.account:
            raise forms.ValidationError("You cannot transfer money to your own account.")
        return to_account_number

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount <= 0:
            raise forms.ValidationError("Transfer amount must be positive.")
        if amount > self.account.balance:
            raise forms.ValidationError("Insufficient balance to transfer.")
        return amount

    def save(self, commit=True):
        amount = self.cleaned_data['amount']

        # Deduct from sender balance
        self.account.balance -= amount
        self.account.save(update_fields=['balance'])

        # Add to receiver balance
        self.to_account.balance += amount
        self.to_account.save(update_fields=['balance'])

        # Save transaction record for sender
        self.instance.account = self.account
        self.instance.transaction_type = 5
        self.instance.balance_after_transaction = self.account.balance
        super().save(commit=commit)

        # Create transaction record for receiver
        TransactionModel.objects.create(
            account=self.to_account,
            amount=amount,
            balance_after_transaction=self.to_account.balance,
            transaction_type = 5,
        )

        return self.instance