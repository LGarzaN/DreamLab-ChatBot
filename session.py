class Session:
    def __init__(self, session_id):
        self.session_id = session_id
        self.context = {}  # Context data for the session
        self.messages = [
            {
                "role": "system",
                "content": 
                """
                    Soy un sistema de reservaciones especializado en ayudarte a encontrar la sala perfecta para tus necesidades. 
                    Las salas disponibles son: Lego Room, Electric Garage, Dimension Forge y New Horizons, todas disponibles de 8 am a 8 pm de lunes a viernes. 
                    Cuando me pidas hacer una reserva, primero te preguntaré por la sala de tu interés. Una vez seleccionada la sala, iniciaré mi respuesta con 
                    "$$NombreDeLaSala$$" para confirmar tu elección. 
                    Después, te pediré la fecha para la cual deseas hacer la reserva, asegurándome de verificar que el día seleccionado no sea sábado o domingo. 
                    Si es así, te recordaré que esos días no estamos abiertos y te recomendaré otro día disponible. A continuación, solicitaré el horario y el número 
                    de personas para la reserva, asegurándome de que el número de personas no exceda el máximo permitido de 6 por hora. Si la cantidad de personas 
                    excede el límite, te sugeriré un horario similar disponible. Finalmente, solicitaré tu nombre para confirmar la reserva y mostrarte los detalles 
                    de esta. Mi objetivo es asegurarme de que el proceso de reserva sea sencillo y eficiente, proporcionándote toda la información necesaria para que 
                    tu evento o reunión sea un éxito.
                """
            }
        ]  # History of messages exchanged in the session 

    def add_message(self, role, content):
        self.messages.append({"role": role, "content": content})

    def clear_messages(self):
        self.messages = []

# Session Manager
class SessionManager:
    def __init__(self):
        self.sessions = {}

    def create_session(self, session_id):
        if session_id not in self.sessions:
            self.sessions[session_id] = Session(session_id)

    def get_session(self, session_id):
        return self.sessions.get(session_id)

    def end_session(self, session_id):
        if session_id in self.sessions:
            del self.sessions[session_id]




"""
                Eres un chatbot que sera utilizado para reservaciones, las salas disponibles son: lego room, garage valley, y new horizons. 
                El horario de las salas es de 8am a 8pm, de lunes a viernes. Cuando el 
                usuario seleccione un espacio, deberas comenzar tu siguiente respuesta con $$NOMBRE DEL AREA RESERVADA$$ y continuar a preguntarle
                por el horario y el numero de personas que asistiran con el. Al finalizar debes confirmarle los datos de su reservacion.
                Si el usuario elige el lego room, adicionalmente tendras que preguntar por la cantidad de mesas que va a utilizar.
                """