from django.test import TestCase
from django.contrib.auth import get_user_model

Usuario = get_user_model()


class UsuarioModelTest(TestCase):
    """Testes para o modelo Usuario"""

    def test_create_usuario(self):
        """Teste de criação de um usuário"""
        usuario = Usuario.objects.create_user(
            username='joao_silva',
            email='teste@example.com',
            password='senha123'
        )
        self.assertEqual(usuario.email, 'teste@example.com')
        self.assertEqual(usuario.username, 'joao_silva')
        self.assertTrue(usuario.check_password('senha123'))

    def test_usuario_str(self):
        """Teste da representação em string do usuário"""
        usuario = Usuario.objects.create_user(
            username='joao_silva',
            email='teste@example.com',
            password='senha123'
        )
        self.assertEqual(str(usuario), 'joao_silva')

    def test_usuario_is_active_por_padrao(self):
        """Teste se usuário é ativo por padrão"""
        usuario = Usuario.objects.create_user(
            username='joao_silva',
            email='teste@example.com',
            password='senha123'
        )
        self.assertTrue(usuario.is_active)

    def test_usuario_nao_e_staff_por_padrao(self):
        """Teste se usuário não é staff por padrão"""
        usuario = Usuario.objects.create_user(
            username='joao_silva',
            email='teste@example.com',
            password='senha123'
        )
        self.assertFalse(usuario.is_staff)

    def test_criar_superuser(self):
        """Teste de criação de um superuser"""
        admin = Usuario.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='senha123'
        )
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)

    def test_usuario_campos_timestamp(self):
        """Teste se os campos de timestamp são criados automaticamente"""
        usuario = Usuario.objects.create_user(
            username='joao_silva',
            email='teste@example.com',
            password='senha123'
        )
        self.assertIsNotNone(usuario.created_at)
        self.assertIsNotNone(usuario.updated_at)

    def test_usuario_email_unico(self):
        """Teste se o email deve ser único"""
        Usuario.objects.create_user(
            username='joao1',
            email='teste@example.com',
            password='senha123'
        )
        usuario2 = Usuario.objects.create_user(
            username='joao2',
            email='teste2@example.com',
            password='senha123'
        )
        self.assertNotEqual(usuario2.email, 'teste@example.com')

    def test_usuario_update_updated_at(self):
        """Teste se updated_at é atualizado ao modificar usuário"""
        usuario = Usuario.objects.create_user(
            username='joao_silva',
            email='teste@example.com',
            password='senha123'
        )
        created_at = usuario.created_at
        usuario.first_name = 'João'
        usuario.save()
        self.assertEqual(usuario.created_at, created_at)
