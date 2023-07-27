from ast import Try
from cProfile import label

from calendar import c
from email.headerregistry import Group
from pyexpat import model
import re

from django.core.exceptions import ValidationError
from django  import  forms


from .models import Warning,Status, UserGroup,User,City,District,Type,Gender,Energy,Owner,Vehicle,Reader,Operation,TypeOperation,Agency, Verdict
# from phonenumber_field.formfields import PhoneNumberField


#genaral custom Form 
class CustomModelForm(forms.ModelForm):
     def is_valid(self):
        result = super().is_valid()
         # loop on *all* fields if key '__all__' found else only on errors:
        for x in (self.fields if '__all__' in self.errors else self.errors):
            attrs = self.fields[x].widget.attrs
            attrs.update({'class': attrs.get('class', '') + ' is-invalid'})
        return result

class CustomForm(forms.Form):
     def is_valid(self):
        result = super().is_valid()
         # loop on *all* fields if key '__all__' found else only on errors:
        for x in (self.fields if '__all__' in self.errors else self.errors):
            attrs = self.fields[x].widget.attrs
            attrs.update({'class': attrs.get('class', '') + ' is-invalid'})
        return result

class UsersForm(forms.Form):
    username= forms.CharField(required=True,min_length=3, max_length=50)
    profile_img= forms.ImageField(required=True)
    password= forms.CharField(required=True,min_length=8, max_length=50)
    confirm = forms.CharField(required=True,min_length=8, max_length=50)
    
      
    def clean_username(self):
        data = self.cleaned_data['username']
        
        if User.objects.filter(username=data).first() is not None:
            raise ValidationError("Le nom d'utilisateur est déjà utilisé")

      
        return data
    def clean_profile_img(self):
        image = self.cleaned_data.get('profile_img', False)
        if image:
            if image.size > 4*1024*1024:
                raise ValidationError("La taille de l'image est trop grande ( > 4mb )")
            return image
        else:
            raise ValidationError("le fichier image est corrompu")
    
    def clean_confirm(self):
        data = self.cleaned_data['confirm']
        data1 = self.cleaned_data['password']
        
        if data1 != data:
            raise ValidationError("Echec de confirmation de mot de passe")

      
        return data

    def is_valid(self):
         result = super().is_valid()
         # loop on *all* fields if key '__all__' found else only on errors:
         for x in (self.fields if '__all__' in self.errors else self.errors):
             attrs = self.fields[x].widget.attrs
             attrs.update({'class': attrs.get('class', '') + ' is-invalid'})
         return result

class UsersFormUpdate(forms.Form):
    username= forms.CharField(required=True,min_length=3, max_length=50)
    profile_img= forms.ImageField(required=False)
    password= forms.CharField(required=False,min_length=8, max_length=50)
    confirm = forms.CharField(required=False,min_length=8, max_length=50)
    
      

    def clean_profile_img(self):
        image = self.cleaned_data.get('profile_img', False)
        if image:
            if image.size > 4*1024*1024:
                raise ValidationError("La taille de l'image est trop grande ( > 4mb )")
            return image
       
    
    def clean_confirm(self):
        data = self.cleaned_data['confirm']
        data1 = self.cleaned_data['password']
        
        if data1 != data:
            raise ValidationError("Echec de confirmation de mot de passe")

      
        return data

    def is_valid(self):
         result = super().is_valid()
         # loop on *all* fields if key '__all__' found else only on errors:
         for x in (self.fields if '__all__' in self.errors else self.errors):
             attrs = self.fields[x].widget.attrs
             attrs.update({'class': attrs.get('class', '') + ' is-invalid'})
         return result

class LoginForm(forms.Form):
    username = forms.CharField(required=True,min_length=3, max_length=50,label="nom d'utilisateur")
    password = forms.CharField(required=True,min_length=8,max_length=50,label="Mot de passe")
    
    def clean_username(self):
        data = self.cleaned_data['username']
        
        if User.objects.filter(username=data).first() is None:
            raise ValidationError("Le nom d'utilisateur n'existe pas")

      
        return data
    

class AgencyFormUpdate(UsersFormUpdate):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(AgencyFormUpdate, self).__init__(*args, **kwargs)
        self.fields['user_group'].queryset = UserGroup.objects.filter(parent= self.request.user.user_group)
    
    user_group =forms.ModelChoiceField(required=True,queryset=UserGroup.objects.all())
    designation = forms.CharField(max_length=50, label="Désignation")
    head_agency = forms.CharField(max_length=50, label="Nom complet de Chef")
    phone_number = forms.CharField(required=True,min_length=8, max_length=25)
    email = forms.EmailField(required=True,min_length=5,max_length=50)
    city = forms.ModelChoiceField(required=True,queryset=City.objects.all())
    district= forms.ModelChoiceField(queryset=District.objects.all())
    address = forms.CharField(min_length=3,max_length=250,required=True)
    
