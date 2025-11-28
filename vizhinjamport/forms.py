from django import forms
from .models  import *

from django.utils import timezone

CATEGORY_CHOICES = [
        ('','--- Select Product Category---'),
        ('Electronics', 'Electronics'),
        ('Furniture', 'Furniture'),

  
    ]
PRODUCT_CHOICES = {
    'Electronics': [
        ('Laptop&parts', 'Laptop & Parts'),
        ('electronic gadgets', 'Electronic Gadgets'),
        ('mobile phones', 'Mobile Phones'),
        ('television', 'Television'),
    ],
    'Furniture': [
        ('Chair', 'Chair'),
        ('Table', 'Table'),
         ('sofa', 'Sofa'),
        ('bed', 'Bed'),
    ],
}

CATEGORY = [
        ('','--- Select tender Category---'),
        ('Open', 'Open'),
        ('Closed', 'Closed'),

  
    ]

GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

DISTRICT_CHOICES = [
        ('', '--- Select District ---'),
        ('Thiruvananthapuram', 'Thiruvananthapuram'),
        ('Kollam', 'Kollam'),
        ('Pathanamthitta', 'Pathanamthitta'),
        ('Alappuzha', 'Alappuzha'),
        ('Kottayam', 'Kottayam'),
        ('Idukki', 'Idukki'),
        ('Ernakulam', 'Ernakulam'),
        ('Thrissur', 'Thrissur'),
        ('Palakkad', 'Palakkad'),
        ('Malappuram', 'Malappuram'),
        ('Kozhikode', 'Kozhikode'),
        ('Wayanad', 'Wayanad'),
        ('Kannur', 'Kannur'),
        ('Kasaragod', 'Kasaragod'),
    ]

class UserForm(forms.ModelForm):
    name=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),)
    contact=forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control'}),)
    district = forms.ChoiceField(   
        choices=DISTRICT_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="District"
    )
    city=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),)
    class Meta:
        model = User
        fields = ['name','contact','district','city']
        

class LoginForm(forms.ModelForm):
    # password = forms.CharField(widget=forms.PasswordInput())
    email=  forms.CharField(label="E-mail",widget=forms.EmailInput(attrs={'class':'form-control'}),)
    class Meta:  
      model = Login
      fields = ['email','password']
      widgets={
            'password':forms.PasswordInput(attrs={'class':'form-control'}),
        } 

class LoginEditForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
      
    class Meta:  
      model = Login
      fields = ['email'] 

