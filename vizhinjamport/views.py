from genericpath import exists
from django.shortcuts import render, redirect,get_object_or_404
from .forms import *
from .models import *
from django.db.models import Q
from django.contrib import messages
from datetime import date
# Create your views here.


def landing(request):
    return render(request,'landing.html')

def reg(request):
    return render(request,'reg.html')

def register_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        form1 = LoginForm(request.POST)
        if form.is_valid() and form1.is_valid():
            a=form1.save(commit=False)
            a.usertype="public"
            a.save()
            b=form.save(commit=False)
            b.login_id=a
            b.save()
            messages.success(request,'registeration successful!')
            return redirect('landing')
    else:
        form = UserForm()
        form1 = LoginForm()   
    return render(request,'register.html',{'form':form,'form1':form1}) 

def register_company(request):
    if request.method == 'POST':
        form = CompanyForm(request.POST)
        form1= LoginForm(request.POST)
        if form.is_valid() and form1.is_valid():
            a=form1.save(commit=False)
            a.usertype="company"
            a.save()
            b=form.save(commit=False)
            b.login_id=a
            b.save()
            messages.success(request,'registeration successful!')
            return redirect('landing')
    else:
        form = CompanyForm()
        form1 = LoginForm()   
    return render(request,'compreg.html',{'form':form,'form1':form1})

def register_contractor(request):
    if request.method == 'POST':
        form = ContractorForm(request.POST)
        form1= LoginForm(request.POST)
        if form.is_valid() and form1.is_valid():
            a=form1.save(commit=False)
            a.usertype="contractor"
            a.save()
            b=form.save(commit=False)
            b.login_id=a
            b.save()
            messages.success(request,'registeration successful!')
            return redirect('landing')
    else:
        form = ContractorForm()
        form1 = LoginForm()   
    return render(request,'contractor_reg.html',{'form':form,'form1':form1})

def user_list(request):
    users = User.objects.all()
    return render(request,'admin_user.html',{'users':users})

def company_list(request):
    companys = Company.objects.all()
    return render(request,'admin_company.html',{'companys':companys})

def contractor_list(request):
    contractors = Contractor.objects.all()
    return render(request,'admin_contractor.html',{'contractors':contractors})

def login(request):
    if request.method=='POST':
        print(2)
        form=CustomLoginForm(request.POST)
        if form.is_valid():
            email=form.cleaned_data['email']
            password=form.cleaned_data['password']
            if email=="admin@gmail.com" and password =="admin123":
                return redirect('dash')
            try:
                data=Login.objects.get(email=email,password=password)
                if data.usertype=="public":
                    request.session['user_id']=data.id
                    return redirect('userhome')
                elif data.usertype=="company" and data.status==1:
                    request.session['company_id']=data.id
                    return redirect('companyhome')
                elif data.usertype=="contractor" and data.status==1:
                    request.session['contractor_id']=data.id
                    return redirect('contractorhome')
                else:
                    return render (request,'loginform.html',{"msg":"waiting for approval",'form':form})
            except Login.DoesNotExist:

                return render (request, 'loginform.html',{"msg":"invalid email or password",'form':form})
    else:
        form=CustomLoginForm()
    return render(request,'loginform.html',{'form':form})

def userhome(request):
    return render(request,'userhome.html')

def companyhome(request):
    return render(request,'companyhome.html')

def contractorhome(request):
    return render(request,'contractorhome.html')

def register_ship(request):
    id=request.session.get('company_id')
    if not id:
         return redirect('userlogin')
    compid=Company.objects.get(login_id=id)
    if request.method == 'POST':
        form = ShipForm(request.POST)
        if form.is_valid():      
            b=form.save(commit=False)
            b.company_id=compid
            b.save()
            messages.success(request,'registeration successful!')
            return redirect('companyhome')
    else:
        form = ShipForm()   
    return render(request,'ship_reg.html',{'form':form})

def ship_list(request):
    id=request.session.get('company_id')
    if not id:
         return redirect('userlogin')
    ships = Ship.objects.filter(company_id__login_id=id)

    return render(request,'ship_list.html',{'ships':ships}) 

