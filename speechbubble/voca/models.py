import operator
from django.db import models
from datetime import datetime
from django.db.models import Q
from filebrowser.fields import FileBrowseField
from tinymce import models as tinymce_models
from photologue.models import ImageModel, Photo

# Create your models here.

SPEECH_TYPE_CHOICES = (
    ('recorded', 'Recorded'),
    ('artificial', 'Mainly Artificial'),
)

OS_CHOICES = (
    ('none', 'None'),
    ('dedicated', 'Dedicated'),
    ('windows', 'Windows'),
    ('macintosh', 'Macintosh'),
    ('mobile', 'Mobile Devices'),
    ('other', 'Other'),
)


class DraftManager(models.Manager):
    ''' Use this manager to get objects that have a draft field '''
    def get_query_set(self):
        return super(DraftManager, self).get_query_set().filter(draft=False)

    def all_with_draft(self):
        return super(DraftManager, self).get_query_set()

    def draft_set(self):
        return super(DraftManager, self).get_query_set().filter(draft=True)

    def get(self, *args, **kwargs):
        ''' if a specific record was requested, return it even if it's
        draft '''
        return self.all_with_draft().get(*args, **kwargs)
                     
    def filter(self, *args, **kwargs):
        ''' if pk was specified as a kwarg, return even
        if it's draft '''
        if 'pk' in kwargs:
            return self.all_with_draft().filter(*args, **kwargs)
        return self.get_query_set().filter(*args, **kwargs)


class DeviceImage(models.Model):
    device = models.ForeignKey('Device', related_name='images')
    image = FileBrowseField(
        "Image",
        max_length=200, 
        directory="images/", 
        extensions=['.jpg', '.jpeg', '.gif','.png','.tif','.tiff'], 
        blank=True, 
        null=True
    )


class SoftwareImage(models.Model):
    software = models.ForeignKey('Software', related_name='images')
    image = FileBrowseField(
        max_length=200, 
        directory="images/", 
        extensions=['.jpg', '.jpeg', '.gif','.png','.tif','.tiff'], 
        format='Image', 
        blank=True, 
        null=True
    )


class VocabularyImage(models.Model):
    vocabulary = models.ForeignKey('Vocabulary', related_name='images')
    image = FileBrowseField(
        max_length=200, 
        directory="images/", 
        extensions=['.jpg', '.jpeg', '.gif','.png','.tif','.tiff'], 
        format='Image', 
        blank=True, 
        null=True
    )


class DeviceType(models.Model):
    date_created = models.DateTimeField(editable=False)
    date_updated = models.DateTimeField(editable=False)
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name

    def save(self, **kwargs):
        if not self.id:
            self.date_created = datetime.now() # Edit created timestamp only if it's new entry
        self.date_updated = datetime.now()
        super(DeviceType,self).save()

    class Meta:
        ordering = ['-id']


class ScanningIndication(models.Model):
    date_created = models.DateTimeField(editable=False)
    date_updated = models.DateTimeField(editable=False)
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name

    def save(self, **kwargs):
        if not self.id:
            self.date_created = datetime.now() # Edit created timestamp only if it's new entry
        self.date_updated = datetime.now()
        super(ScanningIndication,self).save()


class PredictionEnhancement(models.Model):
    date_created = models.DateTimeField(editable=False)
    date_updated = models.DateTimeField(editable=False)
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name

    def save(self, **kwargs):
        if not self.id:
            self.date_created = datetime.now() # Edit created timestamp only if it's new entry
        self.date_updated = datetime.now()
        super(PredictionEnhancement,self).save()

    class Meta:
        ordering = ['-id']


class AuditoryScanning(models.Model):
    date_created = models.DateTimeField(editable=False)
    date_updated = models.DateTimeField(editable=False)
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name

    def save(self, **kwargs):
        if not self.id:
            self.date_created = datetime.now() # Edit created timestamp only if it's new entry
        self.date_updated = datetime.now()
        super(AuditoryScanning,self).save()

    class Meta:
        ordering = ['-id']


class LanguageLevel(models.Model):
    date_created = models.DateTimeField(editable=False)
    date_updated = models.DateTimeField(editable=False)
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name

    def save(self, **kwargs):
        if not self.id:
            self.date_created = datetime.now() # Edit created timestamp only if it's new entry
        self.date_updated = datetime.now()
        super(LanguageLevel,self).save()

    class Meta:
        ordering = ['-id']


