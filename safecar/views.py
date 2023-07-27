from asyncio import tasks

from calendar import month
from cgitb import html
from curses import erasechar
from itertools import count
from pydoc import plain
import re
from unittest import removeResult
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .forms import OwnerFormUpdate, AgencyForm, Anomaly,Report, Stealing, TagForm, TechnicalVisit,Toll,CarUpdateForm, LoginForm,UserForm ,CarForm,Owner, Vehicle,UserGroup,AgencyFormUpdate,ReaderForm ,Assurance,TypeOperation
from pprint import pp, pprint
from .models import Agency, Record, User,Reader ,Operation ,Warning,Notification,Tag
from safecar.my_decorators.group_acces import group_required
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from django.db.models import Count, F, Value ,Q
from dateutil.relativedelta import relativedelta
from django.http import HttpResponse,JsonResponse
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.core.mail import EmailMessage




# Create your views here.

def get_agencies(request):

    return render(request,"safecar/agencies.html")

def agency_profile(request):
    
    return render(request,"safecar/agency_profile.html")

def profile(request):
   

    # send_mail(
    #     'Subject here',
    #     '<strong>Here is<br> the message.</strong>',
    #     'from@example.com',
    #     ['to@example.com'],
    #     fail_silently=False,
    # )
    user = request.user
    
    if user.user_group.sys_name=="owner":
        return render(request,"safecar/profile.html")
    return render(request,"safecar/agency_profile.html")

def get_profile(request,id):
    my_user= get_object_or_404(User,pk=id) 
    
    if my_user.user_group.sys_name=="owner":
        return render(request,"safecar/profile_get.html",{"my_user":my_user})
    return render(request,"safecar/agency_profile_get.html",{"my_user":my_user})

def reader(request):
    
    readers= Reader.objects.all()
    return render(request,"safecar/reader.html",{"readers": readers})


def reader_add(request):
   
        
    id=''
    if request.method =="POST" : 
        if request.POST["id"]!="0": 
            read =get_object_or_404(Reader,pk=request.POST["id"])
            reader = ReaderForm(request.POST,instance=read)
        
        else:  reader = ReaderForm(request.POST)
             
       
        if reader.is_valid():
            reader.save()
            return redirect("reader")
            
    else:  
        try :
            
            read =get_object_or_404(Reader,pk=request.GET["id"])
            reader = ReaderForm(instance=read)
            id = read.id
        except: reader = ReaderForm()
        
    
    return render(request,"safecar/reader_add.html",{"reader":reader})
@group_required(["admin"])
def reader_delete(request):
    if request.method == "POST":
        reader =get_object_or_404(Reader,pk=request.POST["id"])
        reader.delete()
    return redirect("reader")
    
        




def vehicle_edit(request):
   
    if request.method =="POST" : 
        if request.POST["id"]!="0": 
            task =get_object_or_404(Vehicle,pk=request.POST["id"])
            form = CarUpdateForm(request.POST,instance=task)
            if Vehicle.objects.filter(plate_number=request.POST["plate_number"]).first() !=task:
                if Vehicle.objects.filter(plate_number=request.POST["plate_number"]).first() is not None:
                    form.add_error("plate_number","L'immatriculation est déjà utilisé")
            
          
        else:  
            form = CarUpdateForm(request.POST)
            if Vehicle.objects.filter(plate_number=request.POST["plate_number"]).first() is not None:
                    form.add_error("plate_number","L'immatriculation est déjà utilisé")
             
       
        if form.is_valid():
            form.save()
            return redirect("vehicles")
            
    else:  
        if request.GET.get("id",None) is not  None:
            
            task =get_object_or_404(Vehicle,pk=request.GET["id"])
            form = CarUpdateForm(instance=task)
            
        else: form= CarUpdateForm()
        
    
    return render(request,"safecar/vehicle_edit.html",{"form":form})

def vehicle_delete(request):
    if request.method == "POST":
        reader =get_object_or_404(Vehicle,pk=request.POST["id"])
        reader.delete()
    return redirect("vehicles")

