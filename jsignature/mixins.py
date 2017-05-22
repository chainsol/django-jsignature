"""
    A django mixin providing fields to store a signature captured
    with jSignature jQuery plugin
"""
from django.utils import timezone
from django.db import models
from django.utils.translation import ugettext_lazy as _
from .fields import JSignatureField


class JSignatureFieldsMixin(models.Model):
    """ Mixin class providing fields to store a signature with jSignature """
    signature = JSignatureField(
        _('Signature'),
        blank=True,
        null=True)
    signature_date = models.DateTimeField(
        _('Signature date'),
        blank=True,
        null=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):

        is_new = self._state.adding
        if not is_new:
            original = self.__class__.objects.get(pk=self.pk)
        else:
            original = None

        if self.signature:
            if is_new or self.signature != original.signature:
                self.signature_date = timezone.now()
        else:
            self.signature_date = None

        super(JSignatureFieldsMixin, self).save()
