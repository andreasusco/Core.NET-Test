from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Associazione, User, SedeDistaccata, MembroConsiglio, RuoloReferente, Contatto, EmailTemplate

class ContattoInline(admin.TabularInline):
    model = Contatto
    extra = 1

class SedeDistaccataInline(admin.TabularInline):
    model = SedeDistaccata
    extra = 1

class MembroConsiglioInline(admin.TabularInline):
    model = MembroConsiglio
    extra = 1

@admin.register(Associazione)
class AssociazioneAdmin(admin.ModelAdmin):
    list_display = ('denominazione', 'indirizzo_principale')
    search_fields = ('denominazione',)
    inlines = [SedeDistaccataInline, MembroConsiglioInline, ContattoInline]

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role', 'associazione')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('role', 'associazione')}),
    )

@admin.register(RuoloReferente)
class RuoloReferenteAdmin(admin.ModelAdmin):
    list_display = ('nome_ruolo',)

@admin.register(Contatto)
class ContattoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cognome', 'ruolo', 'associazione')
    list_filter = ('associazione', 'ruolo')
    search_fields = ('nome', 'cognome', 'email')

@admin.register(EmailTemplate)
class EmailTemplateAdmin(admin.ModelAdmin):
    list_display = ('nome_template', 'oggetto')
    search_fields = ('nome_template', 'oggetto')