class AgencyForm(UsersForm):
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(AgencyForm, self).__init__(*args, **kwargs)
        self.fields['user_group'].queryset = UserGroup.objects.filter(parent= self.request.user.user_group)
  
  
    user_group =forms.ModelChoiceField(required=True,queryset=UserGroup.objects.all())
    
    designation = forms.CharField(max_length=50, label="Désignation")
    head_agency = forms.CharField(max_length=50, label="Nom complet de Chef")
    phone_number = forms.CharField(required=True,min_length=8, max_length=25)
    email = forms.EmailField(required=True,min_length=5,max_length=50)
    city = forms.ModelChoiceField(required=True,queryset=City.objects.all())
    district= forms.ModelChoiceField(queryset=District.objects.all())
    address = forms.CharField(min_length=3,max_length=250,required=True)
    


class UserForm(UsersForm):
    
   
    last_name= forms.CharField(required=True,min_length=2, max_length=50)
    first_name= forms.CharField(required=True,min_length=3)
    birth_date= forms.DateField(required=True,widget=forms.DateInput(attrs={'type': 'date'}))
    birth_place= forms.CharField(required=True,min_length=3, max_length=50)
    profession=forms.CharField(required=True,min_length=3, max_length=50)
    sex = forms.CharField(required=True,max_length=20)
    # phone_number = PhoneNumberField(required=True,min_length=8, max_length=25)
    phone_number = forms.CharField(required=True,min_length=8, max_length=25)
    email = forms.EmailField(required=True,min_length=5,max_length=50)
    city = forms.ModelChoiceField(required=True,queryset=City.objects.all())
    district= forms.ModelChoiceField(queryset=District.objects.all())
    address = forms.CharField(min_length=3,max_length=250,required=True)
  
class OwnerFormUpdate(UsersFormUpdate):
    last_name= forms.CharField(required=True,min_length=2, max_length=50)
    first_name= forms.CharField(required=True,min_length=3)
    birth_date= forms.DateField(required=True,widget=forms.DateInput(attrs={'type': 'date'}))
    birth_place= forms.CharField(required=True,min_length=3, max_length=50)
    profession=forms.CharField(required=True,min_length=3, max_length=50)
    sex = forms.CharField(required=True,max_length=20)
    # phone_number = PhoneNumberField(required=True,min_length=8, max_length=25)
    phone_number = forms.CharField(required=True,min_length=8, max_length=25)
    email = forms.EmailField(required=True,min_length=5,max_length=50)
    city = forms.ModelChoiceField(required=True,queryset=City.objects.all())
    district= forms.ModelChoiceField(queryset=District.objects.all())
    address = forms.CharField(min_length=3,max_length=250,required=True)
    
    
class CarForm(CustomModelForm):
    error_css_class="is-invalid"
    required_css_class="is-invalid"
    
    owner = forms.ModelChoiceField(required=False,queryset=Owner.objects.all())
    type =  forms.ModelChoiceField(required=True,queryset=Type.objects.all())
    energy = forms.ModelChoiceField(required=True,queryset=Energy.objects.all())
    gender = forms.ModelChoiceField(required=True,queryset=Gender.objects.all())
    power = forms.IntegerField(required=True)
    car_model = forms.CharField(required=True)
    pay_load = forms.IntegerField(required=True)
    empty_weight = forms.IntegerField(required=True)
    plate_number = forms.CharField(required=True,max_length=20)
    
    def is_valid(self):
         result = super().is_valid()
         # loop on *all* fields if key '__all__' found else only on errors:
         for x in (self.fields if '__all__' in self.errors else self.errors):
             attrs = self.fields[x].widget.attrs
             attrs.update({'class': attrs.get('class', '') + ' is-invalid'})
         return result
     
    def clean_plate_number(self):
        data = self.cleaned_data['plate_number']
        
        if Vehicle.objects.filter(plate_number=data).first() is not None:
            raise ValidationError("L'immatriculation est déjà utilisé")

        return data

    class Meta():
        model = Vehicle
        fields='__all__'
class ReaderForm(CustomModelForm):
    
    def __init__(self, *args, **kwargs):
        super(ReaderForm, self).__init__(*args, **kwargs)
        try: 
           
            self.instance =kwargs.pop("instance")
            self.fields['id'].initial = self.instance.id 
        except: pass
        
    id =forms.IntegerField(required=False,initial=0)
    uid= forms.CharField(required=True,max_length=200)
    designation = forms.CharField(required=True,min_length=3, max_length=50)
    city = forms.ModelChoiceField(required=True,queryset=City.objects.all())
    district= forms.ModelChoiceField(queryset=District.objects.all())
    address= forms.CharField(max_length=200)
    
   
    
    class Meta:
        model= Reader
        fields = ['uid', 'designation','city','district','address']

