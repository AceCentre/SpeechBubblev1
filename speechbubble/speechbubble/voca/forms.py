import django.forms as forms
import models

BINARY_CHOICES = (
    ('', 'Not important'),
    ('1', 'Yes'),
)

suppliers = models.Supplier.objects.order_by('name')

SUPPLIER_CHOICES = [
    ('', 'Select supplier'),
]

for supplier in suppliers:
    SUPPLIER_CHOICES.append((supplier.slug, supplier.name))

access_methods = models.Access.objects.all()

ACCESS_CHOICES = []

for access_method in access_methods:
    ACCESS_CHOICES.append((access_method.name, access_method.name))

softwares = models.Software.objects.order_by('name')

SOFTWARE_CHOICES = [
   ('', 'choose software'),
]

for software in softwares:
    SOFTWARE_CHOICES.append((software.slug, software.name))

vocabularies = models.Vocabulary.objects.order_by('name')

VOCABULARY_CHOICES = [
    ('', 'choose vocabulary'),
]

for vocabulary in vocabularies:
    VOCABULARY_CHOICES.append((vocabulary.slug, vocabulary.name))

PHYSICAL_SORT_BY_CHOICES = (
    ('name', 'name'),
    ('price_low', 'price (lowest first)'),
    ('price_high', 'price (highest first)'),
    ('weight_low', 'weight (lowest first)'),
    ('weight_high', 'weight (highest first)'),
)

ABSTRACT_SORT_BY_CHOICES = (
    ('name', 'name'),
    ('price_low', 'price (lowest first)'),
    ('price_high', 'price (highest first)'),
)

class DeviceSearchForm(forms.Form):
    DEVICE_TYPE_CHOICES = (
        ('Simple aid with 1 message', 'Simple aids with one message'),
        ('Simple aid with 2 to 16 messages', 'Simple aids with 2 to 16 messages'),
        ('Midrange aid without touchscreen', 'Midrange aid without touchscreen'),
        ('Computer-based aid with touchscreen', 'Computer-based aids with touchscreen'),
        ('Handheld PDA-based aid', 'Handheld PDA-based aids'),
        ('Aid with typing keyboard for literate users', 'Aids with built-in letter keyboards'),
    )

    device_type = forms.MultipleChoiceField(
        choices = DEVICE_TYPE_CHOICES, 
        widget = forms.CheckboxSelectMultiple,
        required = False,
    )

    supplier = forms.ChoiceField(
        choices = SUPPLIER_CHOICES, 
        required = False,
    )

    access = forms.MultipleChoiceField(
        choices = ACCESS_CHOICES, 
        widget = forms.CheckboxSelectMultiple,
        required = False,
    )

    NUMBER_MESSAGES_CHOICES = (
        ('', 'Not important'),
        ('single', '1 only'),
        ('2-16', '2-16'),
        ('over-16', 'Over 16'),
    )

    number_messages = forms.ChoiceField(
        choices = NUMBER_MESSAGES_CHOICES,
        widget = forms.RadioSelect,
        required = False,
    )

    SCANNING_FEEDBACK_CHOICES = (
        ('Visual', 'Visual (eg scanned item lights up)'),
        ('Beep', 'Beep'),
        ('Spoken', 'Spoken (ie auditory feedback)'),
    )

    scanning_feedback = forms.MultipleChoiceField(
        choices = SCANNING_FEEDBACK_CHOICES, 
        widget = forms.CheckboxSelectMultiple,
        required = False,
    )

    SPEECH_TYPE_CHOICES = (
        ('', 'Not important'),
        ('recorded', 'Recorded speech'),
        ('artificial', 'Artificial'),
    )

    speech_type = forms.ChoiceField(
        choices = SPEECH_TYPE_CHOICES,
        widget = forms.RadioSelect,
        required = False,
    )

    KEYGUARD_CHOICES = (
        ('built-in', "Built-in keyguards"),
        ('off-the-shelf', "Off-the-shelf keyguards available"),
        ('custom-made', "Custom-made by the supplier"),
    )

    keyguard = forms.MultipleChoiceField(
        choices = KEYGUARD_CHOICES,
        widget = forms.CheckboxSelectMultiple,
        required = False,
    )

    TOUCHSCREEN_SIZE_CHOICES = (
        ('', 'Not important'),
        ('small', 'Palmtop size'),
        ('medium', 'Paperback size'),
        ('large', 'Laptop size'),
    )

    touchscreen_size = forms.ChoiceField(
        choices = TOUCHSCREEN_SIZE_CHOICES,
        widget = forms.RadioSelect,
        required = False,
    )

    OPERATING_SYSTEM_CHOICES = (
        ('', 'Not important'),
        ('Dedicated', 'Dedicated'),
        ('Windows', 'Windows'),
        ('Macintosh', 'Macintosh'),
        ('Other', 'Other'),
    )

    operating_system = forms.ChoiceField(
        choices = OPERATING_SYSTEM_CHOICES,
        widget = forms.RadioSelect,
        required = False,
    )

    environmental_control = forms.ChoiceField(
        choices = BINARY_CHOICES,
        widget = forms.RadioSelect,
        required = False,
    )

    install_own_software = forms.ChoiceField(
        choices = BINARY_CHOICES,
        widget = forms.RadioSelect,
        required = False,
    )

    MOBILE_PHONE_CAPABLE_CHOICES = (
        ('', 'Not important'),
        ('text', 'Texting only'),
        ('built-in', 'Voice calling built-in'),
        ('aircard', 'Voice calling via aircard'),
        ('bluetooth', 'Voice calling via bluetooth'),
    )

    mobile_phone_capable = forms.ChoiceField(
        choices = MOBILE_PHONE_CAPABLE_CHOICES,
        widget = forms.RadioSelect,
        required = False,
    )

    INTERNET_CAPABLE_CHOICES = (
        ('', 'Not important'),
        ('built-in', 'Yes, built-in'),
        ('add-on', 'Yes, via add-on equipment'),
    )

    internet_capable = forms.ChoiceField(
        choices = INTERNET_CAPABLE_CHOICES,
        widget = forms.RadioSelect,
        required = False,
    )

    WHEELCHAIR_MOUNT_CHOICES = (
        ('', 'Not important'),
        ('included', 'Yes, included'),
        ('optional', 'Yes, optional'),
    )

    wheelchair_mount = forms.ChoiceField(
        choices = WHEELCHAIR_MOUNT_CHOICES,
        widget = forms.RadioSelect,
        required = False,
    )

    software = forms.ChoiceField(
        choices = SOFTWARE_CHOICES,
        required = False,
    )

    vocabulary = forms.ChoiceField(
        choices = VOCABULARY_CHOICES,
        required = False,
    )

    weight = forms.FloatField(
        required = False,
    )

    sort_by = forms.ChoiceField(
        choices = PHYSICAL_SORT_BY_CHOICES,
        required = False,
    )

