
from email.headerregistry import Group
from django.db import models
from django.db.models import Count, F
from datetime import datetime,date, timedelta
from dateutil.relativedelta import relativedelta
from computed_property import ComputedBooleanField

from django.contrib.auth.models import AbstractUser , BaseUserManager
# Create your models here.
class UserGroup(models.Model):
    sys_name = models.CharField(max_length=40,unique=True, verbose_name="Non systeme")
    name = models.CharField(max_length=40,unique=True, verbose_name="Nom")
    parent = models.ForeignKey('self',verbose_name="Groupe parent",null=True,blank=True,on_delete=models.SET_NULL)
     
    def __str__(self):
        return  self.name
class Status(models.Model):
    sys_name = models.CharField(max_length=40,unique=True, verbose_name="Non systeme")
    name = models.CharField(max_length=40,unique=True, verbose_name="Nom")
    entity= models.CharField(max_length=40,verbose_name="Entité")
     
    def __str__(self):
        return  self.name



class User(AbstractUser):
    username = models.CharField(max_length=40,unique=True, verbose_name="Nom d'utilisateur")
    date_joined = models.DateTimeField(auto_now_add=True,verbose_name="Date d'inscription")
    last_login = models.DateTimeField(auto_now=True,verbose_name="Dernière connexion")
    profile_img= models.ImageField(max_length=20000, null=True, blank=True,upload_to='uploads/images/',verbose_name="Photo de profil")
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    user_group = models.ForeignKey(UserGroup,on_delete=models.SET_NULL,null=True, verbose_name="Groupe d'utilisateur")

    USERNAME_FIELD= "username" 
    REQUIRED_FIELD= ["username", ]

    def __str__(self):
        return self.username

    def has_perm(self, perm: str, obj=None):
        return super().has_perm(perm)
    
    def has_module_perms(self, app_label):
        return super().has_module_perms(app_label)

class Energy(models.Model):
    wording = models.CharField(max_length=40, verbose_name="Libellé")
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.wording

class Gender(models.Model):
    wording = models.CharField(max_length=40, verbose_name="Libellé")
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.wording

class Type(models.Model):
    wording = models.CharField(max_length=40, verbose_name="Libellé")
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.wording
    

class Department(models.Model):
    name = models.CharField(max_length=40, verbose_name="Nom")
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

class City(models.Model):
    name = models.CharField(max_length=40, verbose_name="Nom")
    department = models.ForeignKey(Department,on_delete=models.CASCADE,verbose_name="Departement")
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    

class District(models.Model):
    name = models.CharField(max_length=40, verbose_name="Nom")
    city = models.ForeignKey(City,on_delete=models.CASCADE,verbose_name="Ville")
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    

class Owner(models.Model):
    last_name = models.CharField(max_length=30, verbose_name="Nom de famille")
    first_name = models.CharField(max_length=30, verbose_name="Prénom(s)")
    birth_date = models.DateField(verbose_name="Date de naissance")
    birth_place = models.CharField(max_length=30, verbose_name="Lieu de naissance")
    profession =  models.CharField(max_length=30, verbose_name="Profession")
    phone_number = models.CharField(max_length=30, verbose_name="Numero de téléphone")
    address =  models.TextField(max_length=250, verbose_name="Adresse ")
    sex= models.CharField( verbose_name='Sexe',max_length=20)
    city = models.ForeignKey(City,verbose_name="Ville actuelle",on_delete=models.SET_NULL,null=True)
    district = models.ForeignKey(District,null=True,on_delete=models.SET_NULL,verbose_name="Quartier actuel")
    user = models.ForeignKey(User,verbose_name="Utilisateur",null=True,blank=True,on_delete=models.SET_NULL)
  
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.last_name+ " "+self.first_name

class Agency(models.Model):
    designation = models.CharField(max_length=50, verbose_name="Désignation")
    head_agency = models.CharField(max_length=50, verbose_name="Nom complet de Chef")
    phone_number = models.CharField(max_length=30, verbose_name="Numero de téléphone")
    address =  models.TextField(max_length=250, verbose_name="Adresse ")
    city = models.ForeignKey(City,verbose_name="Ville actuelle",null=True,on_delete=models.SET_NULL)
    district = models.ForeignKey(District,null=True,on_delete=models.SET_NULL,verbose_name="Quartier actuel")
    parent = models.ForeignKey('self',verbose_name="Service parent",null=True,blank=True,on_delete=models.CASCADE)
    user = models.ForeignKey(User,verbose_name="Utilisateur",null=True,blank=True,on_delete=models.SET_NULL)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.designation
    

