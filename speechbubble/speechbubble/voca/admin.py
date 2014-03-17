from django.contrib import admin
from reversion.admin import VersionAdmin
import models


class DraftAdmin(VersionAdmin):
    list_display = ('__unicode__', 'draft',)
    list_filter = ('draft',)
    def queryset(self, request):
        """ Returns a QuerySet of all model instances 
        that can be edited by the
        admin site. This is used by changelist_view. """
        # Default: qs =  self.model._default_manager.get_query_set()
        qs = self.model._default_manager.all_with_draft()
        # TODO: this should be handled by some parameter to the ChangeList.
        ordering = self.ordering or () # otherwise we might try to *None, which is bad ;)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs

# this requires __unicode__ to be defined in your model


class DeviceImageInline(admin.TabularInline):
    model = models.DeviceImage
    extra = 3


class SoftwareImageInline(admin.TabularInline):
    model = models.SoftwareImage
    extra = 3

class VocabularyImageInline(admin.TabularInline):
    model = models.VocabularyImage
    extra = 3


class DeviceTypeAdmin(admin.ModelAdmin):
    list_display = ['name']

admin.site.register(models.DeviceType, DeviceTypeAdmin)


class ScanningIndicationAdmin(admin.ModelAdmin):
    list_display = ['name']

admin.site.register(models.ScanningIndication, ScanningIndicationAdmin)


class PredictionEnhancementAdmin(admin.ModelAdmin):
    list_display = ['name']

admin.site.register(models.PredictionEnhancement, PredictionEnhancementAdmin)


class AuditoryScanningAdmin(admin.ModelAdmin):
    list_display = ['name']

admin.site.register(models.AuditoryScanning, AuditoryScanningAdmin)


class LanguageLevelAdmin(admin.ModelAdmin):
    list_display = ['name']

admin.site.register(models.LanguageLevel, LanguageLevelAdmin)


class OperatingSystemAdmin(admin.ModelAdmin):
    list_display = ['name']

admin.site.register(models.OperatingSystem, OperatingSystemAdmin)


class SupplierAdmin(admin.ModelAdmin):
    list_display = ['name']

admin.site.register(models.Supplier, SupplierAdmin)


class DocumentAdmin(admin.ModelAdmin):
    list_display = ['name']

admin.site.register(models.Document, DocumentAdmin)


class AccessAdmin(admin.ModelAdmin):
    list_display = ['name']

admin.site.register(models.Access, AccessAdmin)


class SymbolLibraryAdmin(admin.ModelAdmin):
    list_display = ['name']

admin.site.register(models.SymbolLibrary, SymbolLibraryAdmin)


class WheelchairMountAdmin(admin.ModelAdmin):
    list_display = ['name']

admin.site.register(models.WheelchairMount, WheelchairMountAdmin)


class VoiceAdmin(admin.ModelAdmin):
    list_display = ['name']

admin.site.register(models.Voice, VoiceAdmin)


class VocabularyAdmin(DraftAdmin):
    ordering = ('name',)
    search_fields = ('name',)

    inlines = [ VocabularyImageInline, ]

    fieldsets = [
        ('Basic info', {
            'fields': [
                'name',
                'short_description',
                'suppliers',
            ],
            'classes': ['wide'],
           'description': "This is the minimum info require to create a record of software",
        }),

        ('More details', {
           'fields': [
                'type',
                'language_representation',
                #'language_level',
                #'new_features',
                #'update',
                'long_description',
           ],
           'classes': ['wide'],
           'description': "",
        }),

        ('Supplier details', {
           'fields': [
                'guide_price_gbp',
                'guide_price_na',
                'guide_price_notes',
                'discontinued',
                'documents',
           ],
           'classes': ['wide'],
           'description': "Information on obtaining the vocabulary",
        }),

        ('Features', {
           'fields': [
                'use_of_colour_for_navigation',
                'use_of_colour_for_grammar',
                'switch_access',
                'on_screen_keyboard',
                'prediction',
           ],
           'classes': ['wide'],
           'description': "",
        }),

        ('Advanced stuff', {
           'fields': [
                'draft',
                'slug',
           ],
           'classes': ['collapse', 'wide'],
           'description': "You usually won't need to edit these fields"
        }),
    ]

    prepopulated_fields = {'slug': ('name',)}

    filter_horizontal = (
        'suppliers',
        'language_level',
    )
admin.site.register(models.Vocabulary, VocabularyAdmin)


