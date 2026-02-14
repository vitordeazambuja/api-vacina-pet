from django.contrib import admin
from .models import Pet, Vacina, PetVacina

@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'especie', 'raca', 'dono', 'peso', 'created_at')
    list_filter = ('especie', 'created_at')
    search_fields = ('nome', 'dono__nome', 'raca')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)

@admin.register(Vacina)
class VacinaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'fabricante', 'valor', 'intervalo_doses_dias', 'created_at')
    list_filter = ('fabricante', 'created_at')
    search_fields = ('nome', 'fabricante')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)

@admin.register(PetVacina)
class PetVacinaAdmin(admin.ModelAdmin):
    list_display = ('id', 'pet', 'vacina', 'aplicador', 'data_aplicacao', 'proxima_dose', 'get_status_display', 'created_at')
    list_filter = ('data_aplicacao', 'proxima_dose', 'created_at')
    search_fields = ('pet__nome', 'vacina__nome', 'aplicador__nome', 'lote')
    readonly_fields = ('created_at', 'updated_at', 'get_status_display', 'get_esta_vencida_display')
    ordering = ('-created_at',)
    fieldsets = (
        ('Informações Principais', {
            'fields': ('pet', 'vacina', 'aplicador', 'data_aplicacao')
        }),
        ('Detalhes da Dose', {
            'fields': ('proxima_dose', 'lote', 'observacoes')
        }),
        ('Status', {
            'fields': ('get_status_display', 'get_esta_vencida_display')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_status_display(self, obj):
        """Exibe o status da vacinação (em_dia, proxima_em_breve, vencida, indefinido)"""
        return obj.get_status()
    get_status_display.short_description = "Status"
    
    def get_esta_vencida_display(self, obj):
        """Exibe se a vacinação está vencida"""
        return obj.esta_vencida()
    get_esta_vencida_display.short_description = "Está Vencida?"
