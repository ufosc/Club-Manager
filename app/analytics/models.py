from pathlib import Path
from typing import ClassVar, Optional
from django.core.files import File
from django.urls import reverse

from django.db import models

from core.abstracts.models import ManagerBase, ModelBase
from utils.formatting import format_bytes
from utils.models import OneToOneOrNoneField, UploadFilepathFactory


class LinkManager(ManagerBase["Link"]):
    """Manage queries for Links."""

    def create(self, target_url: str, club, create_qrcode=False, **kwargs):

        link = super().create(target_url=target_url, club=club, **kwargs)

        if create_qrcode:
            QRCode.objects.create(link=link)

        return link


class Link(ModelBase):
    """Track visits to target url."""

    club = models.ForeignKey(
        "clubs.Club", on_delete=models.CASCADE, related_name="links"
    )
    target_url = models.CharField()
    display_name = models.CharField(null=True, blank=True)
    pings = models.IntegerField(default=0)

    # Relationships
    visits: models.QuerySet["LinkVisit"]
    qrcode: Optional["QRCode"] = None

    # Dynamic Properties
    @property
    def public_url(self):
        return reverse("redirect-link", kwargs={"link_id": self.id})

    # @property
    # def qrcode(self) -> Optional["QRCode"]:
    #     try:
    #         return self._qrcode
    #     except ObjectDoesNotExist:
    #         return None

    # Overrides
    objects: ClassVar[LinkManager] = LinkManager()

    def __str__(self):
        self.display_name or self.public_url


class LinkVisitManager(ManagerBase["LinkVisit"]):
    """Manage Link Visit queries."""

    def create(self, link: Link, ipaddress: str, **kwargs):
        return super().create(link=link, ipaddress=ipaddress, **kwargs)


class LinkVisit(ModelBase):
    """Who visited a link."""

    link = models.ForeignKey(Link, on_delete=models.CASCADE, related_name="visits")
    # TODO: stash breadcrumb on browser to prevent VPNs from registering as multiple visits
    ipaddress = models.GenericIPAddressField()
    context = models.JSONField(null=True, blank=True)
    amount = models.IntegerField(default=0)

    # Overrides
    objects: ClassVar[LinkVisitManager] = LinkVisitManager()

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=("link", "ipaddress"),
                name="unique_ip_per_link",
            ),
        )

    # Methods
    def increment(self, by: int = 1, commit=True):
        """Increase visit amount."""

        self.amount += by

        if commit:
            self.save()


class QRCode(ModelBase):
    """Store image for QR Codes."""

    qrcode_upload_path = UploadFilepathFactory("clubs/qrcodes/")

    link = OneToOneOrNoneField(
        Link, on_delete=models.CASCADE, related_name="qrcode", primary_key=True
    )
    image = models.ImageField(null=True, blank=True, upload_to=qrcode_upload_path)

    def save_image(self, filepath: str):
        """Takes path for image and sets it to the image field."""

        path = Path(filepath)

        with path.open(mode="rb") as f:
            self.image = File(f, name=f.name)
            self.save()

    # Dynamic Properties
    @property
    def url(self):
        return self.link.public_url

    @property
    def width(self):
        if self.image:
            return self.image.width

    @property
    def size(self):
        if self.image:
            return format_bytes(self.image.size)

    # Overrides
    def __str__(self) -> str:
        return self.url

    class Meta:
        verbose_name = "QR Code"
