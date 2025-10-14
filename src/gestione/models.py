from django.contrib.auth.models import AbstractUser
from django.db import models


class Associazione(models.Model):
    """
    Modello per i dati anagrafici dell'associazione.
    """
    denominazione = models.CharField(max_length=255, unique=True)
    logo = models.ImageField(upload_to='loghi/', blank=True, null=True)
    indirizzo_principale = models.TextField()
    codice_univoco = models.CharField(
        max_length=50, unique=True,
        help_text="Codice univoco fornito per la registrazione iniziale."
    )

    def __str__(self):
        return self.denominazione

    class Meta:
        verbose_name_plural = "Associazioni"


class User(AbstractUser):
    """
    Modello utente personalizzato per gestire ruoli e associazione.
    """
    class Role(models.TextChoices):
        MASTER = "MASTER", "Master"
        ADMIN = "ADMIN", "Admin"

    role = models.CharField(max_length=50, choices=Role.choices)
    associazione = models.ForeignKey(
        Associazione, on_delete=models.CASCADE,
        null=True, blank=True, related_name='utenti'
    )


class SedeDistaccata(models.Model):
    """
    Sedi distaccate di un'associazione.
    """
    associazione = models.ForeignKey(
        Associazione, on_delete=models.CASCADE, related_name='sedi_distaccate'
    )
    indirizzo = models.TextField()

    def __str__(self):
        return f"Sede di {self.associazione.denominazione} - {self.indirizzo[:30]}..."

    class Meta:
        verbose_name_plural = "Sedi Distaccate"


class MembroConsiglio(models.Model):
    """
    Membri del consiglio direttivo (Presidente, Consiglieri).
    """
    associazione = models.ForeignKey(
        Associazione, on_delete=models.CASCADE, related_name='consiglio'
    )
    nome = models.CharField(max_length=100)
    cognome = models.CharField(max_length=100)
    ruolo = models.CharField(max_length=100, help_text="Es. Presidente, Consigliere")

    def __str__(self):
        return f"{self.nome} {self.cognome} ({self.ruolo}) - {self.associazione.denominazione}"

    class Meta:
        verbose_name_plural = "Membri del Consiglio"


class RuoloReferente(models.Model):
    """
    Ruoli predefiniti per i contatti (es. Referente Tecnico).
    """
    nome_ruolo = models.CharField(
        max_length=100, unique=True,
        help_text="Il nome del ruolo predefinito (es. Referente Tecnico)."
    )

    def __str__(self):
        return self.nome_ruolo

    class Meta:
        verbose_name_plural = "Ruoli Referente"


class Contatto(models.Model):
    """
    Contatti (referenti) di un'associazione.
    """
    associazione = models.ForeignKey(
        Associazione, on_delete=models.CASCADE, related_name='contatti'
    )
    ruolo = models.ForeignKey(
        RuoloReferente, on_delete=models.PROTECT, related_name='contatti'
    )
    nome = models.CharField(max_length=100)
    cognome = models.CharField(max_length=100)
    email = models.EmailField()
    telefono = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.nome} {self.cognome} ({self.ruolo.nome_ruolo}) - {self.associazione.denominazione}"

    class Meta:
        verbose_name_plural = "Contatti"


class EmailTemplate(models.Model):
    """
    Template per le email da inviare in blocco.
    """
    nome_template = models.CharField(max_length=100, unique=True)
    oggetto = models.CharField(max_length=255)
    corpo = models.TextField(help_text="Puoi usare placeholders come {{nome}} e {{cognome}}.")

    def __str__(self):
        return self.nome_template

    class Meta:
        verbose_name_plural = "Template Email"