class Vehicle(models.Model):
    car_model= models.CharField(max_length=30, verbose_name="Modèle")
    energy = models.ForeignKey(Energy, verbose_name="Energie",null=True, on_delete=models.SET_NULL)
    gender = models.ForeignKey(Gender, verbose_name="Genre",null=True,on_delete=models.SET_NULL)
    type = models.ForeignKey(Type, verbose_name="Type",null=True,on_delete=models.SET_NULL)
    power = models.BigIntegerField(verbose_name="Puissance")
    empty_weight= models.BigIntegerField(verbose_name="Poids à vide")
    pay_load= models.BigIntegerField(verbose_name="Charge utile")
    uid_tag_rfid = models.TextField(verbose_name="UID du tag RFID",null=True,unique=True)
    plate_number = models.TextField(max_length=30,verbose_name="Numéro d'immatriculation",unique=True)
    status = models.ForeignKey(Status,verbose_name="Status",null=True,on_delete =models.SET_NULL)
   
    owner = models.ForeignKey(Owner,verbose_name="Propriétaire",on_delete =models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.car_model +" "+self.plate_number

class Warning(models.Model):
    done_at = models.DateField(verbose_name="Date du constat",null=True, )
    motif = models.CharField(max_length=40, verbose_name="Motif")
    description= models.TextField(max_length=400, verbose_name="Description")
    vehicle = models.ForeignKey(Vehicle,verbose_name="Vehicule",on_delete=models.CASCADE)
    owner = models.ForeignKey(Owner,verbose_name="Propriétaire",null=True,on_delete=models.SET_NULL)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.motif +' '+self.create_at

class Reader(models.Model):
 
    uid= models.TextField(max_length=400, verbose_name="UID",unique=True)
    designation = models.CharField(max_length=50, verbose_name="Désignation")
    address= models.TextField(max_length=400, verbose_name="Adresse")
    city = models.ForeignKey(City,verbose_name="Ville actuelle",null=True,on_delete=models.SET_NULL)
    district = models.ForeignKey(District,verbose_name="Quartier actuel",null=True,on_delete=models.SET_NULL)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.uid

class Record(models.Model):
    reader= models.ForeignKey(Reader,verbose_name="UID du lecteur",to_field="uid",null=True,on_delete=models.CASCADE)
    vehicle= models.ForeignKey(Vehicle,verbose_name="UID du Vehicule",to_field="uid_tag_rfid",null=True,on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)
    
    


class Notification(models.Model):
  
    message= models.TextField(max_length=400, verbose_name="Message")
    record = models.ForeignKey(Record,verbose_name="Enregistrement",on_delete=models.CASCADE)
    errors=models.TextField(null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.errors + " " +self.message


class Verdict(models.Model):
    sys_name = models.CharField(max_length=40, verbose_name="Nom système")
    name = models.CharField(max_length=40, verbose_name="Nom")
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

class TypeOperation(models.Model):
    sys_name = models.CharField(max_length=40, verbose_name="Nom système")
    name = models.CharField(max_length=40, verbose_name="Nom")
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name


class Operation(models.Model):
    type_operation = models.ForeignKey(TypeOperation,verbose_name="type d'operation",null=True,on_delete=models.SET_NULL)
    motif = models.CharField(max_length=40,null=True, verbose_name="Motif")
    description= models.TextField(max_length=400, null=True, verbose_name="Description")
    done_at = models.DateField(verbose_name="Date",null=True, )
    validity = models.IntegerField(verbose_name="Validité",null=True, )
    verdict = models.ForeignKey(Verdict,verbose_name="Verdict",null=True,on_delete=models.SET_NULL)
    vehicle = models.ForeignKey(Vehicle,verbose_name="Vehicule",on_delete=models.CASCADE)
    agency = models.ForeignKey(Agency,verbose_name="Agence",null=True,on_delete=models.SET_NULL)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    # is_expired = ComputedBooleanField(compute_from="_is_expired",default=False)
    
    def _is_expired(self):
        if  self.validity is not None:
            return self.done_at <= (date.today() - relativedelta(months=self.validity))
        if self.type_operation.sys_name=="stealing":
            return True
        return False
    
    def will_expired(self):
        
        if  self.validity is not None:
            return ( self.done_at-relativedelta(days=8)) < (date.today() - relativedelta(months=self.validity))<( self.done_at-relativedelta(days=8))
        return False
    
class Tag(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle,on_delete=models.CASCADE)
    reader = models.ForeignKey(Reader, on_delete=models.CASCADE,to_field="uid")
    create_at= models.DateTimeField(auto_now_add=True)

















