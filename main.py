import openai
from dotenv import find_dotenv, load_dotenv
import time
import logging
from datetime import datetime
import os
import requests
import json
import streamlit as st
from chatbot import tools

load_dotenv()

client = openai.OpenAI()
model = "gpt-4-turbo"
vector_store_id = os.environ.get("VECTOR_STORE_ID")

# Valor de la API Key para comunicarse con la base de datos
api_key = os.environ.get("X_API_KEY")
# Configurar los encabezados de la solicitud
headers = {
    "x-api-key": api_key
}

file_path = "documents/SystemPrompt.txt"

def read_system_prompt(file_path):
    """
    Lee un archivo de texto y retorna su contenido como una cadena de texto.
    
    :param file_path: La ruta al archivo de texto que se desea leer.
    :return: El contenido del archivo como una cadena de texto.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as archivo:
            contenido = archivo.read()
        return contenido
    except FileNotFoundError:
        print(f"El archivo en la ruta {file_path} no se encuentra.")
    except IOError:
        print(f"Ha ocurrido un error al intentar leer el archivo {file_path}.")

def create_reservation_bot(user_id, schedule, user_requirements, space_id):
    url = ( 
        f"https://dlbackendtws.azurewebsites.net/chatbot/create/bot"
    )
    payload = {
        "user_id": user_id,
        "schedule": schedule,
        "user_requirements": user_requirements,
        "space_id": space_id
    }
    print("\n\n\nPayload: ", payload)
    print("\n\n\n")
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 201 or response.status_code == 200:
            # Succesfully created
            data = response.json()
            print("Reserva creada exitosamente:", data)
            return data
        else:
            print("Error al crear la reserva - Código de estado:", response.status_code)
            return None
    except requests.exceptions.RequestException as e:
        print("Error occurred during API Request ", e)
        return None

def delete_reservation(user_id, group_code):
    url = (
        f"https://dlbackendtws.azurewebsites.net/chatbot"
    )
    payload = {
        "user_id": user_id,
        "group_code": group_code
    }
    print("\n\n\nPayload: ", payload)
    print("\n\n\n")
    try:
        response = requests.delete(url, json=payload, headers=headers)
        if response.status_code == 200:
            # Delete was successful
            data = response.json()
            print("Reserva eliminada exitosamente:", data)
            return data
        else:
            print("Error al eliminar la reserva - Código de estado:", response.status_code)
            return None
    except requests.exceptions.RequestException as e:
        print("Error occurred during API Request ", e)
        return None

def get_userid(UserName):
    url = (
        f"https://dlbackendtws.azurewebsites.net/chatbot/userid/{UserName}"
    )
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            # Obtener los datos en formato JSON
            data = response.json()
            final_user = []

            for user in data:
                user_id = user["UserId"]
                final_user.append(f"""
                    Id: {user_id},
                    Name: {UserName}
                    """)
            # Imprimir los datos recibidos
            print("Datos recibidos get_userid:", user_id)
            return final_user
        else:
            print("Error ocurred during API Request - get_userid()")
            return []
    except requests.exceptions.RequestException as e:
        print("Error ocurred during API Request ", e)

def get_zones():
    url = (
        f"https://dlbackendtws.azurewebsites.net/chatbot/zones"
    )
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            # Obtener los datos en formato JSON
            data = response.json()
            zones = []

            # Loop through the data
            for zone in data:
                zone_description = zone["Zone"]
                zones.append(zone_description)
            # Imprimir los datos recibidos
            print("Datos recibidos get_zones:", zones)
            return zones
        else:
            print("Error ocurred during API Request - get_zones()")
            return []
    except requests.exceptions.RequestException as e:
        print("Error ocurred during API Request ", e)

def get_spaces_by_zone(zone_name):
    url = (
        f"https://dlbackendtws.azurewebsites.net/chatbot/spaces/zone/{zone_name}"
    )
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            # Obtener los datos en formato JSON
            data = response.json()
            final_spaces = []

            # Loop through the data
            for space in data:
                id = space["SpaceId"]
                name = space["Name"]
                descripction = space["Description"]
                final_spaces.append(f"""
                    Id: {id},
                    Name: {name},
                    Description: {descripction}
                    """)
            # Imprimir los datos recibidos
            print("Datos recibidos get_spaces_by_zone:", final_spaces)
            return final_spaces
        else:
            print("Error ocurred during API Request - get_spaces_by_zone()")
            return []
    except requests.exceptions.RequestException as e:
        print("Error ocurred during API Request ", e)

def get_space_description(space_name):
    url = (
        f"https://dlbackendtws.azurewebsites.net/chatbot/spaces/{space_name}"
    )
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            # Obtener los datos en formato JSON
            data = response.json()
            final_space = []

            for space in data:
                id = space["SpaceId"]
                name = space["Name"]
                descripction = space["Description"]
                final_space.append(f"""
                    Id: {id},
                    Name: {name},
                    Description: {descripction}
                    """)
            # Imprimir los datos recibidos
            print("Datos recibidos get_space_description:", final_space)
            return final_space
        else:
            print("Error ocurred during API Request - get_space_description()")
            return []
    except requests.exceptions.RequestException as e:
        print("Error ocurred during API Request ", e)

def get_schedule(SpaceId, Day):
    url = (
        f"https://dlbackendtws.azurewebsites.net/chatbot/schedules/{SpaceId}/{Day}"
    )
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            # Obtener los datos en formato JSON
            data = response.json()
            final_schedule = []

            # Loop through the data
            for schedule in data:
                StartHour = schedule["StartHour"]
                EndHour = schedule["EndHour"]
                final_schedule.append(f"""
                    Start Hour: {StartHour},
                    End Hour: {EndHour}
                    """)
            # Imprimir los datos recibidos
            print("Datos recibidos get_schedule:", final_schedule)
            return final_schedule
        else:
            print("Error ocurred during API Request - get_schedule()")
            return []
    except requests.exceptions.RequestException as e:
        print("Error ocurred during API Request ", e)

def get_space_requirements(SpaceId):
    url = (
        f"https://dlbackendtws.azurewebsites.net/chatbot/requirements/{SpaceId}"
    )
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            # Obtener los datos en formato JSON
            data = response.json()
            final_requirements = []
            
            # Loop through the data
            for requirement in data:
                SpaceId = requirement["SpaceId"]
                requirementsId = requirement["RequirementId"]
                requirementName = requirement["RequirementName"]
                maxQuantity = requirement["MaxQuantity"]
                final_requirements.append(f"""
                    SpaceId: {SpaceId},
                    RequirementId: {requirementsId},
                    Requirement Name: {requirementName},
                    Max Quantity: {maxQuantity}
                    """)
            
            # Imprimir los datos recibidos
            print("Datos recibidos get_space_requirements:", final_requirements)
            return final_requirements
        else:
            print("Error ocurred during API Request - get_space_requirements()")
            return []
    except requests.exceptions.RequestException as e:
        print("Error ocurred during API Request ", e)

def get_reservations(user_id):
    url = (
        f"https://dlbackendtws.azurewebsites.net/chatbot/{user_id}"
    )
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            # Obtener los datos en formato JSON
            data = response.json()
            final_reservations = []

            # Loop through the data
            for reservation in data:
                Day = reservation["Day"]
                StartHour = reservation["StartHour"]
                EndHour = reservation["EndHour"]
                SpaceName = reservation["SpaceName"]
                SpaceId = reservation["SpaceId"]
                RequirementId = reservation["RequirementsId"]
                Quantity = reservation["RequirementsQuantity"]
                GroupCode = reservation["GroupCode"]
                final_reservations.append(f"""
                    Day: {Day},
                    Start Hour: {StartHour},
                    End Hour: {EndHour},
                    Space Name: {SpaceName},
                    Space Id: {SpaceId},
                    Requirement Id: {RequirementId},
                    Quantity: {Quantity},
                    Group Code: {GroupCode}
                    """)
            # Imprimir los datos recibidos
            print("Datos recibidos get_reservations:", final_reservations)
            return final_reservations
        else:
            print("Error ocurred during API Request - get_reservations()")
            return []
    except requests.exceptions.RequestException as e:
        print("Error ocurred during API Request ", e)

class AssistantManager:
    thread_id = None
    assistant_id = "asst_XPg009w2uccOa5eKVeg62dxO"

    def __init__(self, model: str = model):
        self.client = client
        self.model = model
        self.assistant = None
        self.thread = None
        self.run = None
        self.summary = None

        # Retrieve existing assistant and thread if IDs are already set
        if AssistantManager.assistant_id:
            self.assistant = self.client.beta.assistants.retrieve(
                assistant_id = AssistantManager.assistant_id
            )
        if AssistantManager.thread_id:
            self.thread = self.client.beta.threads.retrieve(
                thread_id = AssistantManager.thread_id
            )
    def create_assistant(self, name, instructions, temperature, top_p, max_tokens, tools, tool_resources):
        if not self.assistant:
            assistant_obj = self.client.beta.assistants.create(
                name = name,
                instructions = instructions,
                temperature = temperature,
                top_p = top_p,
                #max_tokens = max_tokens,
                tools = tools,
                model = self.model,
                tool_resources = tool_resources
            )
            AssistantManager.assistant_id = assistant_obj.id
            self.assistant = assistant_obj
            print(f"Assistant created with ID: {self.assistant.id}")
    
    def create_thread(self):
        if not self.thread:
            thread_obj = self.client.beta.threads.create()
            AssistantManager.thread_id = thread_obj.id
            self.thread = thread_obj
            print(f"Thread created with ID: {self.thread.id}")

    def add_message_to_thread(self, role, content):
        if self.thread:
            self.client.beta.threads.messages.create(
                thread_id = self.thread.id,
                role = role,
                content = content
            )
    
    def run_assistant(self, instructions):
        if self.thread and self.assistant:
            self.run = self.client.beta.threads.runs.create(
                thread_id = self.thread.id,
                assistant_id = self.assistant.id,
                instructions = instructions
            )
    
    def process_message(self):
        if self.thread:
            messages = self.client.beta.threads.messages.list(
                thread_id = self.thread.id
            )
            summary = []

            last_message = messages.data[0]
            role = last_message.role
            response = last_message.content[0].text.value
            summary.append(response)

            self.summary = "\n".join(summary)
            print(f"SUMMARY-----> {role.capitalize()}: ==> {response}")

            #for msg in messages:
            #    role = msg.role
            #    content = msg.content[0].text.value
            #    print(f"SUMMARY-----> {role.capitalize()}: ==> {response}")
    
    def call_required_functions(self, required_actions):
        if not self.run:
            return
        tool_outputs = []

        for action in required_actions["tool_calls"]:
            func_name = action["function"]["name"]
            arguments = json.loads(action["function"]["arguments"])
            
            if func_name == "get_userid":
                output = get_userid(UserName=arguments["UserName"])
                print(f"Output of get_userid: {output}")
                final_str = ""
                for item in output:
                    final_str += "".join(item)
                
                tool_outputs.append({"tool_call_id": action["id"], 
                                    "output": final_str})

            elif func_name == "get_zones":
                output = get_zones()
                print(f"Output of get_zones: {output}")
                final_str = ""
                for item in output:
                    final_str += "".join(item)
                
                tool_outputs.append({"tool_call_id": action["id"], 
                                    "output": final_str})
            
            elif func_name == "get_spaces_by_zone":
                output = get_spaces_by_zone(zone_name=arguments["zone_name"])
                print(f"Output of get_spaces_by_zone: {output}")
                final_str = ""
                for item in output:
                    final_str += "".join(item)
                
                tool_outputs.append({"tool_call_id": action["id"], 
                                    "output": final_str})
                
            elif func_name == "get_space_description":
                output = get_space_description(space_name=arguments["spaceName"])
                print(f"Output of get_space_description: {output}")
                final_str = "".join(output)
                
                tool_outputs.append({"tool_call_id": action["id"], 
                                    "output": final_str})
                
            elif func_name == "get_schedule":
                output = get_schedule(SpaceId=arguments["SpaceId"], Day=arguments["Day"])
                print(f"Output of get_schedule: {output}")
                final_str = ""
                for item in output:
                    final_str += "".join(item)
                
                tool_outputs.append({"tool_call_id": action["id"], 
                                    "output": final_str})
                
            elif func_name == "get_space_requirements":
                output = get_space_requirements(SpaceId=arguments["SpaceId"])
                print(f"Output of get_space_requirements: {output}")
                final_str = ""
                for item in output:
                    final_str += "".join(item)
                
                tool_outputs.append({"tool_call_id": action["id"], 
                                    "output": final_str})
            elif func_name == "create_reservation_bot":
                output = create_reservation_bot(user_id=arguments["user_id"], 
                                                schedule=arguments["schedule"], 
                                                user_requirements=arguments["user_requirements"], 
                                                space_id=arguments["space_id"])
                print(f"Output of create_reservation_bot: {output}")
                final_str = f"Reserva creada exitosamente: {output}"
                
                tool_outputs.append({"tool_call_id": action["id"], 
                                    "output": final_str})
                
            elif func_name == "get_reservations":
                output = get_reservations(user_id=arguments["user_id"])
                print(f"Output of get_reservations: {output}")
                final_str = ""
                for item in output:
                    final_str += "".join(item)
                
                tool_outputs.append({"tool_call_id": action["id"], 
                                    "output": final_str})
                
            elif func_name == "delete_reservation":
                output = delete_reservation(user_id=arguments["user_id"], 
                                            group_code=arguments["group_code"])
                print(f"Output of delete_reservation: {output}")
                final_str = f"Reserva eliminada exitosamente: {output}"
                
                tool_outputs.append({"tool_call_id": action["id"], 
                                    "output": final_str})
                
            else:
                raise ValueError(f"Unknown function: {func_name}")
            
        print("Submiting outputs back to the assistant...")
        self.client.beta.threads.runs.submit_tool_outputs(
            thread_id = self.thread.id,
            run_id = self.run.id,
            tool_outputs = tool_outputs
        )

    # for streamlit
    def get_summary(self):  
        return self.summary
    
    def wait_for_completion(self):
        if self.thread and self.run:
            while True:
                time.sleep(5)
                run_status = self.client.beta.threads.runs.retrieve(
                    thread_id = self.thread.id,
                    run_id = self.run.id
                )
                
                if run_status.status == "completed":
                    self.process_message()
                    break
                elif run_status.status == "requires_action":
                    print("Function Calling Now...")
                    self.call_required_functions(
                        required_actions = run_status.required_action.submit_tool_outputs.model_dump()
                    )

#print(f"Run status: {run_status.model_dump_json(indent=4)}")

    # Run the steps
    def run_steps(self):
        run_steps = self.client.beta.threads.runs.steps.list(
            thread_id = self.thread.id,
            run_id = self.run.id
        )
        return run_steps.data

#print(f"Run steps: {run_steps}")

def initialize_assistant():
    file = read_system_prompt(file_path)
    print("\n\n\nEjecutando el chatbot\n\n\n")

    manager = AssistantManager()

    # Create the assistant
    manager.create_assistant(
        name = "TechBot",
        instructions = file,
        temperature = 0.01,
        top_p = 0.01,
        max_tokens = 150,
        tools = tools,
        tool_resources = {"file_search": {"vector_store_ids": [vector_store_id]}},
    )


    # Create the thread
    manager.create_thread()
    return manager


def main():
    if 'manager' not in st.session_state:
        st.session_state.manager = initialize_assistant()

    # Streamlit interface
    st.title("ChatBot DreamLab")

    with st.form(key="user_input_form"):
        instructions = st.text_area("Enter topic:")
        submit_button = st.form_submit_button(label="Run Assistant")

        if submit_button:
            manager = st.session_state.manager
            # Add the message and run the assistant
            manager.add_message_to_thread(
                role = "user",
                content = f"{instructions}"
            )

            manager.run_assistant(instructions="Usa los archivos a los que tienes acceso por medio de file search para encontrar información relevante en los documentos, muestra la información clara al usuario y ayudalo a realizar la reservación en el DreamLab. Procura ser amigable y claro en tus respuestas, de ser necesario pregunta al usuario para obtener más información y poder ayudarlo de la mejor manera posible.")

            # Wait for completions and process messages
            manager.wait_for_completion()

            summary = manager.get_summary()

            st.write(summary)

            st.text("Run Steps:")
            st.code(manager.run_steps(), line_numbers=True)

if __name__ == "__main__":
    main()