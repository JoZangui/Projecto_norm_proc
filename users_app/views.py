""" users_app/views.py """
# users_app/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import get_user_model
from django.views.generic.edit import FormView
from django.conf import settings

# from mozilla_django_oidc.views import OIDCAuthenticationRequestView, OIDCAuthenticationCallbackView

from auth.exceptions import DomainNotAuthorized
from auth.utils import get_subsidiary_by_email
from auth.utils import get_trusted_domains, get_sso_domains
# from auth.oidc_client import build_authorization_redirect, exchange_code_for_claims, get_oidc_endpoints
from users_app.models import Profile
from .forms import UserRegistrationForm, EmailAuthenticationForm

def register(request):
    try:
        if request.user.is_authenticated:
            return render(request, 'users_app/profile.html')
    except AttributeError:
        print("AttributeError: 'AnonymousUser' object has no attribute 'is_authenticated'")

    if request.method == 'POST':
        # Handle form submission (not implemented here)
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            user_form.save()
            return redirect('home')
        return render(request, 'users_app/register.html', {'user_form': user_form})
    user_form = UserRegistrationForm()
    return render(request, 'users_app/register.html', {'user_form': user_form})

def profile(request):
    return render(request, 'users_app/profile.html')

# ! retornar quando for necessário o OIDC

# class LoginView(FormView):
    
#     template_name = "users_app/login.html"
#     form_class = EmailAuthenticationForm

#     def form_valid(self, form):
#         email = form.cleaned_data["email"]
#         domain = email.split("@")[-1]
#         return redirect(reverse("oidc_authentication_init") + f"?domain={domain}")
#         # return HttpResponse(f'email: {email}, domain: {domain}')

# class CustomOIDCAuthenticationRequestView(OIDCAuthenticationRequestView): 
#     def get(self, request, *args, **kwargs):
#         email = request.session.get("oidc_initial_email")
#         if not email or "@" not in email:
#             messages.error(request, "E-mail inválido ou ausente para autenticação federada.")
#             return HttpResponseRedirect(reverse("login"))

#         domain = email.split("@")[-1].lower()

#         from auth.oidc_client import get_oidc_endpoints
#         endpoints = get_oidc_endpoints(domain)
#         if not endpoints:
#             messages.error(request, f"Domínio '{domain}' não está federado.")
#             return HttpResponseRedirect(reverse("login"))

#         # Injetar dinamicamente todas as configurações esperadas
#         self.get_settings = lambda attr, *args: {
#             "OIDC_RP_CLIENT_ID": settings.OIDC_RP_CLIENT_ID,
#             "OIDC_RP_CLIENT_SECRET": settings.OIDC_RP_CLIENT_SECRET,
#             "OIDC_RP_SCOPES": settings.OIDC_RP_SCOPES,
#             "OIDC_OP_AUTHORIZATION_ENDPOINT": endpoints["authorization_endpoint"],
#             "OIDC_OP_TOKEN_ENDPOINT": endpoints["token_endpoint"],
#             "OIDC_OP_USER_ENDPOINT": endpoints["userinfo_endpoint"],
#             "OIDC_OP_JWKS_ENDPOINT": endpoints["jwks_uri"],
#         }.get(attr)

#         # Call the parent class's get method to ensure a valid HttpResponseRedirect is always returned
#         return super().get(request, *args, **kwargs)


# class CustomOIDCAuthenticationCallbackView(OIDCAuthenticationCallbackView):
#     def login_success(self):
#         user = self.request.user

#         # Validação defensiva: garante que é um usuário autenticado
#         if not user or not isinstance(user, get_user_model()):
#             return self.login_failure()

#         email = getattr(user, "email", None)
#         if email:
#             subsidiary = get_subsidiary_by_email(email)
#             profile, _ = Profile.objects.get_or_create(user=user)

#             if subsidiary and profile.subsidiary != subsidiary:
#                 profile.subsidiary = subsidiary
#                 profile.save()

#         login(self.request, user)

#         next_url = self.request.session.pop("next", None) or self.request.GET.get("next") or reverse("home")
#         return HttpResponseRedirect(next_url)

#     def login_failure(self):
#         return HttpResponseRedirect(reverse("login") + "?error=oidc_failure")

# ! rever a necessidade deste método no futuro quando for usar o OIDC
def user_login(request):
    """ 
     View para autenticação local (e-mail e senha).
     Esta view é usada para autenticação local, mas também pode ser o ponto de partida para autenticação federada.
     Ela valida o e-mail, verifica o domínio e autentica o usuário.
    """
    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        if "@" not in email:
            messages.error(request, "E-mail inválido.")
            return render(request, 'users_app/login.html')

        # domain = email.split("@")[-1].lower()

        # trusted_domains = get_trusted_domains()
        # if domain not in trusted_domains:
        #     messages.error(request, f"Domínio '{domain}' não está autorizado para autenticação federada.")
        #     return render(request, 'users_app/login.html')

        email = request.POST["email"]
        password = request.POST["password"]

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            print(f"User {user.email} logged in successfully.")
            return redirect('norm_proc_app:home')
        else:
            messages.error(request, "Credenciais inválidas.")
            return render(request, 'users_app/login.html')
    return render(request, 'users_app/login.html')


def register_success(request):
    return render(request, 'users_app/register_success.html')
