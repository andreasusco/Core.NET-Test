from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from allauth.socialaccount.helpers import complete_social_login
from allauth.socialaccount.models import SocialLogin
from .models import Associazione, User, Contatto, RuoloReferente, EmailTemplate

class AssociazioneRegistrationView(View):
    def get(self, request, *args, **kwargs):
        if 'sociallogin_data' not in request.session:
            return redirect('/') # Redirect if no social login data
        return render(request, 'gestione/associazione_register.html')

    def post(self, request, *args, **kwargs):
        sociallogin_data = request.session.get('sociallogin_data')
        if not sociallogin_data:
            return redirect('/')

        codice_univoco = request.POST.get('codice_univoco')
        try:
            associazione = Associazione.objects.get(codice_univoco=codice_univoco, utenti__isnull=True)
        except Associazione.DoesNotExist:
            # Codice non valido o associazione già registrata
            return render(request, 'gestione/associazione_register.html', {'error': 'Codice non valido o già utilizzato.'})

        # Completa il login social e crea l'utente
        sociallogin = SocialLogin.deserialize(sociallogin_data)
        user = sociallogin.user
        user.associazione = associazione
        user.role = User.Role.MASTER
        user.save()

        # Completa il processo di login
        sociallogin.connect(request, user)
        complete_social_login(request, sociallogin)

        # Rimuovi i dati dalla sessione
        del request.session['sociallogin_data']

        return redirect('dashboard')


class DashboardView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = request.user
        if user.role == User.Role.ADMIN:
            # L'admin vede tutte le associazioni
            associazioni = Associazione.objects.all()
            return render(request, 'gestione/admin_dashboard.html', {'associazioni': associazioni})

        # L'utente master vede la propria associazione
        associazione = user.associazione
        return render(request, 'gestione/dashboard.html', {'associazione': associazione})


class ReportingView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = request.user
        contatti = Contatto.objects.all()
        ruoli = RuoloReferente.objects.all()

        if user.role == User.Role.MASTER:
            contatti = contatti.filter(associazione=user.associazione)

        # Filtri
        ruolo_id = request.GET.get('ruolo')
        if ruolo_id:
            contatti = contatti.filter(ruolo_id=ruolo_id)

        context = {
            'contatti': contatti,
            'ruoli': ruoli,
            'templates': EmailTemplate.objects.all()
        }
        return render(request, 'gestione/reporting.html', context)

    def post(self, request, *args, **kwargs):
        template_id = request.POST.get('template_id')
        contatto_ids = request.POST.getlist('contatto_ids')

        template = EmailTemplate.objects.get(id=template_id)
        contatti = Contatto.objects.filter(id__in=contatto_ids)

        # Qui andrà la logica per l'invio email
        # Per ora, simuliamo con un messaggio.

        from django.contrib import messages
        from .services import get_gmail_service, send_email

        gmail_service = get_gmail_service()

        if gmail_service:
            for contatto in contatti:
                # Personalizza il corpo dell'email
                body = template.corpo.replace('{{nome}}', contatto.nome).replace('{{cognome}}', contatto.cognome)
                send_email(gmail_service, contatto.email, template.oggetto, body)
            messages.success(request, f"Invio email con template '{template.nome_template}' a {len(contatti)} contatti completato.")
        else:
            messages.warning(request, "Il servizio Gmail non è configurato. Impossibile inviare email.")

        return redirect('reporting')
