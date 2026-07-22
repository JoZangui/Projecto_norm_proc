# norm_proc_app/models.py
from django.db import models
from django.conf import settings
from utils.identifiers import generate_sequential_uuid
from users_app.models import Department

class BaseDocument(models.Model):
    id = models.UUIDField(primary_key=True, default=generate_sequential_uuid, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=50, choices=[
        ('rascunho', 'Rascunho'),
        ('em_analise', 'Em análise'),
        ('aprovado', 'Aprovado'),
        ('revogado', 'Revogado'),
    ], default='draft')
    file = models.FileField(upload_to='documents/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    published_at = models.DateTimeField(null=True, blank=True)
    revoked_at = models.DateTimeField(null=True, blank=True)
    current_version = models.CharField(max_length=10, default="1.0")  # agora string tipo "1.0"
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="versions")

    class Meta:
        abstract = True

    def create_new_version(self, author, major=False):
        """
        Cria uma nova versão do documento.
        Se major=True → incrementa versão principal (ex.: 1.0 → 2.0).
        Caso contrário → incrementa versão menor (ex.: 1.0 → 1.1).
        """
        major_v, minor_v = map(int, self.current_version.split("."))
        if major:
            major_v += 1
            minor_v = 0
        else:
            minor_v += 1
        new_version = f"{major_v}.{minor_v}"

        return self.__class__.objects.create(
            title=self.title,
            description=self.description,
            file=self.file,
            current_version=new_version,
            author=author,
            parent=self,
            status="rascunho"
        )

class Norms(BaseDocument):
    legal_basis = models.TextField(blank=True)
    document_type = models.CharField(max_length=100, choices=[
        ('politica', 'Política'),
        ('regulamento', 'Regulamento'),
        ('norma_tecnica', 'Norma técnica'),
    ])
    # O campo "responsible_department" indica qual departamento é responsável pela criação, manutenção e atualização da norma.
    # Exemplo:
        # Departamento Jurídico → responsável por normas legais e regulamentos.
        # Departamento de Qualidade → responsável por normas ISO ou padrões internos.
        # Esse campo mostra quem tem autoridade sobre o documento e quem deve ser consultado em caso de dúvidas ou revisões.
    responsible_department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Norma: {self.title} (v{self.current_version})"

    class Meta(BaseDocument.Meta):
        verbose_name_plural = 'Normas'

class Procedures(BaseDocument):
    steps = models.JSONField(default=list)
    estimated_duration = models.DurationField(null=True, blank=True)
    criticality = models.CharField(max_length=50, choices=[
        ('baixo', 'Baixo'),
        ('medio', 'Médio'),
        ('alto', 'Alto'),
    ])
    # O campo "operational_department" Indica quem executa na prática o procedimento operacional.
    # Exemplo:
        # Departamento de TI → responsável por procedimentos de backup.
        # Departamento de RH → responsável por procedimentos de onboarding de funcionários.
        # Esse campo mostra quem aplica a norma no dia a dia, garantindo que a execução esteja alinhada com a norma correspondente.
    operational_department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Procedimento: {self.title} (v{self.current_version})"

    class Meta(BaseDocument.Meta):
        verbose_name_plural = "Procedimentos"
