# norm_proc_app/models.py
from django.db import models
from django.conf import settings
from utils.identifiers import generate_sequential_uuid
from users_app.models import Department

class BaseDocument(models.Model):
    id = models.UUIDField(primary_key=True, default=generate_sequential_uuid, editable=False)
    # Título do documento, não pode ser nulo ou em branco
    title = models.CharField(max_length=255)
    # Descrição do documento, pode ser nula ou em branco
    Description = models.TextField(blank=True, verbose_name="Descrição")  
    # Status do documento, pode ser "vigente", "expirado" ou "revogado"
    status = models.CharField(max_length=50, choices=[
        ('vigente', 'Vigente'),
        ('revogado', 'Revogado'),
    ], default='vigente')
    # Arquivo do documento, pode ser nulo ou em branco, será armazenado na pasta 'documents/'
    file = models.FileField(upload_to='documents/', default='documents/default.pdf')
    Classification_level = models.CharField(max_length=50, verbose_name="Nível de classificação", choices=[
        ('publico', 'Público'),
        ('interno', 'Interno'),
        ('confidencial', 'Confidencial'),
        ('restrito', 'Restrito'),
    ], default='interno')
    created_at = models.DateTimeField(auto_now_add=True)
    published_at = models.DateTimeField(null=True, blank=True) # todo: Considerar se é necessário ter um campo de data de publicação
    revoked_at = models.DateTimeField(null=True, blank=True)
    current_version = models.CharField(max_length=10, default="1.0")
    author = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name="%(class)s_authored_documents") # Gabinete proveniente do documento
    drafted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="%(class)s_drafted_documents") # Quem redigiu o documento
    reviewed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True, related_name="%(class)s_reviewed_documents") #Quem revisou o documento
    next_review_date = models.DateField(null=True, blank=True, verbose_name="Próxima revisão") # data da próxima revisão do documento
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True, related_name="%(class)s_approved_documents") # autoridade que aprovou o documento
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="versions") # Permite criar uma relação de versão entre documentos
    document_owner = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name="%(class)s_owned_documents") # Departamento proprietário do documento
    document_type = models.CharField(max_length=50, choices=[
        ('norm', 'Norma'),
        ('procedure', 'Procedimento'),
        ('policy', 'Política'),
        ('regulation', 'Regulamento'),
        ('manual', 'Manual'),
        ('guide', 'Guia'),
        ('sop', ' Standard Operating Procedure'),
    ], default='norm', verbose_name="Tipo de documento")
    code = models.CharField(max_length=100, unique=True, blank=True, null=True, verbose_name="Código do documento") # Código único do documento, pode ser gerado automaticamente ou definido manualmente
    Recipient = models.ForeignKey(Department, verbose_name="Destinatário", on_delete=models.CASCADE) # Destinatário do documento, pode ser nulo ou em branco

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
            Description=self.Description,
            file=self.file,
            current_version=new_version,
            author=author,
            parent=self,
            status="draft"
        )
