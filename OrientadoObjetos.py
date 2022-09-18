class CuentaBancaria:

    def __init__(self, num_cuenta, nombre_titular, balance):
        self.num_cuenta = num_cuenta
        self.nombre_titular = nombre_titular
        self.balance = balance

        def generar_balance(self):
            print(self.balance)

        def depositar(self, monto):
            if monto > 0:
                self.balance +=monto

#instancia -> Se asume que self ya tiene un valor
mi_cuenta = CuentaBancaria ("105-356-643", "Nora Smith", 5600)
mi_cuenta.balance()