class OperatingSystem(models.Model):
    date_created = models.DateTimeField(editable=False)
    date_updated = models.DateTimeField(editable=False)
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name

    def save(self, **kwargs):
        if not self.id:
            self.date_created = datetime.now() # Edit created timestamp only if it's new entry
        self.date_updated = datetime.now()
        super(OperatingSystem,self).save()

    class Meta:
        ordering = ['-id']


class Supplier(models.Model):
    date_created = models.DateTimeField(editable=False)
    date_updated = models.DateTimeField(editable=False)
    name = models.CharField(max_length=30)
    slug = models.SlugField(unique=True)
    address = tinymce_models.HTMLField()
    postcode = models.CharField(max_length=8, null=True, blank=True)
    phone_number = models.CharField(max_length=50, null=True, blank=True)
    fax_number = models.CharField(max_length=50, null=True, blank=True)
    email_address = models.EmailField(null=True, blank=True)
    website_url = models.CharField(max_length=255, null=True, blank=True)
    bhta_member = models.BooleanField()
    switch_access = models.BooleanField()
    googlemap = models.URLField(null=True, blank=True)
    no_longer_trading = models.BooleanField()
    notes = tinymce_models.HTMLField(null=True, blank=True)

    def __unicode__(self):
        return self.name

    def save(self, **kwargs):
        if not self.id:
            self.date_created = datetime.now() # Edit created timestamp only if it's new entry
        self.date_updated = datetime.now()
        super(Supplier,self).save()


class Document(models.Model):
    date_created = models.DateTimeField(editable=False)
    date_updated = models.DateTimeField(editable=False)
    name = models.CharField(max_length=100)
    file = models.FileField(upload_to='docs')
    supplier = models.ForeignKey(Supplier, null=True, blank=True)

    def __unicode__(self):
        return self.name

    def save(self, **kwargs):
        if not self.id:
            self.date_created = datetime.now() # Edit created timestamp only if it's new entry
        self.date_updated = datetime.now()
        super(Document,self).save()


class Access(models.Model):
    date_created = models.DateTimeField(editable=False)
    date_updated = models.DateTimeField(editable=False)
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name

    def save(self, **kwargs):
        if not self.id:
            self.date_created = datetime.now() # Edit created timestamp only if it's new entry
        self.date_updated = datetime.now()
        super(Access,self).save()

    class Meta:
        ordering = ['-id']


class SymbolLibrary(models.Model):
    date_created = models.DateTimeField(editable=False)
    date_updated = models.DateTimeField(editable=False)
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name

    def save(self, **kwargs):
        if not self.id:
            self.date_created = datetime.now() # Edit created timestamp only if it's new entry
        self.date_updated = datetime.now()
        super(SymbolLibrary,self).save()


class WheelchairMount(models.Model):
    date_created = models.DateTimeField(editable=False)
    date_updated = models.DateTimeField(editable=False)
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name

    def save(self, **kwargs):
        if not self.id:
            self.date_created = datetime.now() # Edit created timestamp only if it's new entry
        self.date_updated = datetime.now()
        super(WheelchairMount,self).save()


class Voice(models.Model):
    date_created = models.DateTimeField(editable=False)
    date_updated = models.DateTimeField(editable=False)
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name

    def save(self, **kwargs):
        if not self.id:
            self.date_created = datetime.now() # Edit created timestamp only if it's new entry
        self.date_updated = datetime.now()
        super(Voice,self).save()


class VocabularyManager(DraftManager):
    def search(self, terms):
        q_objects = []

        for term in terms:
            q_objects.append(Q(name=term))

        # Start with a bare QuerySet
        qs = self.get_query_set()

        # Use operator's or_ to string together all of your Q objects.
        return qs.filter(reduce(operator.or_, q_objects))


