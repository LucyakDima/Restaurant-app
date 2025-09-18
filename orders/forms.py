from django import forms

class OrderForm(forms.Form):
    full_name = forms.CharField(label="Ваше імʼя", max_length=100)
    email = forms.EmailField(label="Електронна пошта")
    phone = forms.CharField(label="Телефон (необовʼязково)", max_length=20, required=False)
    payment_method = forms.ChoiceField(
        choices=[("card", "Оплата карткою"), ("cash", "Оплата при отриманні")],
        label="Спосіб оплати"
    )