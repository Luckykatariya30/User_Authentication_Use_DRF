from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser


# create custom manager 
class UserManager(BaseUserManager):
    def create_user(self, email, name , date_of_birth, password=None , password2=None):
        """
        Creates and saves a User with the given email, name , tc , and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            date_of_birth=date_of_birth
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

# created custom superuser  

    def create_superuser(self, email, name, date_of_birth , password=None ):
            """
            Creates and saves a superuser with the given email, name ,tc and password.
            """
            user = self.create_user(
                email,
                password=password,
                name=name,
                date_of_birth=date_of_birth
            )
            user.is_admin = True
            user.save(using=self._db)
            return user 
    
# create custom user  

class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=225)
    date_of_birth = models.DateField()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name","date_of_birth"]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