def edit_ship(request,id):
    cid=request.session.get('company_id')
    if not cid:
         return redirect('userlogin')
    ship = get_object_or_404(Ship,id=id)
    
    if request.method == 'POST':
        form = ShipForm(request.POST,instance=ship)
        if form.is_valid():
            form.save()
            messages.success(request,'editing successful!')
            return redirect('ship_list')
    else:
        form = ShipForm(instance=ship)   
    return render(request,'ship_edit.html',{'form':form})

def delete_ship(request,id):
    ship = get_object_or_404(Ship,id=id)
    ship.delete()
    return redirect('ship_list')

# def ship_user(request):
#     ships = Ship.objects.all()
#     return render(request,'ship_user.html',{'ships':ships}) 
from django.db.models import OuterRef, Subquery

def search_ship(request):
    id=request.session.get('user_id')
    if not id:
         return redirect('userlogin')
    query = request.GET.get('q')
    ships = Ship.objects.all()

    if query:
        ships = ships.filter(
            Q(shipcategory__icontains=query) |
            Q(shipname__icontains=query) |
            Q(source__icontains=query) |
            Q(destination__icontains=query)
        )

    # Subquery: get latest ship_status from ShipTracking
    latest_tracking = ShipTracking.objects.filter(
        ship_id=OuterRef('pk')
    ).order_by('-date', '-time')

    ships = ships.annotate(
        latest_status=Subquery(latest_tracking.values('ship_status')[:1])
    )

    return render(request, 'ship_user.html', {'ships': ships, 'query': query})

def edit_user(request):
    id=request.session.get('user_id')
    if not id:
         return redirect('userlogin')
    user=User.objects.get(login_id=id)
    log=Login.objects.get(id=id)
    
    if request.method == 'POST':
        form = UserForm(request.POST,instance=user)
        form1 = LoginEditForm(request.POST,instance=log)
        if form.is_valid() and form1.is_valid():
            form.save()
            form1.save()
            messages.success(request,'updation successful!')
            return redirect('userhome')
    else:
        form = UserForm(instance=user)
        form1 = LoginEditForm(instance=log)   
    return render(request,'user_edit.html',{'form':form,'form1':form1})

def edit_company(request):
    id=request.session.get('company_id')
    if not id:
         return redirect('userlogin')
    comp=Company.objects.get(login_id=id)
    log=Login.objects.get(id=id)
    
    if request.method == 'POST':
        form = CompanyForm(request.POST,instance=comp)
        form1 = LoginEditForm(request.POST,instance=log)
        if form.is_valid() and form1.is_valid():
            form.save()
            form1.save()
            messages.success(request,'updation successful!')
            return redirect('companyhome')
    else:
        form = CompanyForm(instance=comp)
        form1 = LoginEditForm(instance=log)   
    return render(request,'company_edit.html',{'form':form,'form1':form1})

def edit_contractor(request):
    id=request.session.get('contractor_id')
    if not id:
         return redirect('userlogin')
    tend=Contractor.objects.get(login_id=id)
    log=Login.objects.get(id=id)
    
    if request.method == 'POST':
        form = ContractorForm(request.POST,instance=tend)
        form1 = LoginEditForm(request.POST,instance=log)
        if form.is_valid() and form1.is_valid():
            form.save()
            form1.save()
            messages.success(request,'updation successful!')
            return redirect('contractorhome')
    else:
        form = ContractorForm(instance=tend)
        form1 = LoginEditForm(instance=log)   
    return render(request,'contractor_edit.html',{'form':form,'form1':form1})

def export(request,id):
    uid=request.session.get('user_id')
    if not uid:
         return redirect('userlogin')
    user=User.objects.get(login_id=uid)
    ship = get_object_or_404(Ship,id=id)

    if request.method == 'POST':
        form = ExportForm(request.POST)
        if form.is_valid():      
            b=form.save(commit=False)
            b.publicid=user
            b.shipid=ship
            b.exportstatus=1
            
            b.save()
            messages.success(request,'export registeration successful!')
            return redirect('payment',pid=b.id)
    else:
        form = ExportForm()   
    return render(request,'export.html',{'form':form})

def export_list(request):
    id = request.session.get('user_id')
    if not id:
         return redirect('userlogin')
    userid=User.objects.get(login_id=id)
    exports = Export.objects.filter(publicid=userid)
    return render(request,'export_list.html',{'exports':exports})