class SoftwareAdmin(DraftAdmin):
    ordering = ('name',)
    search_fields = ('name',)

    inlines = [ SoftwareImageInline, ]

    fieldsets = [
        ('Basic info', {
            'fields': [
                'name',
                'short_description',
                'suppliers',
            ],
            'classes': ['wide'],
           'description': "This is the minimum info require to create a record of software",
        }),

        ('More details', {
           'fields': [
                'version',
                #'new_features',
                #'update',
                'long_description',
           ],
           'classes': ['wide'],
           'description': "",
        }),

        ('Supplier details', {
           'fields': [
                'guide_price_gbp',
                'guide_price_na',
                'guide_price_notes',
                'discontinued',
                'documents',
           ],
           'classes': ['wide'],
           'description': "Information on obtaining the software",
        }),

        ('Interface', {
           'fields': [
                'access_methods',
                'message_view',
                'auditory_scanning',
           ],
           'classes': ['wide'],
           'description': "How the software is accessed",
        }),

        ('Speech', {
           'fields': [
                'speech_type',
                'number_supplied_voices',
                'supplied_voices',
                'compatible_voices',
           ],
           'classes': ['wide'],
           'description': "",
        }),

        ('Vocabularies', {
           'fields': [
                'number_supplied_vocabularies',
                'supplied_vocabularies',
                'compatible_vocabularies',
                'vocabularies_notes',
           ],
           'classes': ['wide'],
           'description': "",
        }),

        ('Symbol libraries', {
           'fields': [
                'number_supplied_symbol_libraries',
                'supplied_symbol_libraries',
                'compatible_symbol_libraries',
                'symbol_libraries_notes',
           ],
           'classes': ['wide'],
           'description': "",
        }),

        ('Features', {
           'fields': [
                'multiple_users',
                'second_language_support',
                'editable_dictionary',
                'cell_magnification',
                'environmental_control',
                'operating_system',
                'prediction_enhancement',
           ],
           'classes': ['wide'],
           'description': "",
        }),

        ('Advanced stuff', {
           'fields': [
                'draft',
                'slug',
           ],
           'classes': ['collapse', 'wide'],
           'description': "You usually won't need to edit these fields"
        }),
    ]

    prepopulated_fields = {'slug': ('name',)}

    filter_horizontal = (
        'operating_system',
        'access_methods',
        'prediction_enhancement',
        'auditory_scanning',
        'supplied_voices',
        'compatible_voices',
        'supplied_symbol_libraries',
        'compatible_symbol_libraries',
        'supplied_vocabularies',
        'compatible_vocabularies',
        'suppliers',
    )
admin.site.register(models.Software, SoftwareAdmin)


class DeviceAdmin(DraftAdmin):
    ordering = ('name',)
    search_fields = ('name',)

    inlines = [ DeviceImageInline, ]

    fieldsets = [
        ('Basic info', {
           'fields': [
                'name',
                'aka',
                'device_type',
                'short_description',
                'speech_type',
                'suppliers',
           ],
           'classes': ['wide'],
           'description': "This is the minimum info require to create a record of a device",
        }),

        ('Physical details', {
           'fields': [
                #'new_features',
                #'update',
                'long_description',
                'battery_life',
                'touchscreen',
                'screen_size_cm',
                'screen_size_na',
                'weight_kg',
                'width_cm',
                'height_cm',
                'depth_cm',
           ],
           'classes': ['wide'],
           'description': "Details of the device construction",
        }),

        ('Supplier details', {
           'fields': [
                'guide_price_gbp',
                'guide_price_na',
                'guide_price_notes',
                'discontinued',
                'warranty_notes',
                'documents',
           ],
           'classes': ['wide'],
           'description': "Supplier details",
        }),

        ('Interface', {
           'fields': [
                'access_methods',
                'scanning_indication',
                'number_messages',
                'max_number_messages',
                'message_levels',
                'number_message_levels',
           ],
           'classes': ['wide'],
           'description': "How the device operates",
        }),

        ('Software', {
           'fields': [
                'uses_software',
                'install_own_software',
                'number_supplied_software',
                'supplied_software',
                'compatible_software',
                'software_notes',
           ],
           'classes': ['wide'],
           'description': "",
        }),

#        ('Symbol libraries', {
#           'fields': [
#                'number_supplied_symbol_libraries',
#                'supplied_symbol_libraries',
#                'compatible_symbol_libraries',
#                'symbol_libraries_notes',
#           ],
#           'classes': ['wide'],
#           'description': "",
#        }),

        ('Features', {
           'fields': [
                'internet_capable',
                'environmental_control',
                'environmental_control_notes',
                'mobile_phone_capable',
                'wheelchair_mount',
                'compatible_wheelchair_mount',
                'table_stand',
                'keyguards',
                'colours',
           ],
           'classes': ['wide'],
           'description': "",
        }),

        ('Advanced stuff', {
           'fields': [
                'draft',
                'slug',
           ],
           'classes': ['collapse', 'wide'],
           'description': "You usually won't need to edit these fields"
        }),
    ]

    prepopulated_fields = {'slug': ('name',)}


    filter_horizontal = (
        'device_type',
        'documents',
        'access_methods',
        'scanning_indication',
        'supplied_vocabularies',
        'compatible_vocabularies',
        'supplied_software',
        'compatible_software',
        'supplied_symbol_libraries',
        'compatible_symbol_libraries',
        'operating_system',
        'compatible_wheelchair_mount',
        'suppliers',
    )

admin.site.register(models.Device, DeviceAdmin)