class Vocabulary(models.Model):
    VOCABULARY_TYPE_CHOICES = (
        ('topic', 'Mainly topic based'),
        ('syntax', 'Mainly syntax based'),
        ('scene', 'Visual scene based'),
    )

    LANGUAGE_REPRESENTATION_CHOICES = (
        ('text', 'Text only (letters, words, phrases)'),
        ('single', 'Text and single meaning symbols'),
        ('multi', 'Text and multi-meaning symbols'),
    )

    date_created = models.DateTimeField(editable=False)
    date_updated = models.DateTimeField(editable=False)
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    date_uk_release = models.DateField(null=True, blank=True)
    draft = models.BooleanField()
    discontinued = models.BooleanField()
    update = models.BooleanField()
    new_features = tinymce_models.HTMLField(null=True, blank=True)
    short_description = tinymce_models.HTMLField()
    long_description = tinymce_models.HTMLField(null=True, blank=True)
    guide_price_gbp = models.PositiveIntegerField(null=True, blank=True)
    guide_price_na = models.BooleanField()
    guide_price_notes = tinymce_models.HTMLField(null=True, blank=True)
    suppliers = models.ManyToManyField(Supplier)
    type = models.CharField(
        max_length=6, 
        choices=VOCABULARY_TYPE_CHOICES, 
        null=True, 
        blank=True
    )
    language_level = models.ManyToManyField(
        LanguageLevel, 
        related_name='vocabulary_language_level', 
        null=True, 
        blank=True
    )
    use_of_colour_for_navigation = models.BooleanField()
    use_of_colour_for_grammar = models.BooleanField()
    switch_access = models.BooleanField()
    on_screen_keyboard = models.BooleanField()
    language_representation = models.CharField(
        max_length=6, 
        choices=LANGUAGE_REPRESENTATION_CHOICES, 
        null=True, 
        blank=True
    )
    prediction = models.BooleanField()
    documents = models.ManyToManyField(
        Document, 
        related_name = 'vocabulary_documents', 
        null = True, 
        blank = True,
    )

    objects = VocabularyManager()

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return "/vocabulary/%s/" % (self.slug)

    def save(self, **kwargs):
        if not self.id:
            self.date_created = datetime.now() # Edit created timestamp only if it's new entry
        self.date_updated = datetime.now()
        super(Vocabulary,self).save()


class SoftwareManager(DraftManager):
    def search(self, terms):
        q_objects = []

        for term in terms:
            q_objects.append(Q(name=term))

        # Start with a bare QuerySet
        qs = self.get_query_set()

        # Use operator's or_ to string together all of your Q objects.
        return qs.filter(reduce(operator.or_, q_objects))


class Software(models.Model):
    MESSAGE_VIEW_CHOICES =(
        ('text', 'Text'),
        ('symbols', 'Text and symbols'),
    )

    AUDITORY_SCANNING_CHOICES =(
        ('none', 'None'),
        ('beep', 'Beep'),
        ('switch', 'Speech prompt for switch users only'),
        ('keypress', 'Speech prompt on keypress'),
    )

    date_created = models.DateTimeField(editable=False)
    date_updated = models.DateTimeField(editable=False)
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    date_uk_release = models.DateField(
        null=True, 
        blank=True, 
        editable=False
    )
    draft = models.BooleanField()
    discontinued = models.BooleanField()
    update = models.BooleanField()
    new_features = tinymce_models.HTMLField(null=True, blank=True)
    short_description = tinymce_models.HTMLField()
    long_description = tinymce_models.HTMLField(null=True, blank=True)
    version = models.CharField(max_length=30, null=True, blank=True)
    guide_price_gbp = models.PositiveIntegerField(null=True, blank=True)
    guide_price_na = models.BooleanField()
    guide_price_notes = tinymce_models.HTMLField(null=True, blank=True)
    suppliers = models.ManyToManyField(Supplier)
    operating_system = models.ManyToManyField(
        OperatingSystem, 
        related_name = 'software_operating_system', 
        null = True, 
        blank = True,
    )
    number_supplied_voices = models.PositiveIntegerField(
        null=True, 
        blank=True
    )
    supplied_voices = models.ManyToManyField(
        Voice, 
        related_name='software_supplied_voices', 
        null=True, 
        blank=True
    )
    compatible_voices = models.ManyToManyField(Voice, related_name='software_compatible_voices', null=True, blank=True)
    access_methods = models.ManyToManyField(Access, related_name='software_access_methods', null=True, blank=True)
    speech_type = models.CharField(max_length=10, choices=SPEECH_TYPE_CHOICES, null=True, blank=True)
    number_supplied_symbol_libraries = models.PositiveIntegerField(null=True, blank=True)
    supplied_symbol_libraries = models.ManyToManyField(SymbolLibrary, related_name='software_supplied_symbol_libraries', null=True, blank=True)
    compatible_symbol_libraries = models.ManyToManyField(SymbolLibrary, related_name='software_compatible_symbol_libraries', null=True, blank=True)
    symbol_libraries_notes = tinymce_models.HTMLField(null=True, blank=True)
    number_supplied_vocabularies = models.PositiveIntegerField(null=True, blank=True)
    supplied_vocabularies = models.ManyToManyField(Vocabulary, related_name='software_supplied_vocabularies', null=True, blank=True)
    compatible_vocabularies = models.ManyToManyField(Vocabulary, related_name='software_compatible_vocabularies', null=True, blank=True)
    vocabularies_notes = tinymce_models.HTMLField(null=True, blank=True)
    multiple_users = models.BooleanField()
    second_language_support = models.BooleanField()
    message_view = models.CharField(max_length=7, choices=MESSAGE_VIEW_CHOICES, null=True, blank=True)
    editable_dictionary = models.BooleanField()
    prediction_enhancement = models.ManyToManyField(PredictionEnhancement, related_name='software_prediction_enhancement', null=True, blank=True)
    auditory_scanning = models.ManyToManyField(AuditoryScanning, related_name='software_auditory_scanning', null=True, blank=True)
    cell_magnification = models.BooleanField()
    environmental_control = models.BooleanField()
    documents = models.ManyToManyField(
        Document, 
        related_name = 'software_documents', 
        null = True, 
        blank = True,
    )

    objects = SoftwareManager()

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return "/software/%s/" % (self.slug)

    def save(self, **kwargs):
        if not self.id:
            self.date_created = datetime.now() # Edit created timestamp only if it's new entry
        self.date_updated = datetime.now()
        super(Software,self).save()


