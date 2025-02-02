from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from api.managers import UserManager
from django.core.mail import send_mail
from django.db import models


class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('user','User'),
        ('admin','Admin'),
        ('doctor','Doctor'),
        ('manager','Manager')
    )
    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(_("username"), max_length=150, unique=True, )
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(_('staff'), default=True)
    role=models.CharField(_('role'), max_length=30, choices=ROLE_CHOICES, default='user')
    avatar = models.ImageField(_('avatar'), null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)


class Doctor(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    specialization=models.CharField(_('specialization'), max_length=30, blank=True)
    experience=models.PositiveIntegerField(_('experience'), default=0)
    location=models.CharField(_('location'), max_length=30, blank=True)
    clinic_name=models.CharField(_('clinic name'), max_length=30, blank=True)
    cunsultation_fee=models.DecimalField(_('cunsultation fee'), max_digits=10, decimal_places=2)
    is_consultation_fee=models.BooleanField(_('consultation fee'), default=False)
    avaible_today=models.BooleanField(_('avaible today'), default=False)
    rating_percentage=models.PositiveIntegerField(_('rating percentage'), default=0)
    patient_stories=models.PositiveIntegerField(_('patient stories'), default=0)
    def __str__(self):
        return self.specialization


    class Meta:
        verbose_name = _('doctor')
        verbose_name_plural = _('doctors')

class News(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(_('title'), max_length=30, blank=True)
    img=models.ImageField(_('image'))
    created_at=models.DateField(_('created at'), auto_now_add=True)
    def __str__(self):
        return self.title


    class Meta:
        verbose_name = _('news')






