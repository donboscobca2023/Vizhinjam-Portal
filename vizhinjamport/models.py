from django.db import models

# Create your models here.


class Login(models.Model): 
    email=models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    usertype = models.CharField(max_length=100)
    status = models.IntegerField(default=0)
    


class User(models.Model):
    name = models.CharField(max_length=100)
    contact = models.IntegerField()
    district = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    login_id =models.ForeignKey(Login,on_delete=models.CASCADE)

class Company(models.Model):
    company_name = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    reg_no = models.CharField(max_length=100)
    contact = models.IntegerField()
    login_id =models.ForeignKey(Login,on_delete=models.CASCADE)

class Contractor(models.Model):
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    dob = models.DateField()
    district = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    reg_no = models.CharField(max_length=100)
    contact = models.IntegerField()
    login_id =models.ForeignKey(Login,on_delete=models.CASCADE)

class Ship(models.Model):
    shipcategory = models.CharField(max_length=100)
    shipname = models.CharField(max_length=100)
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    currentdate = models.DateField(auto_now_add=True)
    company_id =models.ForeignKey(Company,on_delete=models.CASCADE)
     
class Export(models.Model):
    productcategory = models.CharField(max_length=100)
    productname = models.CharField(max_length=100)
    quantity = models.IntegerField()
    recipientname = models.CharField(max_length=100)
    recipientaddress = models.CharField(max_length=100)
    recipientcontact = models.IntegerField()
    recipientemail = models.CharField(max_length=100)
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    publicid = models.ForeignKey(User,on_delete=models.CASCADE)
    shipid = models.ForeignKey(Ship,on_delete=models.CASCADE)
    currentdate = models.DateField(auto_now_add=True)
    paymentstatus = models.IntegerField(default=0) 
    cancelstatus = models.IntegerField(default=0)
    refundstatus = models.IntegerField(default=0)
    exportstatus = models.IntegerField(default=0) 
    def __str__(self):
        return f"{self.productcategory} - {self.productname} ({self.quantity})"

class ExportCharges(models.Model):
    company_id = models.ForeignKey(Company,on_delete=models.CASCADE)
    productcategory = models.CharField(max_length=100)
    productname = models.CharField(max_length=100)
    amount = models.IntegerField()
    tax = models.IntegerField()
    currentdate = models.DateField(auto_now_add=True)

class Payment(models.Model):
    cardholder=models.CharField(max_length=100)
    cardno=models.IntegerField()
    cvv=models.IntegerField()
    expirydate=models.IntegerField()
    expiryyear=models.IntegerField()
    amount=models.IntegerField()
    login_id =models.ForeignKey(Login,on_delete=models.CASCADE)
    currentdate = models.DateField(auto_now_add=True)

class Complaint(models.Model):
    subject=models.CharField(max_length=100)
    complaint=models.TextField(max_length=200)
    image=models.FileField(upload_to='complaints/')
    reply=models.TextField(null=True)
    export_id=models.ForeignKey(Export,on_delete=models.CASCADE)
    user_id=models.ForeignKey(User,on_delete=models.CASCADE)
    currentdate = models.DateField(auto_now_add=True)

class Tender(models.Model):
    category=models.CharField(max_length=100)
    name=models.CharField(max_length=100)
    discription=models.TextField(max_length=200)
    amount=models.IntegerField()
    no_of_month=models.IntegerField()
    last_date_apply=models.DateField()
    currentdate = models.DateField(auto_now_add=True)

class AppliedTender(models.Model):
    tender_id=models.ForeignKey(Tender,on_delete=models.CASCADE)
    contractor_id=models.ForeignKey(Contractor,on_delete=models.CASCADE)
    amount=models.IntegerField()
    currentdate = models.DateField(auto_now_add=True)
    applystatus = models.IntegerField(default=0)

class TempJob(models.Model):
    name=models.CharField(max_length=100)
    category=models.CharField(max_length=100)
    discription=models.TextField(max_length=247)
    lastdateapply=models.DateField()
    currentdate = models.DateField(auto_now_add=True)
    url = models.URLField(null=True)

class ApplyJob(models.Model):
    job_id=models.ForeignKey(TempJob,on_delete=models.CASCADE)
    user_id=models.ForeignKey(User,on_delete=models.CASCADE)
    qualification=models.CharField(max_length=100)
    documents=models.FileField(upload_to='documents/')
    currentdate = models.DateField(auto_now_add=True)
    status = models.IntegerField(default=0)

class Interview(models.Model):
    job_id=models.ForeignKey(TempJob,on_delete=models.CASCADE)
    time=models.TimeField()
    date=models.DateField()
    venue=models.CharField(max_length=100)
    discription=models.TextField(max_length=247)
    currentdate = models.DateField(auto_now_add=True)    

class News(models.Model):
    news=models.TextField()
    currentdate = models.DateField(auto_now_add=True)

class ShipTracking(models.Model):
    currentlocation=models.CharField(max_length=100)
    time=models.TimeField()
    date=models.DateField()
    ship_id=models.ForeignKey(Ship,on_delete=models.CASCADE)
    ship_status=models.IntegerField(default=0)

class AllComplaint(models.Model):
    login_id=models.ForeignKey(Login,on_delete=models.CASCADE)
    complaint=models.TextField()
    reply=models.TextField()
    currentdate=models.DateField(auto_now_add=True)
    