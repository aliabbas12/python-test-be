# Create your models here.
import posixpath

from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.mail import EmailMultiAlternatives
from django.db import models, transaction
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import gettext_lazy as _

from accounts.managers import UserManager
from accounts.utils import account_confirm_token_generator
from utils.orm.model_mixins import CreatedAtUpdatedAtModelMixin, SoftDeletableModelMixin
from utils.orm.validators import basic_name_validator


class User(
    AbstractBaseUser,
    PermissionsMixin,
    CreatedAtUpdatedAtModelMixin,
    SoftDeletableModelMixin,
):
    """
    Class implementing a custom fully featured User model with admin-compliant
    permissions.

    The class does not have a username field. Uses email as the
    USERNAME_FIELD for authentication.

    email and password are required. Other fields are optional.
    """

    email = models.EmailField(
        _("Email address"),
        unique=True,
    )

    # technical fields
    date_email_verified = models.DateTimeField(
        _("Date of email confirmation"),
        null=True,
        blank=True,
    )
    is_active = models.BooleanField(
        _("Active"),
        default=False,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    is_staff = models.BooleanField(
        _("Staff status"),
        default=False,
        help_text=_("Designates whether the user can log into the admin site."),
    )

    date_last_verification_email_sent = models.DateTimeField(
        _("Date of last verification email"),
        null=True,
        blank=True,
    )
    # personal fields
    first_name = models.CharField(
        _("First name"),
        validators=[basic_name_validator],
        max_length=150,
        null=True,
        blank=True,
    )
    last_name = models.CharField(
        _("Last name"),
        validators=[basic_name_validator],
        max_length=150,
        null=True,
        blank=True,
    )

    soft_delete_attributes = {"is_active": False}
    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"

    # A list of the field names that will be prompted for when creating a user
    # via the createsuperuser management command. REQUIRED_FIELDS has
    # no effect in other parts of Django, like creating a user in the admin
    REQUIRED_FIELDS = ["is_active"]

    objects = UserManager()

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        get_latest_by = "created_at"
        ordering = ["-created_at"]

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Returns the short name for the user."""
        return self.first_name

    def email_user(
        self, subject, message, from_email=None, html_message=None, **kwargs
    ):
        """
        Sends an email to this User.
        """
        subject = f"Menulance - {subject}"
        mail = EmailMultiAlternatives(
            subject, message, from_email, [self.email], **kwargs
        )
        if html_message:
            mail.attach_alternative(html_message, "text/html")
        return bool(mail.send())

    def send_email_verification_email(self):
        """
        Sends an email verification link to this User.
        """
        context = {
            "verification_link": self.get_verification_link(),
            "site_name": "Menulance",
        }
        text_content = render_to_string("accounts/invitation.txt", context)
        html_content = render_to_string("accounts/invitation.html", context)

        if self.email_user(
            subject=_("Verify your email"),
            message=text_content,
            html_message=html_content,
        ):
            self.date_last_verification_email_sent = timezone.now()
            self.save(update_fields=["date_last_verification_email_sent"])

    def get_verification_link(self):
        uid = urlsafe_base64_encode(force_bytes(self.pk))
        token = account_confirm_token_generator.make_token(self)
        return posixpath.join(
            settings.FRONTEND_UI_BASE_URL,
            settings.FRONTEND_UI_VERIFY_EMAIL_PATH.strip("/"),
            uid,
            token,
            "",
        )

    def send_registration_completed_email(self):
        """
        Sends a 'registration completed' email to this User.
        """
        if not self.is_active:
            return False

        context = {
            "site_name": "Menulance.com",
        }

        text_content = render_to_string("accounts/registration_completed.txt", context)
        html_content = render_to_string("accounts/registration_completed.html", context)

        return self.email_user(
            _("Registration completed"), text_content, html_message=html_content
        )

    def send_password_reset_email(self, issuer_mail=None):
        """
        Sends an email including an password reset link to this User.
        """
        context = {
            "username": self.get_username(),
            "password_reset_link": self.get_password_reset_link(),
            "site_name": "Menulance.com",
        }
        text_content = render_to_string("accounts/password_reset.txt", context)
        html_content = render_to_string("accounts/password_reset.html", context)

        bcc = [issuer_mail]
        if issuer_mail is None or issuer_mail == self.email:
            bcc = None
        return self.email_user(
            subject=_("Reset your password"),
            message=text_content,
            bcc=bcc,
            html_message=html_content,
        )

    def get_password_reset_link(self):
        uid = urlsafe_base64_encode(force_bytes(self.pk))
        token = account_confirm_token_generator.make_token(self)
        return posixpath.join(
            settings.URL_CLIENT_APPLICATION,
            settings.ACCOUNTS_PASSWORD_RESET_URL.strip("/"),
            uid,
            token,
            "",
        )

    def delete(self, using=None, keep_parents=False):
        return super().delete(using, keep_parents)

    @transaction.atomic
    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        super().save(
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields,
        )


class UserPreferences(models.Model):
    """
    Class representing additional preferences and settings
    for users in the application.
    """

    user = models.OneToOneField(
        "accounts.User",
        on_delete=models.CASCADE,
        verbose_name='User'
    )
    font = models.ForeignKey(
        "core.Font",
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='Preferred Font',
        help_text='Select the preferred font.'
    )
    font_size = models.IntegerField(
        null=True,
        verbose_name='Font Size',
        help_text='Specify the preferred font size.'
    )
    ui_language = models.ForeignKey(
        "core.Language",
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='UI Language',
        help_text='Choose the preferred language for the user interface.'
    )
    enable_wizard = models.BooleanField(
        default=True,
        verbose_name='Enable Wizard',
        help_text='Toggle to enable or disable the user interface wizard.'
    )
    enable_pro_tips = models.BooleanField(
        default=True,
        verbose_name='Enable Pro Tips',
        help_text='Toggle to display or hide pro tips in the user interface.'
    )
    enable_autodetect = models.BooleanField(
        default=True,
        verbose_name='Enable Autodetect',
        help_text='Toggle to enable or disable auto detection feature.'
    )
    enable_soundfx = models.BooleanField(
        default=True,
        verbose_name='Enable Sound Effects',
        help_text='Toggle to enable or disable sound effects in the application.'
    )
    enable_notifications = models.BooleanField(
        default=True,
        verbose_name='Enable Notifications',
        help_text='Toggle to display or hide notifications.'
    )

    class Meta:
        verbose_name = _("UserPreference")
        verbose_name_plural = _("UserPreferences")