def edit_export(request,id):
    uid = request.session.get('user_id')
    if not uid:
         return redirect('userlogin')
    expo = get_object_or_404(Export,id=id)

    
    if request.method == 'POST':
        form = ExportForm(request.POST,instance=expo)
        if form.is_valid():
            form.save()
            messages.success(request,'editing successful!')
            return redirect('export_list')
    else:
        form = ExportForm(instance=expo)   
    return render(request,'export_edit.html',{'form':form})

def cancel_export(request,id):
    expo = get_object_or_404(Export,id=id)
    expo.cancelstatus=1
    expo.save()
    return redirect('export_list')

def export_comp_list(request):
    id = request.session.get('company_id')
    if not id:
         return redirect('userlogin')
    compid=Company.objects.get(login_id=id)

    exports = Export.objects.filter(shipid__company_id=compid.id,paymentstatus=1)
    print(exports)
    return render(request,'export_comp_list.html',{'exports':exports})

def admin_header(request):
    return render(request,'admin_header.html')

def company_approve(request,id):
    log = get_object_or_404(Login,id=id)
    log.status=1
    log.save()
    return redirect('company_list')

def company_reject(request,id):
    log = get_object_or_404(Login,id=id)
    log.status=2
    log.save()
    return redirect('company_list')

def contractor_approve(request,id):
    log = get_object_or_404(Login,id=id)
    log.status=1
    log.save()
    return redirect('contractor_list')

def contractor_reject(request,id):
    log = get_object_or_404(Login,id=id)
    log.status=2
    log.save()
    return redirect('contractor_list')

def exportcharges(request):
    id=request.session.get('company_id')
    if not id:
         return redirect('userlogin')
    compid=Company.objects.get(login_id=id)
    if request.method == 'POST':
        form = ExportChargesForm(request.POST)
        if form.is_valid():      
            b=form.save(commit=False)
            b.company_id=compid
            b.save()
            messages.success(request,'charges added!')
            return redirect('exportcharges_list')
    else:
        form = ExportChargesForm()   
    return render(request,'exportcharges.html',{'form':form})

def exportcharges_list(request):
    id=request.session.get('company_id')
    if not id:
         return redirect('userlogin')
    charges = ExportCharges.objects.filter(company_id__login_id=id)

    return render(request,'exportchargelist.html',{'charges':charges}) 

def edit_exportcharges(request,id):
    charge = get_object_or_404(ExportCharges,id=id)
    cid = request.session.get('company_id')
    if not cid:
         return redirect('userlogin')
    if request.method == 'POST':
        form = ExportChargesForm(request.POST,instance=charge)
        if form.is_valid():
            form.save()
            messages.success(request,'editing successful!')
            return redirect('exportcharges_list')
    else:
        form = ExportChargesForm(instance=charge)   
    return render(request,'exportcharge_edit.html',{'form':form})

def delete_exportcharges(request,id):
    charge = get_object_or_404(ExportCharges,id=id)
    charge.delete()
    return redirect('exportcharges_list')

# def payment(request):
#     return render(request,'payment.html')
def payment(request, pid):
    exportdetails = get_object_or_404(Export, id=pid)
    company = get_object_or_404(Company, id=exportdetails.shipid.company_id.id)

    charges = get_object_or_404(
        ExportCharges,
        company_id=company.id,
        productcategory=exportdetails.productcategory,
        productname=exportdetails.productname
    )

    amount = charges.amount
    tax = charges.tax
    compcharge = amount * exportdetails.quantity
    total = compcharge + (compcharge * tax) / 100

    id = request.session.get('user_id')
    if not id:
        return redirect('userlogin')

    loginid = Login.objects.get(id=id)

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            a = form.save(commit=False)
            a.login_id = loginid
            a.amount = total
            a.save()

            exportdetails.paymentstatus = 1
            exportdetails.save()

            messages.success(request, 'payment success')
            return redirect('export_list')
    else:
        form = PaymentForm()

    return render(request, 'payment.html', {'form': form, 'amount': total})


def register_complaint(request,eid):
    
    id=request.session.get('user_id')
    if not id:
         return redirect('userlogin')
    uid=User.objects.get(login_id=id)
    expo=Export.objects.get(id=eid)
    if request.method == 'POST':
        form = ComplaintForm(request.POST,request.FILES)
        if form.is_valid():      
            b=form.save(commit=False)
            b.user_id=uid
            b.export_id=expo
            b.save()
            messages.success(request,'complaint registeration successful!')
            return redirect('export_list')
    else:
        form = ComplaintForm()   
    return render(request,'complaint.html',{'form':form})