class SoftwareSearchForm(forms.Form):
    supplier = forms.ChoiceField(
        choices = SUPPLIER_CHOICES, 
        required = False,
    )

    access = forms.MultipleChoiceField(
        choices = ACCESS_CHOICES, 
        widget = forms.CheckboxSelectMultiple,
        required = False,
    )

    AUDITORY_SCANNING_CHOICES = (
        ('Beep', 'Beep'),
        ('Switch prompt on keypress', 'Spoken prompt when pressing a key'),
        ('Switch propmt for switch users only', 'Spoken prompt for switch users'),
    )

    auditory_scanning = forms.MultipleChoiceField(
        choices = AUDITORY_SCANNING_CHOICES,
        widget = forms.CheckboxSelectMultiple,
        required = False,
    )

    multiple_users = forms.ChoiceField(
        choices = BINARY_CHOICES, 
        widget = forms.RadioSelect,
        required = False,
    )

    second_language_support = forms.ChoiceField(
        choices = BINARY_CHOICES, 
        widget = forms.RadioSelect,
        required = False,
    )

    message_view = forms.ChoiceField(
        choices = BINARY_CHOICES,
        widget = forms.RadioSelect,
        required = False,
    )

    PREDICTION_ENHANCEMENT_CHOICES = (
       ('Prediction (letter)', 'Prediction (letter)'),
       ('Prediction (word)', 'Prediction (word)'),
       ('Prediction (grammatical)', 'Prediction (grammatical)'),
       ('Prediction (smart)', 'Prediction (smart)'),
       ('Abbreviation expansion', 'Abbreviation expansion'),
       ('Whole message storage', 'Whole message storage'),
       ('Semantic compaction', 'Semantic compaction (MinSpeak)'),
    )

    prediction_enhancement = forms.MultipleChoiceField(
        choices = PREDICTION_ENHANCEMENT_CHOICES,
        widget = forms.CheckboxSelectMultiple,
        required = False,
    )

    editable_dictionary = forms.ChoiceField(
        choices = BINARY_CHOICES, 
        widget = forms.RadioSelect,
        required = False,
    )

    environmental_control = forms.ChoiceField(
        choices = BINARY_CHOICES, 
        widget = forms.RadioSelect,
        required = False,
    )

    cell_magnification = forms.ChoiceField(
        choices = BINARY_CHOICES, 
        widget = forms.RadioSelect,
        required = False,
    )

    vocabulary = forms.ChoiceField(
        choices = VOCABULARY_CHOICES,
        required = False,
    )

    sort_by = forms.ChoiceField(
        choices = ABSTRACT_SORT_BY_CHOICES,
        required = False,
    )

class VocabularySearchForm(forms.Form):
    supplier = forms.ChoiceField(
        choices = SUPPLIER_CHOICES, 
        required = False,
    )

    LANGUAGE_REPRESENTATION_CHOICES = (
        ('', 'Not important'),
        ('text', 'Text only (letters, words, phrases)'),
        ('single', 'Text and single meaning symbols'),
        ('multi', 'Text and multi-meaning symbols'),
    )

    language_representation = forms.ChoiceField(
        choices = LANGUAGE_REPRESENTATION_CHOICES,
        widget = forms.RadioSelect,
        required = False,
    )

    VOCABULARY_TYPE_CHOICES = (
        ('', 'Not important'),
        ('topic', 'Mainly topic based'),
        ('syntax', 'Mainly syntax based'),
        ('scene', 'Visual scene based'),
    )

    type = forms.ChoiceField(
        choices = VOCABULARY_TYPE_CHOICES,
        widget = forms.RadioSelect,
        required = False,
    )

    switch_access = forms.ChoiceField(
        choices = BINARY_CHOICES,
        widget = forms.RadioSelect,
        required = False,
    )

    on_screen_keyboard = forms.ChoiceField(
        choices = BINARY_CHOICES,
        widget = forms.RadioSelect,
        required = False,
    )

    prediction = forms.ChoiceField(
        choices = BINARY_CHOICES,
        widget = forms.RadioSelect,
        required = False,
    )

    software = forms.ChoiceField(
        choices = SOFTWARE_CHOICES,
        required = False,
    )

    sort_by = forms.ChoiceField(
        choices = ABSTRACT_SORT_BY_CHOICES,
        required = False,
    )
