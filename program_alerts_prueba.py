from datetime import datetime
import unittest

'''Ejercicio 1) Consigna:
1)Se pueden registrar usuarios que recibirán alertas. 
2)Se pueden registrar temas sobre los cuales se enviarán alertas.
3)Los usuarios pueden optar sobre cuales temas quieren recibir alertas.
4)Se puede enviar una alerta sobre un tema y lo reciben todos los usuarios que han optado recibir alertas de ese tema.
5)Se puede enviar una alerta sobre un tema a un usuario específico, solo lo recibe ese único usuario.
6)Una alerta puede tener una fecha y hora de expiración. 
7)Hay dos tipos de alertas: Informativas y Urgentes.
8)Un usuario puede marcar una alerta como leída.
9)Se pueden obtener todas las alertas no expiradas de un usuario que aún no ha leído. 
10)Se pueden obtener todas las alertas no expiradas para un tema. Se informa para cada alerta si es para todos los usuarios o para uno específico.
11)Tanto para el punto 9 como el 10, el ordenamiento de las alertas es el siguiente: las Urgentes van al inicio, siendo la última en llegar la primera en obtenerse (LIFO).
Y a continuación las informativas, siendo la primera en llegar la primera en obtenerse (FIFO). Ej: Dadas las siguientes alertas Informativas y Urgentes que llegan en el siguiente orden: I1,I2,U1,I3,U2,I4 se ordenarán de la siguiente forma --> 
'''

class Usuario:
    def __init__(self, nombre):
        self.nombre = nombre
        self.temas = set()
        self.alertas_no_leidas = []

    def agregar_tema(self, tema): 
        self.temas.add(tema)

    def recibir_alerta(self, alerta):
        if self in alerta.destinatarios:
            self.alertas_no_leidas.append(alerta)

    def marcar_alerta_como_leida(self, alerta):
        alerta.leida = True

    def obtener_alertas_no_leidas(self):
        alertas_urgentes = [alerta for alerta in self.alertas_no_leidas if isinstance(alerta, AlertaUrgente) and not alerta.leida]
        alertas_informativas = [alerta for alerta in self.alertas_no_leidas if isinstance(alerta, AlertaInformativa) and not alerta.leida]

        alertas_urgentes.sort(key=lambda x: x.fecha_creacion, reverse=True)
        alertas_informativas.sort(key=lambda x: x.fecha_creacion)

        return alertas_urgentes + alertas_informativas
    
    def recibir_alerta_especifica(self, alerta):
        if self == alerta.destinatarios[0]:
            self.alertas_no_leidas.append(alerta)

class Tema:
    def __init__(self, nombre):
        self.nombre = nombre
        self.usuarios = set()

    def enviar_alerta_a_todos(self, alerta, fecha_expiracion=None):
        for usuario in self.usuarios:
            alerta = AlertaUrgente(self, [usuario], fecha_expiracion)
            usuario.recibir_alerta(alerta)

    def obtener_alertas_no_expiradas(self):
        alertas = []
        for usuario in self.usuarios:
            for alerta in usuario.alertas_no_leidas:
                if alerta.tema == self and not alerta.expirada():
                    destinatario = "Todos los usuarios" if len(alerta.destinatarios) > 1 else f"Usuario: {alerta.destinatarios[0].nombre}"
                    alertas.append(f"Alerta para {destinatario}: Tipo {alerta.tipo}, Expira en {alerta.fecha_expiracion}")
        return alertas

class Alerta:
    def __init__(self, tema, destinatarios, fecha_expiracion=None):
        self.tema = tema
        self.destinatarios = destinatarios
        self.fecha_expiracion = fecha_expiracion
        self.leida = False
        self.fecha_creacion = datetime.now()

    def marcar_como_leida(self):
        self.leida = True

    def expirada(self):
        return self.fecha_expiracion and datetime.now() > self.fecha_expiracion

class AlertaInformativa(Alerta):
    def __init__(self, tema, destinatario, fecha_expiracion=None):
        super().__init__(tema, destinatario, fecha_expiracion)
        self.tipo = "Informativa"

class AlertaUrgente(Alerta):
    def __init__(self, tema, destinatario, fecha_expiracion=None):
        super().__init__(tema, destinatario, fecha_expiracion)
        self.tipo = "Urgente"
        
    def enviar_alerta_a_usuario(self, usuario, fecha_expiracion=None):
        alerta = AlertaUrgente(self.tema, [usuario], fecha_expiracion)
        usuario.recibir_alerta_especifica(alerta)

            

# Test unitario

class TestSistemaAlertas(unittest.TestCase):
    def test_alertas_no_leidas(self):
        usuario = Usuario("Miusuario1")
        tema = Tema("Tema musical")
        alerta_urgente = AlertaUrgente(tema, [usuario])
        alerta_informativa = AlertaInformativa(tema, [usuario])

        tema.enviar_alerta_a_todos(alerta_urgente)
        tema.obtener_alertas_no_expiradas()

        usuario.recibir_alerta(alerta_urgente)
        usuario.recibir_alerta(alerta_informativa)
        usuario.marcar_alerta_como_leida(alerta_urgente)

        alertas_no_leidas = usuario.obtener_alertas_no_leidas()
        self.assertEqual(len(alertas_no_leidas), 1)
        self.assertEqual(alertas_no_leidas[0], alerta_informativa)

        alertas_no_expiradas = tema.obtener_alertas_no_expiradas()

         

if __name__ == '__main__':
    unittest.main()