def get_vehicle(request,id):
    car = get_object_or_404(Vehicle, pk=id)
    d =datetime.now()
    
    assurance= car.operation_set.filter(type_operation__sys_name="assurance").order_by("-id").first()
    technical_visit= car.operation_set.filter(type_operation__sys_name="technical_visit").order_by("-id").first()
    toll= car.operation_set.filter(type_operation__sys_name="toll").order_by("-id").first() 
    stealing= car.operation_set.filter(type_operation__sys_name="stealing").order_by("-id").first()

    records=car.record_set.filter(create_at__year=d.year, create_at__month=d.month ,create_at__day= d.day )
    return render(request,"safecar/vehicle.html",{"car":car,"records":records,"assurance":assurance,"technical_visit":technical_visit,"toll":toll,"stealing":stealing})


def search_car(request):
    car =Vehicle.objects.filter(plate_number=request.GET.get("id",None)).first()
    if car is not None:
        return JsonResponse(reverse("vehicle",kwargs={"id":car.id}),safe=False)
    else: 
        return JsonResponse(1,safe=False)

@group_required(["admin"])
def get_vehicles(request):
    cars = Vehicle.objects.all()
    
    
    return render(request,"safecar/vehicles.html",{'cars': cars})

# @group_required(["owner"])
def get_my_vehicle(request,id):
    d =datetime.now()
    car= Vehicle.objects.get(id=id,owner__user_id=request.user.id)
    assurance= car.operation_set.filter(type_operation__sys_name="assurance").order_by("-id").first()
    technical_visit= car.operation_set.filter(type_operation__sys_name="technical_visit").order_by("-id").first()
    toll= car.operation_set.filter(type_operation__sys_name="toll").order_by("-id").first() 

    records=car.record_set.filter(create_at__year=d.year, create_at__month=d.month ,create_at__day= d.day )
    return render(request,"safecar/my_vehicle.html",{"car":car,"records":records,"assurance":assurance,"technical_visit":technical_visit,"toll":toll})





@group_required(["owner"])
def get_my_vehicles(request):
    cars = Vehicle.objects.filter(owner=Owner.objects.get(user= request.user))
    return render(request,"safecar/my_vehicles.html",{"cars":cars})






def search_notice_add(request):
    
    return render(request,"safecar/search_notice_add.html")

def report_add(request):
    
    return render(request,"safecar/report_add.html")

def anomaly_add(request):
    
    return render(request,"safecar/anomaly_add.html")

    

def notify(request):
    return render(request,"safecar/notification.html")







def log(request):
    if request.user.is_authenticated:
        try:
            return redirect(request.META['HTTP_REFERER'])
        except:
            return redirect("profile")
        
    
    
    if request.method=='POST' :
        login_form = LoginForm(request.POST)
        
        if login_form.is_valid:
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            
            if  user is not None :
                login(request,user)
                return redirect('profile')
            else:
                login_form.add_error("password","Mot de passe incorrect")
        
        return render(request,"safecar/login.html",{"form": login_form})
    
    login_form = LoginForm()
    return render(request,"safecar/login.html",{"form": login_form})
    
def logout_user(request):
    logout(request)
    return redirect('login')



def owners(request):
    owners = Owner.objects.all()
    
    
    return render(request,"safecar/owners.html",{'owners': owners})

def owner_delete(request):
    if request.method == "POST":
        reader =get_object_or_404(Owner,pk=request.POST["id"])
        reader.delete()
    return redirect("owners")


def owner_add(request):
    
    user_form = UserForm(request.POST ,request.FILES)
  
    if request.method =="POST":
        
        
       
    
        if  user_form.is_valid()   :
            user = User()
            user.username =user_form.cleaned_data['username']
            user.set_password(user_form.cleaned_data['password'])
            user.profile_img=user_form.cleaned_data["profile_img"]
            user.email = user_form.cleaned_data["email"]
            user.user_group = UserGroup.objects.get(sys_name='owner')
            user.save()
           
            
            owner = Owner()
            owner.first_name= user_form.cleaned_data["first_name"]
            owner.last_name= user_form.cleaned_data["last_name"]
            owner.birth_date= user_form.cleaned_data["birth_date"]
            owner.birth_place= user_form.cleaned_data["birth_place"]
            owner.address= user_form.cleaned_data["address"]
            owner.city= user_form.cleaned_data["city"]
            owner.district= user_form.cleaned_data["district"]
            owner.phone_number= user_form.cleaned_data["phone_number"]
            owner.profession= user_form.cleaned_data["profession"]
            owner.sex= user_form.cleaned_data["sex"]
            owner.user= user
            owner.save()
            
            return redirect("get_profile",id=user.id)
            
        
    return render(request,"safecar/owner_add.html",{"user_form":user_form})
    

