from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, firstname, lastname, mobile, password, **extra_fields):
        """
        Creates and saves a User with the
        given email and password and username.
        """
        if not email:
            raise ValueError("Email must be set")
        if not firstname:
            raise ValueError("First Name is required")
        if not lastname:
            raise ValueError("Last Name is required")
        if not mobile:
            raise ValueError("Mobile is required")
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=firstname, last_name=lastname, mobile=mobile, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email, firstname, lastname, mobile, password, **extra_fields):
        return self._create_user(email, firstname, lastname, mobile, password, **extra_fields)

    def create_superuser(self, email, firstname, lastname, mobile, password, **extra_fields):
        return self._create_user(email, firstname, lastname, mobile, password, **extra_fields)