class CompanyForm(forms.ModelForm):

    company_name = forms.CharField(
        label="Name of the Company",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    reg_no = forms.CharField(
        label="Register Number",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    district = forms.ChoiceField(
        choices=DISTRICT_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="District"
    )

    class Meta:
        model = Company
        fields = ['company_name', 'state', 'district', 'city', 'reg_no', 'contact']
        widgets = {
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'contact': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class ContractorForm(forms.ModelForm):
    dob = forms.DateField(
        label="Date of Birth",
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    reg_no = forms.CharField(
        label="Register Number",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    contact = forms.CharField(
        label="Mobile Number",
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    gender = forms.ChoiceField(
        choices=GENDER_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    district = forms.ChoiceField(
        choices=DISTRICT_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="District"
    )
    class Meta:
        model = Contractor
        fields = ['name', 'gender',  'dob', 'state','district', 'city', 'contact', 'reg_no']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'district': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
        }
class CustomLoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class ShipForm(forms.ModelForm):
    
    class Meta:
        model = Ship
        fields = ['shipcategory','shipname','source','destination']
        widgets={
            
            'shipcategory':forms.TextInput(attrs={'class':'form-control'}),
            'shipname':forms.TextInput(attrs={'class':'form-control'}),
            'source':forms.TextInput(attrs={'class':'form-control'}),
            'destination':forms.TextInput(attrs={'class':'form-control'}),
            
        }


class ExportForm(forms.ModelForm):
    productcategory = forms.ChoiceField(
        choices=CATEGORY_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'id_productcategory'})
    )
    productname = forms.ChoiceField(
        choices=[],  # start empty
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'id_productname'})
    )

    def __init__(self, *args, **kwargs):
        category = None
        if 'data' in kwargs:  # during POST
            category = kwargs['data'].get('productcategory')
        elif len(args) > 0:  # during bound form
            category = args[0].get('productcategory')

        super().__init__(*args, **kwargs)

        if category in PRODUCT_CHOICES:
            self.fields['productname'].choices = [('', '--- Select Product ---')] + PRODUCT_CHOICES[category]
        else:
            self.fields['productname'].choices = [('', '--- Select Product ---')]

    class Meta:
        model = Export
        fields = ['productcategory','productname','quantity','recipientname','recipientaddress','recipientcontact','recipientemail','source','destination']
        widgets = {
            'quantity': forms.TextInput(attrs={'class':'form-control'}),
            'recipientname': forms.TextInput(attrs={'class':'form-control'}),
            'recipientaddress': forms.TextInput(attrs={'class':'form-control'}),
            'recipientcontact': forms.NumberInput(attrs={'class':'form-control'}),
            'source': forms.TextInput(attrs={'class':'form-control'}),
            'destination': forms.TextInput(attrs={'class':'form-control'}),
            'recipientemail': forms.EmailInput(attrs={'class':'form-control'}),
        }
class ExportChargesForm(forms.ModelForm):
    productcategory = forms.ChoiceField(
        choices=CATEGORY_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    productname = forms.ChoiceField(
        choices=[],
        widget=forms.Select(attrs={'class': 'form-select'})
    )
 

    def __init__(self, *args, **kwargs):
       category = None
       if 'data' in kwargs:
          category = kwargs['data'].get('productcategory')
       elif len(args) > 0:
          category = args[0].get('productcategory')

       super().__init__(*args, **kwargs)

       self.fields['productname'].choices = [('', '--- Select Product ---')]

       if category and category in PRODUCT_CHOICES:
        self.fields['productname'].choices += PRODUCT_CHOICES[category]

    class Meta:
        model = ExportCharges
        fields = ['productcategory', 'productname','amount', 'tax']
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'tax': forms.NumberInput(attrs={'class': 'form-control'}),
        }

              
class PaymentForm(forms.ModelForm):
    
    class Meta:
        model = Payment
        fields = ['cardholder','cardno','cvv','expirydate','expiryyear']

class ComplaintForm(forms.ModelForm):
    
    class Meta:
        model = Complaint
        fields = ['subject','complaint','image']
        widgets={
            
            'subject':forms.TextInput(attrs={'class':'form-control'}),
            'complaint':forms.Textarea(attrs={'class':'form-control'}),
            'image':forms.ClearableFileInput(attrs={'class':'form-control'})
        }

class ComplaintReplyForm(forms.ModelForm):
    
    class Meta:
        model = Complaint
        fields = ['reply']
        widgets={
            'reply':forms.TextInput(attrs={'class':'form-control'}),
        }
class TenderForm(forms.ModelForm):
    category= forms.ChoiceField(choices=CATEGORY,widget=forms.Select(attrs={'class': 'form-select'}))
    last_date_apply=forms.DateField(label="Last Date To Apply",widget=forms.DateInput(attrs={'class':'form-control','type':'date'}))
    class Meta:
        model = Tender
        fields = ['category','name','discription','amount','no_of_month','last_date_apply']
        widgets={
            
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'discription':forms.Textarea(attrs={'class':'form-control'}),
            'amount':forms.NumberInput(attrs={'class':'form-control'}),
            'no_of_month':forms.NumberInput(attrs={'class':'form-control'}),
        }
    def __init__(self, *args, **kwargs):
           super().__init__(*args, **kwargs)
           today = timezone.now().date()
           self.fields['last_date_apply'].widget.attrs['min'] = today.strftime('%Y-%m-%d')

class AppliedTenderForm(forms.ModelForm):
    
    class Meta:
        model = AppliedTender
        fields = ['amount']
        widgets={
            'amount':forms.NumberInput(attrs={'class':'form-control'}),
        }

class TempJobForm(forms.ModelForm):
    
    class Meta:
        model = TempJob
        fields = ['name', 'category', 'discription', 'lastdateapply']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.TextInput(attrs={'class': 'form-control'}),
            'discription': forms.Textarea(attrs={'class': 'form-control'}),
            'lastdateapply': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        today = timezone.now().date()
        self.fields['lastdateapply'].widget.attrs['min'] = today.strftime('%Y-%m-%d')

class ApplyJobForm(forms.ModelForm):
    
    documents=forms.FileField(label="Add Certificates",widget=forms.ClearableFileInput(attrs={'class':'form-control'}))

    class Meta:

        model = ApplyJob
        fields = ['qualification','documents']
        widgets={
            
            'qualification':forms.TextInput(attrs={'class':'form-control'}),
            # 'documents':forms.ClearableFileInput(attrs={'class':'form-control'})
        }

class InterviewForm(forms.ModelForm):
    
    class Meta:
        model = Interview
        fields = ['time','date','discription']
        widgets={
            
            # 'venue':forms.TextInput(attrs={'class':'form-control'}),
            'discription':forms.Textarea(attrs={'class':'form-control'}),
            'time':forms.TimeInput(attrs={'type': 'time','class':'form-control',}),
            'date':forms.DateInput(attrs={'type': 'date','class':'form-control',}),
            }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        today = timezone.now().date()
        self.fields['date'].widget.attrs['min'] = today.strftime('%Y-%m-%d')


class NewsForm(forms.ModelForm):

    class Meta:
        model=News
        fields=['news']
        widgets={
            'news':forms.Textarea(attrs={'class':'form-control'}),
        }

class ShipTrackingForm(forms.ModelForm):
    
    class Meta:
        model = ShipTracking
        fields = ['currentlocation', 'time', 'date']
        widgets = {
            'currentlocation': forms.TextInput(attrs={'class': 'form-control'}),
            'time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        today = timezone.now().date()  # get today's date
        self.fields['date'].widget.attrs['min'] = today.strftime('%Y-%m-%d')
        
class AllComplaintForm(forms.ModelForm):
    
    class Meta:
        model = AllComplaint
        fields = ['complaint']
        widgets={
            
            'complaint':forms.Textarea(attrs={'class':'form-control'}),
            }
        
class AllComplaintReplyForm(forms.ModelForm):
    
    class Meta:
        model = AllComplaint
        fields = ['reply']
        widgets={
            
            'reply':forms.Textarea(attrs={'class':'form-control'}),
            }