def owner_edit(request,id):
    owner = get_object_or_404(Owner,pk=id)
    user= owner.user
    field=owner.__dict__.copy()
    field["username"]=user.username
    field["email"]=user.email
    field["user_group"]=user.user_group
    field["city"]=owner.city
    field["district"]=owner.district
    
   
  
    owner_form =OwnerFormUpdate(field)
    
    if request.method == 'POST':
        
        owner_form =OwnerFormUpdate(request.POST,request.FILES)
        
        if owner_form.is_valid():
            if user.username==owner_form.cleaned_data['username'] or User.objects.filter(username=owner_form.cleaned_data['username']) is None:
               
                user.username =owner_form.cleaned_data['username']
                if owner_form.cleaned_data.get('password', False): user.set_password(owner_form.cleaned_data['password'])
                if owner_form.cleaned_data.get('profile_img', False): user.profile_img=owner_form.cleaned_data["profile_img"]
                user.email = owner_form.cleaned_data["email"] 
                user.save()
                
            
                
                owner.first_name= owner_form.cleaned_data["first_name"]
                owner.last_name= owner_form.cleaned_data["last_name"]
                owner.birth_date= owner_form.cleaned_data["birth_date"]
                owner.birth_place= owner_form.cleaned_data["birth_place"]
                owner.address= owner_form.cleaned_data["address"]
                owner.city= owner_form.cleaned_data["city"]
                owner.district= owner_form.cleaned_data["district"]
                owner.phone_number= owner_form.cleaned_data["phone_number"]
                owner.profession= owner_form.cleaned_data["profession"]
                owner.sex= owner_form.cleaned_data["sex"]
                owner.user= user
                owner.save()
                
                return redirect("get_profile",id=user.pk)
            
            else:
                owner_form.add_error("username","Ce nom d'utilisateur existe déjà")
                owner_form.is_valid()
                      
    
    return render(request,"safecar/owner_edit.html",{"owner_form":owner_form,"id":id})



@group_required(["admin","assuranc_home","cnsr"])
def agency_add(request):
    
   
  
    agency_form =AgencyForm(request.POST,request.FILES,request=request)
    
    if request.method == 'POST':
        if agency_form.is_valid():
            user = User()
            user.username =agency_form.cleaned_data['username']
            user.set_password(agency_form.cleaned_data['password'])
            user.profile_img=agency_form.cleaned_data["profile_img"]
            user.email = agency_form.cleaned_data["email"]
            user.user_group = agency_form.cleaned_data["user_group"]
            user.save()
            
            agency =Agency()
            agency.designation = agency_form.cleaned_data["designation"] 
            agency.head_agency= agency_form.cleaned_data["head_agency"]  
            agency.address= agency_form.cleaned_data["address"]
            agency.city= agency_form.cleaned_data["city"]
            agency.district= agency_form.cleaned_data["district"]
            agency.phone_number= agency_form.cleaned_data["phone_number"]  
            agency.user =user
            agency.parent= request.user.agency_set.first()           
            agency.save()
            
            return redirect("get_profile",id=user.pk)
                      
    
    return render(request,"safecar/agency_add.html",{"agency_form":agency_form})