def complaint_list(request):
    id = request.session.get('user_id')
    if not id:
         return redirect('userlogin')
    userid=User.objects.get(login_id=id)
    comp = Complaint.objects.filter(user_id=userid)
    return render(request,'complaintlist.html',{'comp':comp})

def edit_complaint(request,id):
    uid = request.session.get('user_id')
    if not uid:
         return redirect('userlogin')
    expo = get_object_or_404(Complaint,id=id)
    
    if request.method == 'POST':
        form = ComplaintForm(request.POST,request.FILES,instance=expo)
        if form.is_valid():
            form.save()
            messages.success(request,'editing successful!')
            return redirect('complaint_list')
    else:
        form = ComplaintForm(instance=expo)   
    return render(request,'complaint_edit.html',{'form':form})

def complaint_complist(request,id):
    cid = request.session.get('company_id')
    if not cid:
         return redirect('userlogin')

    eid=Export.objects.get(id=id)
    comp=None
    try:
        comp = Complaint.objects.get(export_id=eid.id)
    except Complaint.DoesNotExist:
        messages.error(request,"no complaints to view")
    return render(request,'complaint_complist.html',{'comp':comp})

def refund_export(request,id):
    expo = get_object_or_404(Export,id=id)
    expo.refundstatus=1
    expo.save()
    messages.success(request,'Refund successful!')
    return redirect('export_comp_list')

def reply(request,id):
    cid = request.session.get('company_id')
    if not cid:
         return redirect('userlogin')
    expo = get_object_or_404(Complaint,id=id)
    
    if request.method == 'POST':
        form = ComplaintReplyForm(request.POST,request.FILES,instance=expo)
        if form.is_valid():
            form.save()
            messages.success(request,'editing successful!')
            return redirect('export_comp_list')
    else:
        form = ComplaintReplyForm(instance=expo)   
    return render(request,'replycomp.html',{'form':form})
    

def register_tender(request):
    if request.method == 'POST':
        form = TenderForm(request.POST)
        if form.is_valid():      
            form.save()
            messages.success(request,'registeration successful!')
            return redirect('register_tender')
    else:
        form = TenderForm()   
    return render(request,'tender_reg.html',{'form':form})

def tender_list(request):
    tenders = Tender.objects.all()
    return render(request,'tender_list.html',{'tenders':tenders})

def edit_tender(request,id):
    tender = get_object_or_404(Tender,id=id)
    
    if request.method == 'POST':
        form = TenderForm(request.POST,instance=tender)
        if form.is_valid():
            form.save()
            messages.success(request,'editing successful!')
            return redirect('tender_list')
    else:
        form = TenderForm(instance=tender)   
    return render(request,'tender_edit.html',{'form':form})

def delete_tender(request,id):
    tender = get_object_or_404(Tender,id=id)
    tender.delete()
    return redirect('tender_list')

def contractor_tender_list(request):
    contractor_id = request.session.get('contractor_id')
    if not contractor_id:
         return redirect('userlogin') 
    tenders = Tender.objects.all()
    applied_tenders = AppliedTender.objects.filter(contractor_id__login_id=contractor_id).values_list('tender_id', flat=True)
    print(applied_tenders)
    return render(request,'contractor_tender_list.html',{'tenders':tenders,'applied_tenders': applied_tenders,'today':date.today()})

def apply_tender(request,tid):
    
    id=request.session.get('contractor_id')
    if not id:
         return redirect('userlogin')
    cid=Contractor.objects.get(login_id=id)
    tend=get_object_or_404(Tender,id=tid)
    if request.method == 'POST':
        form = AppliedTenderForm(request.POST)
        if form.is_valid():      
            b=form.save(commit=False)
            b.contractor_id=cid
            b.tender_id=tend
            b.save()
            messages.success(request,'registeration successful!')
            return redirect('contractor_tender_list')
    else:
        form = AppliedTenderForm()   
    return render(request,'tender_apply.html',{'form':form})

