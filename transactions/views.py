from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.views.generic import CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import TransactionModel
from .forms import DepositForm, WithdrawForm, LoanRequestForm, TransferForm
from .constants import DEPOSIT, WITHDRAWAL, LOAN, LOAN_PAID, TRANSFER
from django.contrib import messages
from datetime import datetime
from django.db.models import Sum
from django.views import View
from django.urls import reverse_lazy
from .models import TransactionModel
#email
from django.core.mail import EmailMessage , EmailMultiAlternatives
from django.template.loader import render_to_string



def send_transaction_email(user, amount, subject, template):
    try:
        message = render_to_string(template, {
            'user': user,
            'amount': amount,
        })

        send_email = EmailMultiAlternatives(
            subject=subject,
            body='',
            to=[user.email]
        )
        send_email.attach_alternative(message, "text/html")
        send_email.send(fail_silently=True)  # ⭐ IMPORTANT

    except Exception as e:
        # Optional: log error
        print("Email sending failed:", e)




# ei view ke inherit kore amra deposit, withdraw, loan request er kaj korbo
class TransactionCreateMixin(LoginRequiredMixin, CreateView):
     template_name = 'transactions/transaction_form.html'
     model = TransactionModel
     title = ''
     success_url = reverse_lazy('transaction_report')

     def get_form_kwargs(self):
          kwargs = super().get_form_kwargs()
          kwargs.update({
               'account' : self.request.user.account,
          })
          return kwargs
     
     def get_context_data(self, **kwargs):
          context = super().get_context_data(**kwargs)
          context.update({
               'title' : self.title
          })
          return context

class DepositMoneyView(TransactionCreateMixin):
      form_class = DepositForm
      title = 'Deposit'

      def get_initial(self):
           initial = {'transaction_type' : DEPOSIT}
           return initial
      
      def form_valid(self, form):
          amount = form.cleaned_data.get('amount')
          account = self.request.user.account

          account.balance += amount  # user er kache ase 500tk, depost korlo 1000tk.Total ac-balance = 1500
          account.save(update_fields = ['balance'])

          form.instance.account = account
          form.instance.transaction_type = DEPOSIT
          form.instance.balance_after_transaction = account.balance  # set balance after transaction

          messages.success(self.request,f'{amount}$ is deposited to your account successfully')
          send_transaction_email(self.request.user, amount, "Deposit messages", "transactions/deposite_email.html")
          return super().form_valid(form)
      


class WithdrawMoneyView(TransactionCreateMixin):
      form_class = WithdrawForm
      title = 'Withdraw Money'

      def get_initial(self):
           initial = {'transaction_type' : WITHDRAWAL}
           return initial
      
      def form_valid(self, form):
          amount = form.cleaned_data.get('amount')
          account = self.request.user.account

          account.balance -= amount  # user er kache ase 1500tk, withdraw korlo 1000tk.Total ac-balance = 500
          account.save(update_fields = ['balance'])

          form.instance.account = account
          form.instance.transaction_type = WITHDRAWAL
          form.instance.balance_after_transaction = account.balance  # ✅ set balance after transaction

          messages.success(self.request,f'Successfully Withdrawn {amount}$ from your account')
          send_transaction_email(self.request.user, amount, "Withdrawal messages", "transactions/withdrawal_email.html")
          return super().form_valid(form)
      


class LoanRequestView(TransactionCreateMixin):
      form_class = LoanRequestForm
      title = 'Request For LOAN'

      def get_initial(self):
           initial = {'transaction_type' :LOAN}
           return initial
      
      def form_valid(self, form):
          amount = form.cleaned_data.get('amount')
          current_loan_count = TransactionModel.objects.filter(account = self.request.user.account, transaction_type = 3, loan_approve = True).count()

          if current_loan_count >= 3:
               return HttpResponse("You have crossed your limits.")
          
          form.instance.account = self.request.user.account
          form.instance.transaction_type = LOAN
          form.instance.balance_after_transaction = self.request.user.account.balance  # set balance after transaction

          messages.success(self.request,f'Your loan request ${amount} is sent.Wait for response.')
          send_transaction_email(self.request.user, amount, "Loan Request messages", "transactions/loan_email.html")
          return super().form_valid(form)



class TransactionReportView(LoginRequiredMixin, ListView):
     template_name = 'transactions/transaction_report.html'
     model = TransactionModel
     balance = 0
     context_object_name = "report_list"

     def get_queryset(self):
          # jodi user kono transaction_type filter na kore tahole tar total transaction report dekhabe.
          queryset = super().get_queryset().filter(
              account = self.request.user.account
          )
          start_date_str = self.request.GET.get('start_date')
          end_date_str = self.request.GET.get('end_date')

           # date filter kore report dekha
          if start_date_str and end_date_str:   
               start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
               end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
               
               queryset = queryset.filter(
                    time_stamp__date__gte=start_date,
                    time_stamp__date__lte=end_date
               )

               # Important: filter by the same user's account, or total sum of all users will be shown!
               self.balance = TransactionModel.objects.filter(
                    account=self.request.user.account,
                    time_stamp__date__gte=start_date,
                    time_stamp__date__lte=end_date
               ).aggregate(Sum('amount'))['amount__sum'] or 0

          else:
               self.balance = self.request.user.account.balance

          return queryset.distinct()
     

     def get_context_data(self, **kwargs):
          context = super().get_context_data(**kwargs)
          context.update({
               'account' : self.request.user.account
          })
          return context
              

class PayLoanView(LoginRequiredMixin, View):
     def get(self, request, loan_id):
          loan = get_object_or_404(TransactionModel, id=loan_id)

          if loan.loan_approve:
               user_account = loan.account
               if loan.amount <= user_account.balance:
                    user_account.balance -= loan.amount
                    loan.balance_after_transaction = user_account.balance
                    user_account.save()
                    loan.transaction_type = LOAN_PAID
                    loan.save()
                    messages.success(request, f'Loan of {loan.amount}$ paid successfully.')
               else:
                    messages.error(request, 'Loan amount is greater than available balance')
          else:
               messages.error(request, 'Loan is not approved yet.')
          return redirect('loan_list')

          


class LoanListView(LoginRequiredMixin, ListView):
     model = TransactionModel
     template_name = 'transactions/loan_request.html'
     context_object_name = 'loans'

     def get_queryset(self):
          user_account = self.request.user.account
          queryset = TransactionModel.objects.filter(account = user_account, transaction_type = LOAN)
          return queryset
     



class TransferMoneyView(TransactionCreateMixin):
    form_class = TransferForm
    title = 'Transfer Money'

    def get_initial(self):
        return {'transaction_type': TRANSFER}

    def form_valid(self, form):
        sender_account = self.request.user.account
        receiver_account = form.cleaned_data['to_account']
        amount = form.cleaned_data['amount']

        # ❌ Prevent self transfer
        if sender_account == receiver_account:
            messages.error(self.request, "You cannot transfer money to your own account.")
            return redirect('transfer_money')

        # ❌ Insufficient balance check
        if sender_account.balance < amount:
            messages.error(self.request, "Insufficient balance.")
            return redirect('transfer_money')

        # ✅ Update balances
        sender_account.balance -= amount
        receiver_account.balance += amount

        sender_account.save(update_fields=['balance'])
        receiver_account.save(update_fields=['balance'])

        # ✅ Sender transaction record
        form.instance.account = sender_account
        form.instance.transaction_type = TRANSFER
        form.instance.balance_after_transaction = sender_account.balance

        # ✅ Success message
        messages.success(
            self.request,
            f'Successfully transferred {amount}$ to {receiver_account.user.username}'
        )

        return super().form_valid(form)

