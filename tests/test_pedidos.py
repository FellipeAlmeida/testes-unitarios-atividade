import unittest
from unittest.mock import Mock
from sistema_pedidos import Pedido, Estoque, EmailService

class TestPedidos(unittest.TestCase):

    def setUp(self):
        estoque = Estoque()
        email_service = EmailService()

        self.pedido = Pedido(estoque, email_service)
        self.pedido2 = Pedido(estoque, email_service)
        self.pedido3 = Pedido(estoque, email_service)
        self.pedido4 = Pedido(estoque, email_service)

        self.pedido.adicionar_item(1, 1) # 1 NOTEBOOK = 3000

        self.pedido2.adicionar_item(2, 1) # 1 MOUSE = 100

        self.pedido3.adicionar_item(2, 5) # 5 MOUSE = 500

        self.pedido4.adicionar_item(1, 3) # 3 MOUSE = 300

    # ---------------- TESTS CALCULAR SUBTOTAL ----------------

    def test_calcular_subtotal(self):
        result = self.pedido.calcular_subtotal()

        self.assertEqual(result, 3000)

    # ---------------- TESTS CALCULAR DESCONTO ----------------

    def test_calcular_desconto_com_cupom(self):
        result_com_desconto = self.pedido.calcular_desconto('DESCONTO10')

        self.assertEqual(result_com_desconto, 300) # <-- desconto 10%

    def test_calcular_desconto_cupom_inexistente(self):
        result_com_desconto_inexistente = self.pedido.calcular_desconto('DESCONTO20') # <-- a função apenas ignora cupons inexistentes
        
        self.assertEqual(result_com_desconto_inexistente, 150) # <-- desconto de 5% pelo valor do produto

    def test_calcular_desconto_abaixo_borda(self):
        result_abaixo_borda = self.pedido2.calcular_desconto()

        self.assertEqual(result_abaixo_borda, 0)

    def test_calcular_desconto_borda(self):
        result_borda = self.pedido3.calcular_desconto()

        self.assertEqual(result_borda, 25)

    # ---------------- TESTS CALCULAR FRETE ----------------

    def test_calcular_frete_acima_borda(self):
        result = self.pedido2.calcular_frete(31)

        self.assertEqual(result, 50)

    def test_calcular_frete_borda(self):
        result = self.pedido2.calcular_frete(30)

        self.assertEqual(result, 30)

    def test_calcular_frete_abaixo_borda(self):
        result = self.pedido2.calcular_frete(29)

        self.assertEqual(result, 30)

    def test_calcular_frete_acima_borda(self):
        result = self.pedido2.calcular_frete(11)

        self.assertEqual(result, 30)

    def test_calcular_frete_borda(self):
        result = self.pedido2.calcular_frete(10)
    
        self.assertEqual(result, 15)

    def test_calcular_frete_abaixo_borda(self):
        result = self.pedido2.calcular_frete(9)
    
        self.assertEqual(result, 15)

    def test_calcular_frete_subtotal_acima_borda(self):
        result = self.pedido3.calcular_frete(10)

        self.assertEqual(result, 0)

    def test_calcular_frete_subtotal_borda(self):
        result = self.pedido4.calcular_frete(10)

        self.assertEqual(result, 0)

    def test_calcular_frete_subtotal_abaixo_borda(self):
        result = self.pedido2.calcular_frete(5)

        self.assertEqual(result, 15)

    def test_calcular_frete_acima_borda(self):
        result = self.pedido2.calcular_frete(1)

        self.assertEqual(result, 15)

    def test_calcular_frete_borda(self):
        result = self.pedido2.calcular_frete(0)

        self.assertEqual(result, 15)

    def test_calcular_frete_abaixo_borda(self):
        with self.assertRaises(ValueError):
            self.pedido2.calcular_frete(-1)

    def test_calcular_frete_distancia_string(self):
        result = self.pedido.calcular_frete('abc') # <-- sistema não tem proteção contra tipagens inesperadas

        self.assertEqual(result, TypeError) 

    def test_calcular_frete_distancia_bool(self):
        result = self.pedido2.calcular_frete(True) # <-- considera distancia 0???
    
        self.assertEqual(result, 15) 

    def test_calcular_frete(self):
        result = self.pedido2.calcular_frete(31)

        self.assertEqual(result, 50)

    # ---------------- TESTS CALCULAR TOTAL ----------------

    def test_calcular_total(self):

        def calcular_subtotal_stub():
            return 100

        def calcular_desconto_stub(cupom):
            return 10

        def calcular_frete_stub(distancia):
            return 15

        self.pedido.calcular_desconto = calcular_desconto_stub
        self.pedido.calcular_frete = calcular_frete_stub
        self.pedido.calcular_subtotal = calcular_subtotal_stub

        result = self.pedido.calcular_total(31) # <-- o calculo dessa func ta errado

        self.assertEqual(result, 75) 

    # ---------------- TESTS CALCULAR TOTAL ----------------

    def test_finalizar(self):
        email_service = Mock()

        email_service.enviar.return_value = True
        
        result = self.pedido.finalizar(email_service, 15)

        self.assertEqual(result['status'], 'confirmado')
        
        email_service.finalizar.assert_called_once_with(email_service, 15)


if __name__ == "__main__":
    unittest.main()