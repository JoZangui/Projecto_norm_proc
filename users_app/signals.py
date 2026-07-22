from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

from .models import Profile
from auth.utils import get_trusted_domains, get_subsidiary_by_email

User = get_user_model()

@receiver(post_save, sender=User)
def create_or_update_profile(sender, instance, created, **kwargs):
    """
    Cria ou atualiza o Profile associado ao User, 
    ligando-o à filial correta com base no domínio do e-mail.
    """

    # Normaliza e extrai domínio do e-mail
    email = (instance.email or "").strip().lower()
    if "@" not in email:
        return

    domain = email.split("@")[1]

    # Checa se o domínio está ativo em AcceptedDomain
    if domain not in get_trusted_domains():
        return

    # Obtém a filial pela regra de negócio
    # 1) Se o backend OIDC já setou instance.subsidiary, usa esse
    # 2) Senão, deriva via get_subsidiary_by_email
    subsidiary = getattr(instance, "subsidiary", None)
    if not subsidiary:
        subsidiary = get_subsidiary_by_email(email)

    # Criação inicial
    if created:
        Profile.objects.create(user=instance, subsidiary=subsidiary)
        return

    # Atualização subsequente: garante que Profile exista e esteja sincronizado
    try:
        profile = instance.profile
    except ObjectDoesNotExist:
        Profile.objects.create(user=instance, subsidiary=subsidiary)
    else:
        if profile.subsidiary != subsidiary:
            profile.subsidiary = subsidiary
            profile.save()
