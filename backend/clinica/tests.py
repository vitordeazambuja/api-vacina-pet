from django.test import TestCase
from django.contrib.auth import get_user_model
from clinica.models import Pet, Vacina, PetVacina
from usuarios.models import PerfilDono, PerfilFuncionario
from datetime import datetime, timedelta

Usuario = get_user_model()


class PetModelTest(TestCase):
    """Testes para o modelo Pet"""

    def setUp(self):
        """Configuração inicial para cada teste"""
        self.usuario = Usuario.objects.create_user(
            username='dono',
            email='dono@example.com',
            password='senha123'
        )
        
        self.perfil_dono = PerfilDono.objects.create(
            usuario=self.usuario,
            nome='João Silva',
            cpf='12345678901',
            endereco='Rua A, 123',
            telefone='11999999999'
        )

    def test_create_pet(self):
        """Teste de criação de um pet"""
        pet = Pet.objects.create(
            nome='Fluffy',
            especie='Gato',
            raca='Siames',
            peso=4.5,
            data_nascimento='2020-01-01',
            dono=self.perfil_dono
        )
        self.assertEqual(pet.nome, 'Fluffy')
        self.assertEqual(pet.especie, 'Gato')
        self.assertEqual(pet.dono, self.perfil_dono)

    def test_pet_str(self):
        """Teste da representação em string do pet"""
        pet = Pet.objects.create(
            nome='Fluffy',
            especie='Gato',
            raca='Siames',
            peso=4.5,
            data_nascimento='2020-01-01',
            dono=self.perfil_dono
        )
        self.assertIn('Fluffy', str(pet))

    def test_pet_campos_timestamp(self):
        """Teste se os campos de timestamp são criados automaticamente"""
        pet = Pet.objects.create(
            nome='Fluffy',
            especie='Gato',
            raca='Siames',
            peso=4.5,
            data_nascimento='2020-01-01',
            dono=self.perfil_dono
        )
        self.assertIsNotNone(pet.created_at)
        self.assertIsNotNone(pet.updated_at)

    def test_multiplos_pets_mesmo_dono(self):
        """Teste se um dono pode ter múltiplos pets"""
        pet1 = Pet.objects.create(
            nome='Fluffy',
            especie='Gato',
            raca='Siames',
            peso=4.5,
            data_nascimento='2020-01-01',
            dono=self.perfil_dono
        )
        pet2 = Pet.objects.create(
            nome='Rex',
            especie='Cachorro',
            raca='Pastor Alemão',
            peso=30.0,
            data_nascimento='2019-06-15',
            dono=self.perfil_dono
        )

        pets_do_dono = Pet.objects.filter(dono=self.perfil_dono)
        self.assertEqual(pets_do_dono.count(), 2)

    def test_pet_pertence_ao_dono(self):
        """Teste se um pet pertence ao dono correto"""
        outro_usuario = Usuario.objects.create_user(
            username='outro_dono',
            email='outro@example.com',
            password='senha123'
        )

        outro_perfil_dono = PerfilDono.objects.create(
            usuario=outro_usuario,
            nome='Maria Silva',
            cpf='98765432101',
            endereco='Rua B, 456',
            telefone='11888888888'
        )

        pet = Pet.objects.create(
            nome='Fluffy',
            especie='Gato',
            raca='Siames',
            peso=4.5,
            data_nascimento='2020-01-01',
            dono=self.perfil_dono
        )

        self.assertEqual(pet.dono, self.perfil_dono)
        self.assertNotEqual(pet.dono, outro_perfil_dono)

    def test_calcular_idade_dias(self):
        """Teste do cálculo de idade em dias"""
        pet = Pet.objects.create(
            nome='Fluffy',
            especie='Gato',
            raca='Siames',
            peso=4.5,
            data_nascimento=datetime.now().date() - timedelta(days=100),
            dono=self.perfil_dono
        )
        idade_dias = pet.calcular_idade_dias()
        self.assertEqual(idade_dias, 100)