def edit_apply_tender(request,id):
    id = request.session.get('contractor_id')
    if not id:
         return redirect('userlogin')
    tend = get_object_or_404(AppliedTender,id=id)
    
    if request.method == 'POST':
        form = AppliedTenderForm(request.POST,request.FILES,instance=tend)
        if form.is_valid():
            form.save()
            messages.success(request,'editing successful!')
            return redirect('apply_tender_list')
    else:
        form = AppliedTenderForm(instance=tend)   
    return render(request,'tender_apply_edit.html',{'form':form})

def delete_apply_tender(request,id):
    tender = get_object_or_404(AppliedTender,id=id)
    tender.delete()
    return redirect('apply_tender_list')


def apply_tender_list(request):
    id=request.session.get('contractor_id')
    if not id:
         return redirect('userlogin')
    tenders=AppliedTender.objects.filter(contractor_id__login_id=id)
    return render(request,'tender_apply_list.html',{'tenders':tenders})

def admin_applied_tender_list(request,id):
    tid = get_object_or_404(AppliedTender,id=id)
    tenders = AppliedTender.objects.filter(tender_id=tid.tender_id).order_by('amount')
    return render(request,'admin_applied_tender_list.html',{'tenders':tenders})
    
def tender_approve(request,id):
    atend = get_object_or_404(AppliedTender,id=id)
    atend.applystatus=1
    atend.save()
    return redirect('admin_applied_tender_list',id)

def tender_reject(request,id):
    atend = get_object_or_404(AppliedTender,id=id)
    atend.applystatus=2
    atend.save()
    return redirect('admin_applied_tender_list',id)

def register_temp_job(request):
    if request.method == 'POST':
        form = TempJobForm(request.POST)
        if form.is_valid():      
            form.save()
            messages.success(request,'registeration successful!')
            return redirect('register_temp_job')
    else:
        form = TempJobForm()   
    return render(request,'temp_job_reg.html',{'form':form})

def temp_job_list(request):
    tjobs = TempJob.objects.all()
    interview_jobs = Interview.objects.values_list('job_id', flat=True)  # get only job IDs
    return render(
        request,
        'temp_job_list.html',
        {'tjobs': tjobs, 'interview_jobs': list(interview_jobs)}
    )


def edit_temp_job(request,id):
    temp = get_object_or_404(TempJob,id=id)
    
    if request.method == 'POST':
        form = TempJobForm(request.POST,instance=temp)
        if form.is_valid():
            form.save()
            messages.success(request,'editing successful!')
            return redirect('temp_job_list')
    else:
        form = TempJobForm(instance=temp)   
    return render(request,'temp_job_edit.html',{'form':form})

def delete_temp_job(request,id):
    tender = get_object_or_404(TempJob,id=id)
    tender.delete()
    return redirect('temp_job_list')

