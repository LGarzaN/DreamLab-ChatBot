tools = [
    {
        "type": "file_search"
    },
    {
        "type": "function",
        "function": {
            "name": "get_zones",
            "description": "Obtiene todas las zonas existentes dentro del DreamLab, sabiendo que estas no se pueden reservar; sino que contienen dentro de ellas diferentes espacios que se pueden reservar, regresando una lista de zonas con su nombre y descripción"
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_spaces_by_zone",
            "description": "Obtiene todos los espacios existentes dentro de una zona en específico dentro del DreamLab, recibiendo el nombre de la zona y regresando una lista de espacios con su nombre y descripción",
            "parameters": {
                "type": "object",
                "properties": {
                    "zone_name": {
                        "type": "string",
                        "description": "El nombre de la zona que se desea obtener los espacios"
                    }
                },
                "required": ["zone_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_userid",
            "description": "Obtiene el ID de un usuario en específico dentro del DreamLab, recibiendo el nombre del usuario y regresando el ID del usuario, el ID no se le debe dar al usuario",
            "parameters": {
                "type": "object",
                "properties": {
                    "UserName": {
                        "type": "string",
                        "description": "El nombre del usuario que se desea obtener el ID"
                    }
                },
                "required": ["UserName"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_space_description",
            "description": "Obtiene la descripción de un espacio en específico dentro del DreamLab, recibiendo el nombre del espacio y regresando el ID y descripción, el ID no se le debe dar al usuario",
            "parameters": {
                "type": "object",
                "properties": {
                    "spaceName": {
                        "type": "string",
                        "description": "El nombre del espacio que se desea obtener la descripción"
                    }
                },
                "required": ["spaceName"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_schedule",
            "description": "Obtiene el horario de un espacio en específico dentro del DreamLab, recibiendo el ID del espacio y el día de la semana (lunes, martes, miércoles, jueves, viernes, sábado, domingo), en caso de darse en otro formato como fecha DD/MM/AAAA u otro es tu responsabilidad ajustar el formato para que coincida, regresando una lista de horarios con la hora de inicio y fin de cada uno",
            "parameters": {
                "type": "object",
                "properties": {
                    "SpaceId": {
                        "type": "integer",
                        "description": "El ID del espacio que se desea obtener el horario"
                    },
                    "Day": {
                        "type": "string",
                        "description": "El día de la semana que se desea obtener el horario, e.g. ('lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo')"
                    }
                },
                "required": ["SpaceId", "Day"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_space_requirements",
            "description": "Obtiene los requerimientos de un espacio en específico dentro del DreamLab, recibiendo el ID del espacio y regresando una lista de requerimientos con el ID del espacio, ID del requerimiento, nombre del requerimiento y cantidad máxima permitida de ese requerimiento",
            "parameters": {
                "type": "object",
                "properties": {
                    "SpaceId": {
                        "type": "integer",
                        "description": "El ID del espacio que se desea obtener los requerimientos"
                    }
                },
                "required": ["SpaceId"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "create_reservation_bot",
            "description": "Crea una reserva en el DreamLab, recibiendo el ID del usuario, el horario de la reserva, los requerimientos (herramientas que va a utilizar el usuario durante su reserva) del usuario y el ID del espacio, regresando un mensaje de confirmación de la reserva",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "integer",
                        "description": "El ID del usuario que realiza la reserva"
                    },
                    "schedule": {
                        "type": "string",
                        "description": "El horario de la reserva, en formato Dia - Hora, e.g. viernes 16 o lunes 10"
                    },
                    "user_requirements": {
                        "type": "string",
                        "description": "La cantidad de cada requerimiento que necesitará el usuario para la reserva, en formato ID de los requerimientos separados por comas seguido de espacio y la cantidad de cada requerimiento separados por comas, e.g. 5,2,3,4 1,1,1,1, donde el primer conjunto de numeros son los ID's de los requerimientos y el segundo conjunto es la cantidad de esos requerimiento, siendo que el primer numero del primer segmento corresponde al primer numero del segundo segmento y así sucesivamente"
                    },
                    "space_id": {
                        "type": "integer",
                        "description": "El ID del espacio que se desea reservar"
                    },
                },
                "required": ["user_id", "schedule", "user_requirements", "space_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_reservations",
            "description": "Obtiene las reservaciones de un usuario en específico dentro del DreamLab, recibiendo el ID del usuario y regresando una lista de reservaciones con el día, hora de inicio, hora de fin, nombre del espacio, ID del espacio, ID de los requerimientos, cantidad de requerimientos, y código del grupo, el ID de la reserva no se le debe dar al usuario",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "integer",
                        "description": "El ID del usuario que se desea obtener las reservaciones"
                    }
                },
                "required": ["user_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "delete_reservation",
            "description": "Elimina una reserva en el DreamLab, recibiendo el ID del usuario y el código del grupo, y regresando un mensaje de confirmación de la eliminación de la reserva",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "integer",
                        "description": "El ID del usuario que desea eliminar la reserva"
                    },
                    "group_code": {
                        "type": "string",
                        "description": "El código del grupo de la reserva que se desea eliminar"
                    }
                },
                "required": ["user_id", "group_code"]
            }
        }
    },
],