class VacinaModelTest(TestCase):
    """Testes para o modelo Vacina"""

    def test_create_vacina(self):
        """Teste de criação de uma vacina"""
        vacina = Vacina.objects.create(
            nome='Raiva',
            fabricante='Laboratório X',
            valor=50.00,
            intervalo_doses_dias=365,
            descricao='Vacina contra raiva'
        )
        self.assertEqual(vacina.nome, 'Raiva')
        self.assertEqual(vacina.fabricante, 'Laboratório X')

    def test_vacina_str(self):
        """Teste da representação em string da vacina"""
        vacina = Vacina.objects.create(
            nome='Raiva',
            fabricante='Laboratório X',
            valor=50.00,
            intervalo_doses_dias=365,
            descricao='Vacina contra raiva'
        )
        self.assertEqual(str(vacina), 'Raiva')

    def test_multiplas_vacinas(self):
        """Teste se diferentes tipos de vacina podem ser criados"""
        vacina_raiva = Vacina.objects.create(
            nome='Raiva',
            fabricante='Laboratório X',
            valor=50.00,
            intervalo_doses_dias=365,
            descricao='Vacina contra raiva'
        )
        vacina_polivalente = Vacina.objects.create(
            nome='V-4',
            fabricante='Laboratório Y',
            valor=80.00,
            intervalo_doses_dias=365,
            descricao='Vacina polivalente'
        )

        self.assertEqual(vacina_raiva.nome, 'Raiva')
        self.assertEqual(vacina_polivalente.nome, 'V-4')

    def test_vacina_campos_timestamp(self):
        """Teste se os campos de timestamp são criados automaticamente"""
        vacina = Vacina.objects.create(
            nome='Raiva',
            fabricante='Laboratório X',
            valor=50.00,
            intervalo_doses_dias=365,
            descricao='Vacina contra raiva'
        )
        self.assertIsNotNone(vacina.created_at)
        self.assertIsNotNone(vacina.updated_at)


class PetVacinaModelTest(TestCase):
    """Testes para o modelo PetVacina"""

    def setUp(self):
        """Configuração inicial para cada teste"""
        self.usuario_dono = Usuario.objects.create_user(
            username='dono',
            email='dono@example.com',
            password='senha123'
        )

        self.perfil_dono = PerfilDono.objects.create(
            usuario=self.usuario_dono,
            nome='João Silva',
            cpf='12345678901',
            endereco='Rua A, 123',
            telefone='11999999999'
        )

        self.usuario_vet = Usuario.objects.create_user(
            username='vet',
            email='vet@example.com',
            password='senha123'
        )

        self.perfil_vet = PerfilFuncionario.objects.create(
            usuario=self.usuario_vet,
            nome='Dr. Silva',
            cpf='11111111111',
            endereco='Rua Clínica, 100',
            telefone='11987654321',
            cargo='Veterinário'
        )

        self.pet = Pet.objects.create(
            nome='Fluffy',
            especie='Gato',
            raca='Siames',
            peso=4.5,
            data_nascimento='2020-01-01',
            dono=self.perfil_dono
        )

        self.vacina = Vacina.objects.create(
            nome='Raiva',
            fabricante='Laboratório X',
            valor=50.00,
            intervalo_doses_dias=365,
            descricao='Vacina contra raiva'
        )

    def test_registrar_vacinacao(self):
        """Teste de registro de vacinação"""
        hoje = datetime.now().date()

        pet_vacina = PetVacina.objects.create(
            pet=self.pet,
            vacina=self.vacina,
            aplicador=self.perfil_vet,
            data_aplicacao=hoje,
            lote='LOTE123'
        )

        self.assertEqual(pet_vacina.pet, self.pet)
        self.assertEqual(pet_vacina.vacina, self.vacina)
        self.assertEqual(pet_vacina.data_aplicacao, hoje)
        self.assertEqual(pet_vacina.aplicador, self.perfil_vet)

    def test_proxima_dose_calculada_automaticamente(self):
        """Teste se próxima dose é calculada automaticamente"""
        hoje = datetime.now().date()

        pet_vacina = PetVacina.objects.create(
            pet=self.pet,
            vacina=self.vacina,
            aplicador=self.perfil_vet,
            data_aplicacao=hoje,
            lote='LOTE123'
        )

        data_esperada = hoje + timedelta(days=self.vacina.intervalo_doses_dias)
        self.assertEqual(pet_vacina.proxima_dose, data_esperada)

    def test_multiplas_vacinacoes_mesmo_pet(self):
        """Teste se um pet pode ter múltiplas vacinações"""
        vacina2 = Vacina.objects.create(
            nome='V-4',
            fabricante='Laboratório Y',
            valor=80.00,
            intervalo_doses_dias=365,
            descricao='Vacina polivalente'
        )

        hoje = datetime.now().date()

        pet_vacina1 = PetVacina.objects.create(
            pet=self.pet,
            vacina=self.vacina,
            aplicador=self.perfil_vet,
            data_aplicacao=hoje,
            lote='LOTE123'
        )

        pet_vacina2 = PetVacina.objects.create(
            pet=self.pet,
            vacina=vacina2,
            aplicador=self.perfil_vet,
            data_aplicacao=hoje,
            lote='LOTE456'
        )

        vacinacoes_do_pet = PetVacina.objects.filter(pet=self.pet)
        self.assertEqual(vacinacoes_do_pet.count(), 2)

    def test_pet_vacina_campos_timestamp(self):
        """Teste se os campos de timestamp são criados automaticamente"""
        hoje = datetime.now().date()

        pet_vacina = PetVacina.objects.create(
            pet=self.pet,
            vacina=self.vacina,
            aplicador=self.perfil_vet,
            data_aplicacao=hoje,
            lote='LOTE123'
        )

        self.assertIsNotNone(pet_vacina.created_at)
        self.assertIsNotNone(pet_vacina.updated_at)
