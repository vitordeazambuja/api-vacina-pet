from django.contrib import admin
from .models import Usuario, PerfilDono, PerfilFuncionario

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'is_staff', 'created_at')
    list_filter = ('is_staff', 'is_superuser', 'created_at')
    search_fields = ('username', 'email')
    ordering = ('-created_at',)

@admin.register(PerfilDono)
class PerfilDonoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'usuario', 'cpf', 'telefone', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('nome', 'cpf', 'usuario__username')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)

@admin.register(PerfilFuncionario)
class PerfilFuncionarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'usuario', 'cargo', 'cpf', 'created_at')
    list_filter = ('cargo', 'created_at')
    search_fields = ('nome', 'cpf', 'cargo', 'usuario__username')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)