@group_required(["admin","assuranc_home","cnsr"])
def agency_edit(request,id):
    agency= get_object_or_404(Agency,pk=id)
    user= agency.user
    field=agency.__dict__.copy()
    field["username"]=user.username
    field["email"]=user.email
    field["user_group"]=user.user_group
    field["city"]=agency.city
    field["district"]=agency.district
    
   
  
    agency_form =AgencyFormUpdate(field,request=request)
    
    if request.method == 'POST':
        
        agency_form =AgencyFormUpdate(request.POST,request.FILES,request=request)
        
        if agency_form.is_valid():
            if user.username==agency_form.cleaned_data['username'] or User.objects.filter(username=agency_form.cleaned_data['username']) is not None:
               
                user.username =agency_form.cleaned_data['username']
                if agency_form.cleaned_data.get('password', False): user.set_password(agency_form.cleaned_data['password'])
                if agency_form.cleaned_data.get('profile_img', False): user.profile_img=agency_form.cleaned_data["profile_img"]
                user.email = agency_form.cleaned_data["email"] 
                user.user_group = agency_form.cleaned_data["user_group"]
                user.save()
                
            
                agency.designation = agency_form.cleaned_data["designation"] 
                agency.head_agency= agency_form.cleaned_data["head_agency"]  
                agency.address= agency_form.cleaned_data["address"]
                agency.city= agency_form.cleaned_data["city"]
                agency.district= agency_form.cleaned_data["district"]
                agency.phone_number= agency_form.cleaned_data["phone_number"]     
                agency.save()
                
                return redirect("get_profile",id=user.pk)
            
            else:
                agency_form.add_error("username","Ce nom d'utilisateur existe déjà")
                agency_form.is_valid()
                      
    
    return render(request,"safecar/agency_edit.html",{"agency_form":agency_form,"id":id})

@group_required(["admin","assurance","cnsr","police"])
def agency_delete(request):
    agency= get_object_or_404(Agency,pk=request.POST.get('id'))
    user= agency.user
    agency.delete()
    user.delete()
    
    return redirect("agencies")

@group_required(["admin","assuranc_home","cnsr","police"])
def agencies(request):
    
    agency= request.user.agency_set.first()
    agencies =  agency.agency_set.all()
    
    return render(request,"safecar/agencies.html",{"agencies": agencies})



# manage the assurance to the vehicle
def assurances(request):
    task_name="Les assurances"
    task_url ="assurance_add"
    del_url = "assurance_delete"
    
    tasks= Operation.objects.filter(type_operation__sys_name="assurance")
    return render(request,"safecar/assurances.html",{"tasks": tasks,"task_name":task_name,"task_url":task_url,"del_url":del_url})

# @group_required(["admin"])
def assurance_add(request):
    task_name="Les assurances"
    task_url ="assurance_add"
    del_url = "assrance_delete"
   
    
    
   
    if request.method =="POST" : 
        if request.POST["id"]!="0": 
            task =get_object_or_404(Operation,pk=request.POST["id"])
            form = Assurance(request.POST,instance=task,request=request)
            
        else:  form = Assurance(request.POST,request=request)
             
       
        if form.is_valid():
            form.save()
            return redirect("assurances")
            
    else:  
        if request.GET.get("id",None) is not  None:
            
            task =get_object_or_404(Operation,pk=request.GET["id"])
            form = Assurance(instance=task,request=request)
            
        else: form = Assurance(request=request)
        
    
    return render(request,"safecar/assurance_add.html",{"form":form,"task_name":task_name,"task_url":task_url,"del_url":del_url})

def assurance_delete(request):
    if request.method == "POST":
        reader =get_object_or_404(Operation,pk=request.POST["id"])
        reader.delete()
    return redirect("assurances")
    
    
# manage toll
def tolls(request):
    task_name="Les abonnement au péage"
    task_url="toll_add"
    del_url ="toll_delete"
    
    tasks= Operation.objects.filter(type_operation__sys_name="toll")
    return render(request,"safecar/assurances.html",{"tasks": tasks,"task_name":task_name,"task_url":task_url,"del_url":del_url})

# @group_required(["admin"])
def toll_add(request):
   
    task_name="Enregistrer un abonnement"
    
        
   
    if request.method =="POST" : 
        if request.POST["id"]!="0": 
            task =get_object_or_404(Operation,pk=request.POST["id"])
            form = Toll(request.POST,instance=task,request=request)
          
        else:  form = Toll(request.POST,request=request)
             
       
        if form.is_valid():
            form.save()
            return redirect("tolls")
            
    else:  
        if request.GET.get("id",None) is not  None:
            
            task =get_object_or_404(Operation,pk=request.GET["id"])
            form = Toll(instance=task,request=request)
            
        else: form = Toll(request=request)
        
    
    return render(request,"safecar/assurance_add.html",{"form":form,"task_name":task_name})

