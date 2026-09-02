# users_app/models.py
from django.db import models

# Create your models here.
from uuid6 import uuid7

from django.db import models
# from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings

from utils.identifiers import generate_sequential_uuid


class Department(models.Model):
    """
    Modelo para departamentos
    Representa um departamento dentro da organização.
    Cada departamento pode ser responsável por normas e procedimentos específicos.
    Fields:
        - name: Nome do departamento.
        - acronym: Sigla do departamento.
    """

    name = models.CharField(max_length=100)
    acronym = models.CharField(max_length=10)

    def __str__(self):
        return self.acronym
    
    class Meta:
        verbose_name_plural = 'Departamentos'

class CustomUserManager(BaseUserManager):
    """
    Essa classe define como criar usuários e superusuários
    Ela foi criada para suportar o modelo de usuário customizado (CustomUser) que usa e-mail como identificador.
    create_user:
        - Recebe email, password e outros campos opcionais.
        - Valida se o e-mail foi fornecido.
        - Normaliza o e-mail (normalize_email converte para minúsculas e remove espaços).
        - Cria uma instância do modelo (self.model(...)).
        - Define a senha com set_password (usa hash seguro).
        - Salva no banco com save(using=self._db).
    create_superuser:
        - Define is_staff e is_superuser como True.
        - Chama create_user com esses campos extras.
    """

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("O campo email é obrigatório")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Essa é a definição do modelo de usuário.
    campos:
        - email: campo obrigatório e único.
        - username: nome de utilizador único.
        - first_name: primeiro nome do utilizador.
        - last_name: apelido do utilizador.
        - is_active: controla se o usuário está ativo.
        - is_staff: permite acesso ao admin.
    Configurações especiais:
        - USERNAME_FIELD: define que o campo email será usado para login.
        - REQUIRED_FIELDS: campos obrigatórios ao criar superusuário via CLI (vazio aqui).
    Gerenciador:
        - Define que o modelo usará o gerenciador customizado para criar usuários.
    Representação:
        def __str__(self):
            return self.email
        - Retorna o e-mail como representação textual do usuário.
    Conexão com o sistema:
        Para que esse modelo funcione, é preciso configurar no settings.py:
            AUTH_USER_MODEL = 'yourapp.CustomUser'
        Isso informa ao Django que o modelo de usuário padrão foi substituído.
    """
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    # Gerenciador customizado, responsável por criar usuários e superusuários
    objects = CustomUserManager() 

    def __str__(self):
        return self.email
    
    class Meta:
        verbose_name_plural = "Usuários (Modelo customizado)"

class Subsidiary(models.Model):
    """
    Modelo para filiais
    Representa uma filial ou unidade de negócio dentro da organização.
    Cada filial pode ter seus próprios departamentos e usuários.
    Fields:
        - id: Identificador único da filial.
        - name: Nome da filial.
        - domain: Domínio de e-mail associado à filial (para verificação de e-mails).
        - acronym: Sigla da filial.
    """
    id = models.UUIDField(primary_key=True, default=generate_sequential_uuid, editable=False)
    name = models.CharField(max_length=100, verbose_name='Nome')
    domain = models.CharField(max_length=100, unique=True, verbose_name='Domínio')  # Ex: "subsidiaria1.com"
    acronym = models.CharField(max_length=10, verbose_name='Acrónimo')

    def __str__(self):
        return self.acronym
    
    class Meta:
        verbose_name_plural = 'subsidiárias'

class Profile(models.Model):
    """
    Modelo de perfil do usuário. Contém informações adicionais sobre o usuário.
    Cada usuário tem um perfil associado.
    Fields:
        - id: Identificador único do perfil.
        - user: Referência ao usuário (OneToOne).
        - subsidiary: Filial à qual o usuário pertence.
        - department: Departamento do usuário.
        - role: Papel do usuário (leitor, editor, revisor, aprovador, administrador).
        - timezone: Fuso horário do usuário.
        - locale: Localidade do usuário (idioma preferido).
        Obs: O campo locale no model Profile serve para indicar a preferência de idioma ou localização cultural do usuário — e pode ser extremamente útil em aplicações corporativas multilíngues.
        Ele permite que a interface do usuário, mensagens e outros conteúdos sejam apresentados no idioma preferido do usuário, melhorando a experiência do usuário.
        Isso é especialmente importante em ambientes corporativos onde os usuários podem vir de diferentes regiões geográficas e culturais.
        - Pode ser usado com frameworks como django.middleware.locale.LocaleMiddleware para carregar traduções automaticamente.
        - Pode ser usado para formatar datas, números e moedas de acordo com as convenções locais do usuário.
        - Pode ser útil para segmentação de usuários e personalização de conteúdo com base na localização geográfica ou preferências culturais.
    """

    id = models.UUIDField(primary_key=True, default=generate_sequential_uuid, editable=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    subsidiary = models.ForeignKey(Subsidiary, on_delete=models.PROTECT)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    role = models.CharField(max_length=50, choices=[
        ('reader', 'Reader'),
        ('editor', 'Editor'),
        ('reviewer', 'Reviewer'),
        ('approver', 'Approver'),
        ('admin', 'Administrator'),
    ])
    timezone = models.CharField(max_length=50, default='UTC')
    locale = models.CharField(max_length=10, default='en') # Ex: 'en', 'pt', 'fr'

    def __str__(self):
        return f"{self.user.username} @ {self.subsidiary.acronym}"
    
    class Meta:
        verbose_name_plural = 'Perfis'

class AcceptedDomain(models.Model):
    """
    Modelo para domínios aceitos
    Representa um domínio de e-mail aceito para registro de usuários.
    Cada domínio está associado a uma filial específica.
    Fields:
        - id: Identificador único do domínio.
        - domain: Domínio de e-mail (ex: "subsidiaria1.com").
        - subsidiary: Filial associada ao domínio.
        - is_active: Indica se o domínio está ativo para registro.
        - created_at: Data e hora de criação do registro.
    """

    id = models.UUIDField(primary_key=True, default=generate_sequential_uuid, editable=False)
    domain = models.CharField(max_length=100, unique=True)  # Ex: "subsidiaria1.com"
    subsidiary = models.ForeignKey(Subsidiary, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    is_sso_enabled = models.BooleanField(default=False)
    discovery_host = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.domain} ({self.subsidiary.acronym})"

    class Meta:
        verbose_name_plural = 'Domínios aceites'
