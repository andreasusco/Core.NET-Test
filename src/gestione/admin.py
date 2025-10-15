from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Associazione, User, SedeDistaccata, MembroConsiglio, Ruolo, Contatto, EmailTemplate

class SedeDistaccataInline(admin.TabularInline):
    model = SedeDistaccata
    extra = 1

class MembroConsiglioInline(admin.TabularInline):
    model = MembroConsiglio
    extra = 1

class RuoloInline(admin.TabularInline):
    model = Ruolo
    extra = 1

@admin.register(Associazione)
class AssociazioneAdmin(admin.ModelAdmin):
    list_display = ('denominazione', 'indirizzo_principale')
    search_fields = ('denominazione',)
    inlines = [SedeDistaccataInline, MembroConsiglioInline, RuoloInline]

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role', 'associazione')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('role', 'associazione')}),
    )

@admin.register(Ruolo)
class RuoloAdmin(admin.ModelAdmin):
    list_display = ('nome_ruolo', 'associazione')
    list_filter = ('associazione',)
    search_fields = ('nome_ruolo',)
    filter_horizontal = ('contatti',)

@admin.register(Contatto)
class ContattoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cognome', 'email')
    search_fields = ('nome', 'cognome', 'email')

@admin.register(EmailTemplate)
class EmailTemplateAdmin(admin.ModelAdmin):
    list_display = ('nome_template', 'oggetto')
    search_fields = ('nome_template', 'oggetto')