def toll_delete(request):
    if request.method == "POST":
        reader =get_object_or_404(Operation,pk=request.POST["id"])
        reader.delete()
    return redirect("tolls")
    
  

# technical_visit
def technical_visits(request):
    task_name="Les visites techniques"
    
    tasks= Operation.objects.filter(type_operation__sys_name="technical_visit")
    return render(request,"safecar/technical_visits.html",{"tasks": tasks,"task_name":task_name})

# @group_required(["admin"])
def technical_visit_add(request):
   
    task_name="Enregistrer une visite technique"
    
        
   
    if request.method =="POST" : 
        if request.POST["id"]!='0': 
            task =get_object_or_404(Operation,pk=request.POST["id"])
            form = TechnicalVisit(request.POST,instance=task,request=request)
          
        else:  form = TechnicalVisit(request.POST,request=request)
             
       
        if form.is_valid():
            form.save()
            return redirect("technical_visits")
            
    else:  
        if request.GET.get("id",None) is not  None:
            
            task =get_object_or_404(Operation,pk=request.GET["id"])
            form = TechnicalVisit(instance=task,request=request)
            
        else: form = TechnicalVisit(request=request)
        
    
    return render(request,"safecar/technical_visit_add.html",{"form":form,"task_name":task_name})

def technical_visit_delete(request):
    if request.method == "POST":
        reader =get_object_or_404(Operation,pk=request.POST["id"])
        reader.delete()
    return redirect("technical_visits")


# stealing
def stealings(request):
    task_name="Les avis de recherches"
    
    tasks= Operation.objects.filter(type_operation__sys_name="stealing")
    return render(request,"safecar/stealings.html",{"tasks": tasks,"task_name":task_name})

# @group_required(["admin"])
def stealing_add(request):
   
    task_name="Ajouter un avis recherche"
    
        
   
    if request.method =="POST" : 
        if request.POST["id"]!='0': 
            task =get_object_or_404(Operation,pk=request.POST["id"])
            form = Stealing(request.POST,instance=task,request=request)
          
        else:  form = Stealing(request.POST,request=request)
             
       
        if form.is_valid():
            form.save()
            return redirect("stealings")
            
    else:  
        if request.GET.get("id",None) is not  None:
            
            task =get_object_or_404(Operation,pk=request.GET["id"])
            form = Stealing(instance=task,request=request)
            
        else: form = Stealing(request=request)
        
    
    return render(request,"safecar/stealing_add.html",{"form":form,"task_name":task_name})

def stealing_delete(request):
    if request.method == "POST":
        reader =get_object_or_404(Operation,pk=request.POST["id"])
        reader.delete()
    return redirect("stealings")




# reports
def reports(request):
    task_name="Les rapports"
    
    if request.user.user_group.sys_name=="owner": 
        tasks= Operation.objects.filter(type_operation__sys_name="report",vehicle__in=request.user.owner_set.first().vehicle_set.all())
    else:
        tasks= Operation.objects.filter(type_operation__sys_name="report")
    return render(request,"safecar/reports.html",{"tasks": tasks,"task_name":task_name})

# @group_required(["admin"])
def report_add(request):
   
    task_name="Ajouter un rapport"
    
        
   
    if request.method =="POST" : 
        if request.POST["id"]!='0': 
            task =get_object_or_404(Operation,pk=request.POST["id"])
            form = Report(request.POST,instance=task,request=request)
          
        else:  form = Report(request.POST,request=request)
             
       
        if form.is_valid():
            form.save()
            return redirect("reports")
            
    else:  
        if request.GET.get("id",None) is not  None:
            
            task =get_object_or_404(Operation,pk=request.GET["id"])
            form = Report(instance=task,request=request)
            
        else: form = Report(request=request)
        
    
    return render(request,"safecar/report_add.html",{"form":form,"task_name":task_name})