#new code replace
from django.db.models import Exists, OuterRef
def user_temp_job_list(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('userlogin')
    # if not User.objects.filter(id=user_id).exists():
        # return redirect('userlogin')
    user_tbl_id = User.objects.get(login_id=user_id)
    print(user_tbl_id)
    applied_subq = ApplyJob.objects.filter(
        user_id_id=user_tbl_id.id,         # use *_id to avoid an implicit join
        job_id=OuterRef('pk')
    )
    tjobs = (
        TempJob.objects
        .annotate(already_applied=Exists(applied_subq))
        .order_by('-currentdate', '-id')
    )

    return render(request, 'user_temp_job_list.html', {
        'tjobs': tjobs,
        'today': date.today(),
    })
    
def temp_job_apply(request,jid):
    
    id=request.session.get('user_id')
    if not id:
         return redirect('userlogin')
    uid=User.objects.get(login_id=id)
    tjob=get_object_or_404(TempJob,id=jid)
    if request.method == 'POST':
        form = ApplyJobForm(request.POST,request.FILES)
        if form.is_valid():      
            b=form.save(commit=False)
            b.user_id=uid
            b.job_id=tjob
            b.save()
            messages.success(request,'registeration successful!')
            return redirect('user_temp_job_list')
    else:
        form = ApplyJobForm()   
    return render(request,'temp_job_apply.html',{'form':form})

def user_applied_job_list(request):
    id=request.session.get('user_id')
    if not id:
         return redirect('userlogin')
    ajob=ApplyJob.objects.filter(user_id__login_id=id)
    return render(request,'user_applied_job.html',{'ajobs':ajob})

def edit_user_applied_job(request,id):
    uid = request.session.get('user_id')
    if not uid:
         return redirect('userlogin')
    tend = get_object_or_404(ApplyJob,id=id)
    
    if request.method == 'POST':
        form = ApplyJobForm(request.POST,request.FILES,instance=tend)
        if form.is_valid():
            form.save()
            messages.success(request,'editing successful!')
            return redirect('user_applied_job_list')
    else:
        form = ApplyJobForm(instance=tend)   
    return render(request,'user_applied_job_edit.html',{'form':form})

def delete_user_applied_job(request,id):
    tjob = get_object_or_404(ApplyJob,id=id)
    tjob.delete()
    return redirect('user_applied_job_list')

def admin_applied_job_list(request,id):
    ajobs = ApplyJob.objects.filter(job_id__id=id)
    return render(request,'admin_applied_job_list.html',{'ajobs':ajobs})

def temp_job_approve(request,id,jid):
    atjob = get_object_or_404(ApplyJob,id=id)
    atjob.status=1
    atjob.save()
    return redirect('admin_applied_job_list',jid)

def temp_job_reject(request,id,jid):
    atjob = get_object_or_404(ApplyJob,id=id)
    atjob.status=2
    atjob.save()
    return redirect('admin_applied_job_list',jid)

def register_interview(request,id):
    jid = get_object_or_404(TempJob,id=id)

    if request.method == 'POST':
        form = InterviewForm(request.POST)
        if form.is_valid():      
            a=form.save(commit=False)
            a.job_id=jid
            a.save()
            messages.success(request,'registeration successful!')
            return redirect('register_interview',id)
    else:
        form = InterviewForm()   
    return render(request,'interview_reg.html',{'form':form})

def interview_list(request,id):
    interviews = Interview.objects.filter(job_id=id)
    return render(request,'interview_list.html',{'interviews':interviews,'id':id})

def edit_interview(request,id,lid):
    temp = get_object_or_404(Interview,id=id)
    
    if request.method == 'POST':
        form = InterviewForm(request.POST,instance=temp)
        if form.is_valid():
            form.save()
            messages.success(request,'editing successful!')
            return redirect('interview_list',lid)
    else:
        form = InterviewForm(instance=temp)   
    return render(request,'interview_edit.html',{'form':form})

def delete_interview(request,id,lid):
    tender = get_object_or_404(Interview,id=id)
    tender.delete()
    return redirect('interview_list',lid)

# def delete(request,id):
#     tender = get_object_or_404(Company,id=id)
#     tender.delete()
#     return redirect('company_list')

def interview_user(request,id):
    uid = request.session.get('user_id')
    if not uid:
         return redirect('userlogin')

    tenders = Interview.objects.filter(job_id=id)
    
    return render(request,'interview_user.html',{'tenders':tenders})

def logout(request):
    request.session.flush()
    return redirect('landing')


def addnews(request):
    
    if request.method == 'POST':
        form = NewsForm(request.POST)
        if form.is_valid():      
            form.save()
            messages.success(request,'News added!')
            return redirect('addnews')
    else:
        form = NewsForm()   
    return render(request,'admin_addnews.html',{'form':form})

def admin_news_list(request):
    newss = News.objects.all().order_by('-id')
    return render(request,'admin_news_list.html',{'newss':newss})

def edit_news(request,id):
    news = get_object_or_404(News,id=id)
    
    if request.method == 'POST':
        form = NewsForm(request.POST,instance=news)
        if form.is_valid():
            form.save()
            messages.success(request,'editing successful!')
            return redirect('admin_news_list')
    else:
        form = NewsForm(instance=news)   
    return render(request,'admin_edit_news.html',{'form':form})

def delete_news(request,id):
    news = get_object_or_404(News,id=id)
    news.delete()
    return redirect('admin_news_list')

def news_list(request):
    news = News.objects.all().order_by('-id')
    return render(request,'news_list.html',{'news':news})

def user_news_list(request):
    id = request.session.get('user_id')
    if not id:
         return redirect('userlogin')
    news = News.objects.all().order_by('-id')
    return render(request,'user_news.html',{'news':news})

def company_news_list(request):
    id = request.session.get('company_id')
    if not id:
         return redirect('userlogin')
    news = News.objects.all().order_by('-id')
    return render(request,'company_news.html',{'news':news})

def contractor_news_list(request):
    id = request.session.get('contractor_id')
    if not id:
         return redirect('userlogin')
    news = News.objects.all().order_by('-id')
    return render(request,'contractor_news.html',{'news':news})

def ship_track(request,id):
    cid=request.session.get('company_id')
    if not cid:
         return redirect('userlogin')
    
    sid = get_object_or_404(Ship,id=id)

    if request.method == 'POST':
        form = ShipTrackingForm(request.POST)
        if form.is_valid():      
            a=form.save(commit=False)
            a.ship_id=sid
            a.ship_status=1
            a.save()
            messages.success(request,'Track updation successful!')
            return redirect('ship_list')
    else:
        form = ShipTrackingForm()   
    return render(request,'ship_track.html',{'form':form})
    
def ship_track_list(request,id):
    cid=request.session.get('company_id')
    if not cid:
         return redirect('userlogin')
    sid=get_object_or_404(Ship,id=id)
    loc=ShipTracking.objects.filter(ship_id=sid).order_by('-id')
    return render(request,'ship_track_list.html',{'locs':loc,'ship':sid})

def edit_ship_track(request,id,sid):
    cid=request.session.get('company_id')
    if not cid:
         return redirect('userlogin')
    
    stid = get_object_or_404(ShipTracking,id=id)
    
    if request.method == 'POST':
        form = ShipTrackingForm(request.POST,instance=stid)
        if form.is_valid():
            form.save()
            messages.success(request,'editing successful!')
            return redirect('ship_track_list',sid)
    else:
        form = ShipTrackingForm(instance=stid)   
    return render(request,'ship_track_edit.html',{'form':form})

def delete_ship_track(request,id,sid):
    stid = get_object_or_404(ShipTracking,id=id)
    stid.delete()
    return redirect('ship_track_list',sid)

def user_track_ship(request,id):
    uid = request.session.get('user_id')
    if not uid:
         return redirect('userlogin')
    sid=get_object_or_404(Ship,id=id)
    loc=ShipTracking.objects.filter(ship_id=sid).order_by('-id')
    return render(request,'user_track_ship.html',{'locs':loc,'ship':sid})

def company_complaint(request):
    id=request.session.get('company_id')
    if not id:
         return redirect('userlogin')
    cid=Login.objects.get(id=id)
    if request.method == 'POST':
        form = AllComplaintForm(request.POST)
        if form.is_valid():      
            b=form.save(commit=False)
            b.login_id=cid
            b.save()
            messages.success(request,'complaint registeration successful!')
            return redirect('companyhome')
    else:
        form = AllComplaintForm()   
    return render(request,'company_complaint.html',{'form':form})

def company_complaint_list(request):
    id = request.session.get('company_id')
    if not id:
         return redirect('userlogin')
    cid=Login.objects.get(id=id)
    comp = AllComplaint.objects.filter(login_id=cid)
    return render(request,'company_complaintlist.html',{'comp':comp})

def edit_company_complaint(request,id):
    cid = request.session.get('company_id')
    if not cid:
         return redirect('userlogin')
    aid = get_object_or_404(AllComplaint,id=id)
    
    if request.method == 'POST':
        form = AllComplaintForm(request.POST,instance=aid)
        if form.is_valid():
            form.save()
            messages.success(request,'editing successful!')
            return redirect('company_complaint_list')
    else:
        form = AllComplaintForm(instance=aid)   
    return render(request,'company_complaint_edit.html',{'form':form})

def delete_company_complaint(request,id):
    aid = get_object_or_404(AllComplaint,id=id)
    aid.delete()
    return redirect('company_complaint_list')

def user_complaint(request):
    id=request.session.get('user_id')
    if not id:
         return redirect('userlogin')
    uid=Login.objects.get(id=id)
    if request.method == 'POST':
        form = AllComplaintForm(request.POST)
        if form.is_valid():      
            b=form.save(commit=False)
            b.login_id=uid
            b.save()
            messages.success(request,'complaint registeration successful!')
            return redirect('userhome')
    else:
        form = AllComplaintForm()   
    return render(request,'user_complaint.html',{'form':form})

def user_complaint_list(request):
    id = request.session.get('user_id')
    if not id:
         return redirect('userlogin')
    uid=Login.objects.get(id=id)
    comp = AllComplaint.objects.filter(login_id=uid)
    return render(request,'user_complaintlist.html',{'comp':comp})

def edit_user_complaint(request,id):
    uid = request.session.get('user_id')
    if not uid:
         return redirect('userlogin')
    aid = get_object_or_404(AllComplaint,id=id)
    
    if request.method == 'POST':
        form = AllComplaintForm(request.POST,instance=aid)
        if form.is_valid():
            form.save()
            messages.success(request,'editing successful!')
            return redirect('user_complaint_list')
    else:
        form = AllComplaintForm(instance=aid)   
    return render(request,'user_complaint_edit.html',{'form':form})

def delete_user_complaint(request,id):
    aid = get_object_or_404(AllComplaint,id=id)
    aid.delete()
    return redirect('user_complaint_list')

def contractor_complaint(request):
    id=request.session.get('contractor_id')
    if not id:
         return redirect('userlogin')
    uid=Login.objects.get(id=id)
    if request.method == 'POST':
        form = AllComplaintForm(request.POST)
        if form.is_valid():      
            b=form.save(commit=False)
            b.login_id=uid
            b.save()
            messages.success(request,'complaint registeration successful!')
            return redirect('contractorhome')
    else:
        form = AllComplaintForm()   
    return render(request,'contractor_complaint.html',{'form':form})

def contractor_complaint_list(request):
    id = request.session.get('contractor_id')
    if not id:
         return redirect('userlogin')
    uid=Login.objects.get(id=id)
    comp = AllComplaint.objects.filter(login_id=uid)
    return render(request,'contractor_complaintlist.html',{'comp':comp})

def edit_contractor_complaint(request,id):
    cid = request.session.get('contractor_id')
    if not cid:
         return redirect('userlogin')
    aid = get_object_or_404(AllComplaint,id=id)
    
    if request.method == 'POST':
        form = AllComplaintForm(request.POST,instance=aid)
        if form.is_valid():
            form.save()
            messages.success(request,'editing successful!')
            return redirect('contractor_complaint_list')
    else:
        form = AllComplaintForm(instance=aid)   
    return render(request,'contractor_complaint_edit.html',{'form':form})

def delete_contractor_complaint(request,id):
    aid = get_object_or_404(AllComplaint,id=id)
    aid.delete()
    return redirect('contractor_complaint_list')

def admin_all_complaint_list(request):
    comp = AllComplaint.objects.all()
    return render(request,'admin_all_complaint_list.html',{'comp':comp})

def admin_reply(request,id):
    cid=AllComplaint.objects.get(id=id)
    if request.method == 'POST':
        form = AllComplaintReplyForm(request.POST,instance=cid)
        if form.is_valid():      
            form.save()
            messages.success(request,'complaint registeration successful!')
            return redirect('admin_all_complaint_list',)
    else:
        form = AllComplaintReplyForm(instance=cid)   
    return render(request,'admin_reply.html',{'form':form})

# 

# this is a fun added by me

def subhead(request):
    return render(request,'subheader.html')
def user_subhead(request):
    return render(request,'user_subheader.html')

def company_subhead(request):
    return render(request,'company_subheader.html')
def contractor_subhead(request):
    return render(request,'contractor_subheader.html')

def admin_head(request):
    return render(request,'admin_header.html')

def loginnew(request):
    return render(request,'loginform.html')

def admin_dash(request):
    company=Company.objects.all().count()
    ship=Ship.objects.all().count
    export=Export.objects.all().count
    tender=Tender.objects.all().count
    user=User.objects.all().count
    context={
        'company':company,
        "ship":ship,
        'export':export,
        'tender':tender,
        "user":user

    }
    
    return render(request,'admin_dash.html',context)

def interview_conducting(request, id):
    tjob = TempJob.objects.get(id=id)
    return render(request, 'interview_conducting.html', {'tjob': tjob})
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

def save_video_url(request):
    if request.method == "POST":
        data = json.loads(request.body)
        tempjob_id = data.get("tempjob_id")
        url = data.get("url")

        tjob = TempJob.objects.get(id=tempjob_id)
        tjob.url = url
        tjob.save()

        return JsonResponse({"status": "success", "url": url})
    return JsonResponse({"status": "fail"}, status=400)

# def interview_details(request):
#     interviews = Interview.objects.all()
#     return render(request,'interview_details.html',{'interviews':interviews})