class DeviceManager(DraftManager):
    def search(self, terms):
        q_objects = []

        for term in terms:
            q_objects.append(Q(name=term))
            q_objects.append(Q(slug=term))

        # Start with a bare QuerySet
        qs = self.get_query_set()

        # Use operator's or_ to string together all of your Q objects.
        return qs.filter(reduce(operator.or_, q_objects))


class Device(models.Model):
    NUMBER_MESSAGES_CHOICES = (
        ('single', 'Single'),
        ('2-16', '2-16'),
        ('over-16', 'Over 16'),
    )

    INTERNET_CAPABLE_CHOICES = (
        ('no', 'No'),
        ('built-in', 'Yes, built in'),
        ('add-on', 'Yes, via add-on equipment'),
    )

    KEYGUARD_CHOICES = (
        ('no', 'No'),
        ('built-in', 'Yes, built in'),
        ('off-the-shelf', 'Yes, off-the-shelf'),
        ('custom-made', 'Yes, custom-made by supplier'),
    )

    TOUCHSCREEN_CHOICES = (
        ('small', 'Palmtop size'),
        ('medium', 'Paperback size'),
        ('large', 'Laptop size'),
    )

    MOBILE_PHONE_CAPABLE_CHOICES = (
        ('none', 'None'),
        ('text', 'Text only'),
        ('built-in', 'Live calling, built in'),
        ('aircard', 'Live calling, via AirCard'),
        ('bluetooth', 'Live calling, via Bluetooth'),
    )

    WHEELCHAIR_MOUNT_CHOICES = (
        ('none', 'None'),
        ('included', 'Included'),
        ('optional', 'Optional'),
    )

    TABLE_STAND_CHOICES = (
        ('none', 'None'),
        ('integral', 'Integral'),
        ('included', 'Included'),
        ('optional', 'Optional'),
    )

    date_created = models.DateTimeField(editable=False)
    date_updated = models.DateTimeField(editable=False)
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    aka = models.CharField(max_length=100, null=True, blank=True)
    date_uk_release = models.DateField(null=True, blank=True, editable=False)
    draft = models.BooleanField()
    discontinued = models.BooleanField()
    update = models.BooleanField()
    new_features = tinymce_models.HTMLField(null=True, blank=True)
    device_type = models.ManyToManyField(DeviceType, related_name='device_device_type')
    short_description = tinymce_models.HTMLField()
    long_description = tinymce_models.HTMLField(null=True, blank=True)
    guide_price_gbp = models.PositiveIntegerField(null=True, blank=True)
    guide_price_na = models.BooleanField()
    guide_price_notes = tinymce_models.HTMLField(null=True, blank=True)
    access_methods = models.ManyToManyField(
        Access, 
        related_name='device_access_methods', 
        null=True, 
        blank=True
    )
    scanning_indication = models.ManyToManyField(
        ScanningIndication, 
        related_name='device_scanning_indication', 
        null=True, 
        blank=True
    )
    speech_type = models.CharField(
        max_length=10, 
        choices=SPEECH_TYPE_CHOICES
    )
    internet_capable = models.CharField(
        max_length = 9, 
        choices = INTERNET_CAPABLE_CHOICES, 
        null = True, 
        blank = True,
        default = 'no',
    )
    number_messages = models.CharField(
        max_length=11, 
        choices=NUMBER_MESSAGES_CHOICES, 
        null=True, 
        blank=True
    )
    max_number_messages = models.CharField(
        max_length=100,
        null=True, 
        blank=True
    )
    message_levels = models.BooleanField()
    number_message_levels = models.PositiveIntegerField(null=True, blank=True)
    number_supplied_vocabularies = models.PositiveIntegerField(
        null = True, 
        blank = True,
        editable = False,
    )
    supplied_vocabularies = models.ManyToManyField(
        Vocabulary, 
        related_name = 'device_supplied_vocabularies', 
        null = True, 
        blank = True,
        editable = False,
    )
    compatible_vocabularies = models.ManyToManyField(
        Vocabulary, 
        related_name = 'device_compatible_vocabularies', 
        null = True, 
        blank = True,
        editable = False,
    )
    vocabularies_notes = tinymce_models.HTMLField(
        null = True, 
        blank = True,
        editable = False,
    )
    uses_software = models.BooleanField()
    install_own_software = models.BooleanField(
        verbose_name='Can install own software',
    )
    number_supplied_software = models.PositiveIntegerField(
        null=True, 
        blank=True
    )
    supplied_software = models.ManyToManyField(
        Software, 
        related_name='device_supplied_software', 
        null=True, 
        blank=True
    )
    compatible_software = models.ManyToManyField(
        Software, 
        related_name='device_compatible_software', 
        null=True, 
        blank=True
    )
    software_notes = tinymce_models.HTMLField(null=True, blank=True)
    number_supplied_symbol_libraries = models.PositiveIntegerField(
        null=True, 
        blank=True
    )
    supplied_symbol_libraries = models.ManyToManyField(
        SymbolLibrary, 
        related_name='device_supplied_symbol_libraries', 
        null=True, 
        blank=True
    )
    compatible_symbol_libraries = models.ManyToManyField(
        SymbolLibrary, 
        related_name='device_compatible_symbol_libraries', 
        null=True, 
        blank=True
    )
    symbol_libraries_notes = tinymce_models.HTMLField(null=True, blank=True)
    keyguards = models.CharField(
        max_length = 20, 
        choices = KEYGUARD_CHOICES, 
        null = True, 
        blank = True,
        default = 'no',
    )
    touchscreen = models.CharField(
        max_length=6, 
        choices=TOUCHSCREEN_CHOICES, 
        null=True, 
        blank=True
    )
    screen_size_cm = models.FloatField(null = True, blank = True)
    screen_size_na = models.BooleanField()
    weight_kg = models.FloatField(
        null=True, 
        blank=True,
        help_text='Leave blank if not known',
    )
    width_cm = models.FloatField(
        null=True, 
        blank=True,
        help_text='Leave blank if not known',
    )
    height_cm = models.FloatField(
        null=True, 
        blank=True,
        help_text='Leave blank if not known',
    )
    depth_cm = models.FloatField(
        null=True, 
        blank=True,
        help_text='Leave blank if not known',
    )
    environmental_control = models.BooleanField()
    environmental_control_notes = tinymce_models.HTMLField(
        null=True, 
        blank=True
    )
    operating_system = models.ManyToManyField(
        OperatingSystem, 
        related_name = 'device_operating_system', 
        null = True, 
        blank = True,
    )
    mobile_phone_capable = models.CharField(
        max_length=9, 
        choices=MOBILE_PHONE_CAPABLE_CHOICES, 
        null=True, 
        blank=True,
    )
    battery_life = models.TextField(
        null = True, 
        blank = True,
    )
    battery_life_hours = models.FloatField(
        null = True, 
        blank = True,
    )
    wheelchair_mount = models.CharField(
        max_length = 8, 
        choices = WHEELCHAIR_MOUNT_CHOICES, 
        null = True, 
        blank = True,
        default = 'none',
    )
    compatible_wheelchair_mount = models.ManyToManyField(
        WheelchairMount, 
        related_name='device_compatible_wheelchair_mount', 
        null=True, 
        blank=True
    )
    table_stand = models.CharField(
        max_length = 8, 
        choices = TABLE_STAND_CHOICES, 
        null = True, 
        blank = True,
        default = 'none',
    )
    touchscreen = models.CharField(
        max_length = 6, 
        choices = TOUCHSCREEN_CHOICES, 
        null = True, 
        blank = True,
    )
    documents = models.ManyToManyField(
        Document, 
        related_name = 'device_documents', 
        null = True, 
        blank = True,
    )
    colours = tinymce_models.HTMLField(null=True, blank=True)
    warranty_notes = tinymce_models.HTMLField(null=True, blank=True)
    suppliers = models.ManyToManyField(Supplier)

    objects = DeviceManager()

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return "/device/%s/" % (self.slug)

    def save(self, **kwargs):
        if not self.id:
            self.date_created = datetime.now() # Edit created timestamp only if it's new entry
        self.date_updated = datetime.now()
        super(Device,self).save()