def report_delete(request):
    if request.method == "POST":
        reader =get_object_or_404(Operation,pk=request.POST["id"])
        reader.delete()
    return redirect("reports")





# anomaly
def anomalies(request):
    
    
    task_name="Les anomalies"
    if request.user.user_group.sys_name=="owner":
        tasks = Warning.objects.filter(owner=request.user.owner_set.first())
    else:
        tasks= Warning.objects.all()
    return render(request,"safecar/anomalies.html",{"tasks": tasks,"task_name":task_name})



# @group_required(["admin"])
def anomaly_add(request):
   
    task_name="Signaler une anomalie"
    
        
   
    if request.method =="POST" : 
        if request.POST["id"]!='0': 
            task =get_object_or_404(Warning,pk=request.POST["id"])
            form = Anomaly(request.POST,instance=task,request=request)
          
        else:  form = Anomaly(request.POST,request=request)
             
       
        if form.is_valid():
            form.save()
            return redirect("anomalies")
            
    else:  
        if request.GET.get("id",None) is not  None:
            
            task =get_object_or_404(Warning,pk=request.GET["id"])
            form = Anomaly(instance=task,request=request)
            
        else: form = Anomaly(request=request)
        
    
    return render(request,"safecar/anomaly_add.html",{"form":form,"task_name":task_name})

def anomaly_delete(request):
    if request.method == "POST":
        reader =get_object_or_404(Warning,pk=request.POST["id"])
        reader.delete()
    return redirect("anomalies")



def notify(request):
    notes=Notification.objects.all().order_by('-id')
    return render(request,"safecar/notification.html",{"notes":notes})
    
def notify_get(request):
    if request.method == "GET" and request.GET['id'] is not None:
        notes=Notification.objects.filter(id__gt=request.GET['id']).order_by('-id')
        html=render_to_string("safecar/partial_notice.html",{"notes":notes})
    else: html=""
    
    return JsonResponse(html,safe=False)

@csrf_exempt
def read(request):
    pprint(request.POST.get('uid_tag',None))
    pprint(request.POST.get('uid_tag',None))
    try: 
        if request.POST.get('uid_reader',None)!=None and request.POST.get('uid_tag',None)!=None:
            record =Record()
            vehicle= Vehicle.objects.get(uid_tag_rfid=request.POST.get('uid_tag'))
            pprint(vehicle)
            reader = Reader.objects.get(uid=request.POST.get('uid_reader'))
            pprint(reader)
            record.reader = reader
            record.vehicle = vehicle
            record.save()
            pprint(" je suis apres l'enregistrement")
            text=[]
            if Operation.objects.filter(vehicle=record.vehicle,type_operation__sys_name="stealing").last() is not None:
                text.append("stealing")  
            
            assurance=Operation.objects.filter(vehicle=record.vehicle,type_operation__sys_name="assurance").last()
            technical_visit=Operation.objects.filter(vehicle=record.vehicle,type_operation__sys_name="technical_visit").last()
            if assurance is None or assurance._is_expired() :
                text.append("assurance")  
            if technical_visit is None or technical_visit._is_expired() :
                text.append("technical_visit") 
            pprint(" je suis apres l'analyse")    
            note = Notification() 
            note.record=record
            note.message="Ville: " +record.reader.city.name + ', Quartier actuel: '+record.reader.district.name
            pprint(" je suis apres la note")   
            if len(text)!=0:
                print(len(text))
                note.errors= ','.join(text)
                note.save()
            pprint("apres if") 
            
            toll = Operation.objects.filter(vehicle=record.vehicle,type_operation__sys_name="toll").last()
            if toll is not None and  toll._is_expired() is False: 
                return JsonResponse(2,safe=False)# don't have toll on available 
            
            return JsonResponse(1,safe=False)
        else: JsonResponse(0,safe=False)
    except:return JsonResponse(0,safe=False)
    
    
    

