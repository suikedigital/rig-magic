from django.db import models
from django.conf import settings

MATERIAL_CHOICES = [
    ("Aluminum", "Aluminum"),
    ("Carbon", "Carbon"),
    ("Wood", "Wood"),
]

RIG_CHOICES = [
    ('Mast-Head Sloop', 'mast-head sloop'),
    ('Fractional Sloop', 'fractional sloop'),
    ('Sloop', 'Sloop'),
    ('Ketch', 'Ketch'),
    ('Cutter', 'Cutter'),
    ('Yawl', 'Yawl'),
    ('Catamaran', 'Catamaran'),
    ('Trimaran', 'Trimaran'),
]

class BaseYacht(models.Model):
    builder = models.CharField(max_length=50, null=True, blank=True)
    model_name = models.CharField(max_length=50, null=True, blank=True) 
    model_number = models.CharField(max_length=50, null=True, blank=True)
    variant = models.CharField(max_length=100, null=True, blank=True)
    rig_type = models.ForeignKey('RigType', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.builder} {self.model_name} {self.model_number} {self.variant}".strip()

class YachtInstance(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    base_yacht = models.ForeignKey(BaseYacht, on_delete=models.CASCADE)
    custom_name = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f"{self.owner.username}'s {self.base_yacht}"

class YachtDraft(models.Model):
    yacht_instance = models.ForeignKey(YachtInstance, on_delete=models.CASCADE, related_name='drafts')
    draft_custom_name = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f"Draft '{self.draft_custom_name}' for {self.yacht_instance}"

class RigType(models.Model):
    name = models.CharField(max_length=50, choices=RIG_CHOICES)
    def __str__(self):
        return self.name

class Mast(models.Model):
    base_yacht = models.ForeignKey(BaseYacht, on_delete=models.CASCADE, related_name='masts')
    position = models.CharField(
        max_length=20,
        choices=[
            ('main', 'Main Mast'),
            ('mizzen', 'Mizzen Mast'),
            ('fore', 'Foremast'),
            ('aft', 'Aft Mast'),
        ],
        default='main'
    )
    i = models.FloatField(null=True, blank=True, help_text="Deck to genoa halyard sheave")
    j = models.FloatField(null=True, blank=True, help_text="Foretriangle base")
    p = models.FloatField(null=True, blank=True, help_text="Luff length (mainsail)")
    mast_height = models.FloatField(null=True, blank=True)
    material = models.CharField(max_length=50, choices=MATERIAL_CHOICES, null=True, blank=True)

    def __str__(self):
        return f"{self.position.capitalize()} mast for {self.base_yacht.builder} {self.base_yacht.model_name} {self.base_yacht.model_number} {self.base_yacht.variant}".strip()

class Boom(models.Model):
    base_yacht = models.ForeignKey(BaseYacht, on_delete=models.CASCADE, related_name='booms')
    position = models.CharField(
        max_length=20,
        choices=[
            ('main', 'Main Boom'),
            ('mizzen', 'Mizzen Boom'),
            ('fore', 'Fore Boom'),
            ('aft', 'Aft Boom'),
        ],
        default='main'
    )
    length = models.FloatField(null=True, blank=True)
    e = models.FloatField(null=True, blank=True, help_text="Aft face of mast to the black band on the boom")
    material = models.CharField(max_length=50, choices=MATERIAL_CHOICES, null=True, blank=True)
    boom_height = models.FloatField(null=True, blank=True)
    boom_type = models.CharField(max_length=50, choices=[("Standard", "Standard"), ("Furling", "Furling")], null=True, blank=True)

    def __str__(self):
        return f"boom for {self.position.capitalize()} {self.base_yacht.builder} {self.base_yacht.model_name} {self.base_yacht.model_number} {self.base_yacht.variant}".strip()