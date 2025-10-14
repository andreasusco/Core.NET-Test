from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.shortcuts import redirect
from django.urls import reverse

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        """
        Interviene dopo il login social ma prima della creazione/login dell'utente Django.
        Se l'utente non esiste ancora, lo reindirizziamo a una pagina di registrazione
        personalizzata per inserire il codice univoco.
        """
        # Se l'utente esiste già nel nostro sistema, procedi normalmente
        if sociallogin.is_existing:
            return

        # Metti i dati del login social nella sessione per recuperarli dopo
        request.session['sociallogin_data'] = sociallogin.serialize()

        # Reindirizza alla pagina di registrazione personalizzata
        return redirect('associazione_register')