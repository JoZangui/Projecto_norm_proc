# norm_proc_app/models.py
from django.db import models
from django.conf import settings
from utils.identifiers import generate_sequential_uuid
from users_app.models import Department

class BaseDocument(models.Model):
    id = models.UUIDField(primary_key=True, default=generate_sequential_uuid, editable=False)
    title = models.CharField(max_length=255)
    # TipTap guarda o conteúdo como JSON estruturado
    content = models.JSONField(default=dict, blank=True)  
    status = models.CharField(max_length=50, choices=[
        ('draft', 'Draft'),
        ('under_review', 'Under Review'),
        ('approved', 'Approved'),
        ('pending_approval', 'Pending approval'),
        ('revoked', 'Revoked'),
    ], default='draft')
    file = models.FileField(upload_to='documents/', null=True, blank=True)
    Classification_level = models.CharField(max_length=50, verbose_name="Nível de classificação", choices=[
        ('public', 'Public'),
        ('internal', 'Internal'),
        ('confidential', 'Confidential'),
    ], default='internal')
    created_at = models.DateTimeField(auto_now_add=True)
    published_at = models.DateTimeField(null=True, blank=True)
    revoked_at = models.DateTimeField(null=True, blank=True)
    current_version = models.CharField(max_length=10, default="1.0")
    author = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name="%(class)s_authored_documents")
    drafted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="%(class)s_drafted_documents")
    reviewed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True, related_name="%(class)s_reviewed_documents")
    next_review_date = models.DateField(null=True, blank=True, verbose_name="Próxima revisão")
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True, related_name="%(class)s_approved_documents")
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="versions") # Permite criar uma relação de versão entre documentos
    document_owner = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name="%(class)s_owned_documents")
    code = models.CharField(max_length=100, unique=True, blank=True, null=True, verbose_name="Código do documento")

    class Meta:
        abstract = True

    def create_new_version(self, author, major=False):
        """
        Cria uma nova versão do documento.
        Att: Isto é apenas para quando for actualizar uma versão existente não quando for criar um novo documento
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
            content=self.content,  # copia o JSON do TipTap
            file=self.file,
            current_version=new_version,
            author=author,
            parent=self,
            status="draft"
        )

class Norms(BaseDocument):
    document_type = models.CharField(max_length=100, choices=[
        ('policy', 'Policy'),
        ('regulation', 'Regulation'),
        ('technical_standard', 'Technical Standard'),
    ])
    responsible_department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name="norms_responsible_documents")

    def __str__(self):
        return f"Norma: {self.title} (v{self.current_version})"

    class Meta(BaseDocument.Meta):
        verbose_name_plural = 'Normas'

class Procedures(BaseDocument):
    steps = models.JSONField(default=list)  # podes guardar steps como JSON do TipTap
    estimated_duration = models.DurationField(null=True, blank=True)
    criticality = models.CharField(max_length=50, choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ])
    operational_department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name="procedures_operational_documents")

    def __str__(self):
        return f"Procedimento: {self.title} (v{self.current_version})"

    class Meta(BaseDocument.Meta):
        verbose_name_plural = "Procedimentos"