class Assurance(CustomModelForm):
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(Assurance, self).__init__(*args, **kwargs)
        try: 
           
            self.instance =kwargs.pop("instance")
            self.fields['plate_number'].initial = self.instance.vehicle.plate_number
            self.fields['id'].initial = self.instance.id 
            
        except: pass
        
    id =forms.IntegerField(required=False,initial=0)
    validity = forms.IntegerField(required=True, initial=0)
    done_at = forms.DateField(required=True,widget=forms.DateInput(attrs={'type': 'date'}))
    type_operation= forms.IntegerField(required=False,initial=0)
    agency= forms.IntegerField(required=False, initial=0)
    vehicle= forms.IntegerField(required=False, initial=1)
    plate_number=forms.CharField(required=True,max_length=20,min_length=3,initial="")
    class Meta:
        model = Operation
        fields =["vehicle","done_at","agency","validity" ,"type_operation"] 
        
 
        
        
    def save(self, commit=True):
        instance = super(Assurance, self).save(commit=False)
        instance.vehicle = Vehicle.objects.get(plate_number=self.cleaned_data["plate_number"])
        instance.agency=Agency.objects.get(user=self.request.user)
        instance.type_operation= TypeOperation.objects.get(sys_name='assurance')
    
        if commit:
            instance.save()
        return instance
        
        
    def  clean_plate_number(self):
        data = self.cleaned_data["plate_number"]
        if   Vehicle.objects.filter(plate_number=data).first() is  None:
            raise ValidationError("Cette immatriculation n'est pas valide")
        return data
            
        
        
class Toll(Assurance): 
    def save(self, commit=True):
        instance = super(Toll, self).save(commit=False)
        instance.type_operation= TypeOperation.objects.get(sys_name='toll')
    
        if commit:
            instance.save()
        return instance  
    
    
class TechnicalVisit(Assurance):
    verdict = forms.ModelChoiceField(required=True,queryset=Verdict.objects.all()) 
    
    def save(self, commit=True):
        instance = super(TechnicalVisit, self).save(commit=False)
        instance.type_operation= TypeOperation.objects.get(sys_name='technical_visit')
    
        if commit:
            instance.save()
        return instance 
    
    class Meta:
        model = Operation
        fields =["vehicle","done_at","agency","validity" ,"type_operation","verdict"] 


class Stealing(Assurance):
    motif = forms.CharField(max_length=40,required=True) 
    description = forms.CharField(max_length=1000,required=True,widget=forms.Textarea)
    validity =forms.CharField(required=False,disabled=True)
    
    def save(self, commit=True):
        instance = super(Stealing, self).save(commit=False)
        instance.type_operation= TypeOperation.objects.get(sys_name='stealing')
    
        if commit:
            instance.save()
        return instance 
    
    class Meta:
        model = Operation
        fields =["vehicle","done_at","agency","motif" ,"type_operation","description"] 

class Report(Stealing): 
    def save(self, commit=True):
        instance = super(Report, self).save(commit=False)
        instance.type_operation= TypeOperation.objects.get(sys_name='report')
    
        if commit:
            instance.save()
        return instance  
      
    
    
        
    
class Anomaly(CustomModelForm):
    
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(Anomaly, self).__init__(*args, **kwargs)
        try: 
           
            self.instance =kwargs.pop("instance")
            self.fields['plate_number'].initial = self.instance.vehicle.plate_number
            self.fields['id'].initial = self.instance.id 
            
        except: pass
        
        
    id =forms.IntegerField(required=False,initial=0)
    done_at = forms.DateField(required=True,widget=forms.DateInput(attrs={'type': 'date'}))
    owner= forms.IntegerField(required=False, initial=0)
    vehicle= forms.IntegerField(required=False, initial=1)
    plate_number=forms.CharField(required=True,max_length=20,min_length=3,initial="")
    motif = forms.CharField(max_length=40,required=True) 
    description = forms.CharField(max_length=1000,required=True,widget=forms.Textarea)
    class Meta:
        model = Warning
        fields =["vehicle", "done_at","owner","motif" ,"description"] 
     
    
 
        
        
    def save(self, commit=True):
        instance = super(Anomaly, self).save(commit=False)
        instance.vehicle = Vehicle.objects.get(plate_number=self.cleaned_data["plate_number"])
        instance.owner=Owner.objects.get(user=self.request.user)
      
    
        if commit:
            instance.save()
        return instance
        
        
    def  clean_plate_number(self):
        data = self.cleaned_data["plate_number"]
        if   Vehicle.objects.filter(plate_number=data).first() is  None:
            raise ValidationError("Cette immatriculation n'est pas valide")
        return data
               
      
    
class CarUpdateForm(CarForm):
    id =forms.IntegerField(required=False, initial=0) 
    owner= forms.ModelChoiceField(required=True,queryset=Owner.objects.all())
    status= forms.ModelChoiceField(required=True,queryset=Status.objects.filter(entity="vehicle"))
    
    def __init__(self, *args, **kwargs):
        
        super(CarUpdateForm, self).__init__(*args, **kwargs)
        try: 
           
            self.instance =kwargs.pop("instance")
            
            self.fields['id'].initial = self.instance.id 
            
        except: pass
    class Meta:
        model=Vehicle
        fields = ["car_model","owner","type","energy","gender","power","empty_weight","pay_load","plate_number","status"]
    
    
    def clean_plate_number(self):
        data = self.cleaned_data['plate_number']
        
       

        return data
    
    
class TagForm(forms.Form):
    vehicle= forms.ModelChoiceField(queryset=Vehicle.objects.all(),required=True)
    reader =forms.ModelChoiceField(queryset=Reader.objects.all(),required=True)