def check_reader(request,id):
    record = Record.objects.filter(reader=Reader.objects.get(pk=id)).order_by("id").last()
    errors=[]
    if record is not None:
        if Operation.objects.filter(vehicle=record.vehicle,type_operation__sys_name="stealing").last() is not None:
            errors.append("stealing")  
        
        assurance=Operation.objects.filter(vehicle=record.vehicle,type_operation__sys_name="assurance").last()
        technical_visit=Operation.objects.filter(vehicle=record.vehicle,type_operation__sys_name="technical_visit").last()
        if assurance is None or assurance._is_expired() :
            errors.append("assurance")  
        if technical_visit is None or technical_visit._is_expired() :
            errors.append("technical_visit")  
    
    
    
    
    return render(request,"safecar/check_reader.html",{"record":record,"errors":errors}) 

def check_reader_get(request):
    record = Record.objects.filter(reader=Record.objects.get(pk=request.GET["id"]).reader).order_by("id").last()
    errors=[]
    if Operation.objects.filter(vehicle=record.vehicle,type_operation__sys_name="stealing").last() is not None:
        errors.append("stealing")  
    
    assurance=Operation.objects.filter(vehicle=record.vehicle,type_operation__sys_name="assurance").last()
    technical_visit=Operation.objects.filter(vehicle=record.vehicle,type_operation__sys_name="technical_visit").last()
    if assurance is None or assurance._is_expired() :
        errors.append("assurance")  
    if technical_visit is None or technical_visit._is_expired() :
        errors.append("technical_visit")  
    
    
    html=render_to_string("safecar/check_reader_get.html",{"record":record,"errors":errors})
    
    return JsonResponse(html,safe=False)


def tag_register(request):
    
    tag_form =TagForm()
    if request.method =="POST" :
        tag_form =TagForm(request.POST)
        if tag_form.is_valid():
            Tag.objects.filter(user=request.user).delete()
            tag = Tag()
            tag.user=request.user
            tag.vehicle = tag_form.cleaned_data["vehicle"]
            tag.reader = tag_form.cleaned_data["reader"]
            tag.save()
            return JsonResponse(tag.vehicle.plate_number,safe=False)
        else: return JsonResponse("0",safe=False)
    return render(request,"safecar/register_tag.html",{"tag":tag_form})

@csrf_exempt
def tag_api(request):
    
    if request.method == "POST":
        
        if request.POST.get("reader",None) is None: 
            try:
                pprint("yo I send back result ")
                pprint(request.POST["number"])
                pprint(request.POST["uid_tag"])
                vehicle= Tag.objects.get(vehicle__plate_number=request.POST["number"]).vehicle
                pprint(vehicle)
                
                vehicle.uid_tag_rfid=request.POST["uid_tag"]
                pprint(Vehicle.objects.filter(uid_tag_rfid=request.POST["uid_tag"]).first())
                pprint("before saving")
                vehicle.save()
                pprint("after saving")
                Tag.objects.filter(vehicle=vehicle).delete()
                return JsonResponse(1,safe=False)
            except:
                pprint("I run exceptions here")
                return JsonResponse(0,safe=False)
        else:
            tag = Tag.objects.filter(reader=Reader.objects.filter(uid=request.POST.get("reader",None)).first()).first()
            pprint(tag)
            if  tag is not None: 
                return JsonResponse(tag.vehicle.plate_number,safe=False)
            else: return JsonResponse(0,safe=False)  
        
    else: return JsonResponse(2,safe=False)
        
        
def tag_done(request):
    return JsonResponse(Tag.objects.filter(user=request.user).first() is  None,safe=False)

def api_test(request):
    return render(request,"safecar/api_test.html")

def number_notification(request):
    
     
    return JsonResponse(Notification.objects.all().count(),safe=False)


def send_mail_to_user(request):
    assurances= Operation.objects.filter(type_operation__sys_name="assurance")
    visits = Operation.objects.filter(type_operation__sys_name="technical_visit")
    operations= assurances.union(visits)
    
  
    for operation in operations:
        
        html_content=render_to_string("safecar/email.html",{"operation":operation})
        msg = EmailMessage("Notification de SafeCar",html_content,'from@example.com', [operation.vehicle.owner.user.email])
        msg.content_subtype = "html"  # Main content is now text/html
        msg.send()
        if operation.will_expired():
            pprint(operation.vehicle.user.email)
            
          
           
    return JsonResponse(1,safe=False);    
    
    
       
        
