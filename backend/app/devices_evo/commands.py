from .client import EvoClient


class EvoCommands(EvoClient):

    # =====================================
    # LISTAR USUÁRIOS
    # =====================================

    def get_users(self):

        response = self.send({

            "cmd": "getuserlist",

            "stn": 1
        })

        print("=================================")
        print("GET USERS RESPONSE")
        print("=================================")
        print(response)

        return response

    # =====================================
    # NOVO ID
    # =====================================

    def get_new_userid(self):

        response = self.send({

            "cmd": "getunuserid"
        })

        print("=================================")
        print("GET NEW USERID RESPONSE")
        print("=================================")
        print(response)

        return response

    # =====================================
    # CRIAR USUÁRIO
    # =====================================

    def create_user(
        self,
        enrollid,
        name,
        department="",
        password_user="",
        admin=0
    ):

        response = self.send({

            "cmd": "setuserinfo",

            # ID REAL DO RELÓGIO
            "enrollid": int(enrollid),

            "name": str(name),

            "department": str(department),

            "password": str(password_user),

            "pwd": str(password_user),

            "admin": int(admin),

            "card": 0,

            "groupid": 1,

            "shiftid": 1,

            "zoneid": 0,

            "verifymode": 0,

            "birthday": "",

            "starttime": "",

            "endtime": "",

            "userprofile": "",

            "access_times": 0
        })

        print("=================================")
        print("CREATE USER RESPONSE")
        print("=================================")
        print(response)

        return response

    # =====================================
    # DELETAR USUÁRIO
    # =====================================

    def delete_user(self, enrollid):

        print("=================================")
        print("DELETE USER")
        print("=================================")

        print("ENROLLID:")
        print(enrollid)

        response = self.send({

            "cmd": "deleteusers",

            # EVO EXIGE ARRAY
            "list": [int(enrollid)]
        })

        print("=================================")
        print("DELETE USERS RESPONSE")
        print("=================================")
        print(response)

        return response

    # =====================================
    # CHECAR USUÁRIO
    # =====================================

    def check_user(self, enrollid):

        response = self.send({

            "cmd": "checkuserid",

            "enrollid": int(enrollid)
        })

        print("=================================")
        print("CHECK USER RESPONSE")
        print("=================================")
        print(response)

        return response

    # =====================================
    # INFO DISPOSITIVO
    # =====================================

    def device_info(self):

        response = self.send({

            "cmd": "getdevinfo"
        })

        print("=================================")
        print("DEVICE INFO RESPONSE")
        print("=================================")
        print(response)

        return response

     # =====================================
    # REGISTROS TEMPO REAL
    # =====================================

    def get_real_time_logs(self, index=-1):

        response = self.send({

            "cmd": "getrtlog",

            "index": index
        })

        print("=================================")
        print("GET RT LOG RESPONSE")
        print("=================================")
        print(response)

        return response

    # =====================================
    # LISTAR FACES
    # =====================================

    def get_faces(self):

        response = self.send({

            "cmd": "getallface"
        })

        print("=================================")
        print("GET ALL FACE RESPONSE")
        print("=================================")
        print(response)

        return response

    # =====================================
    # DELETAR FACE
    # =====================================

    def delete_face(self, enrollid):

        response = self.send({

            "cmd": "delface",

            "enrollid": int(enrollid)
        })

        print("=================================")
        print("DELETE FACE RESPONSE")
        print("=================================")
        print(response)

        return response

    # =====================================
    # SINCRONIZAR HORA
    # =====================================

    def sync_time(self):

        from datetime import datetime

        now = datetime.now()

        response = self.send({

            "cmd": "settime",

            "year": now.year,

            "month": now.month,

            "day": now.day,

            "hour": now.hour,

            "minute": now.minute,

            "second": now.second
        })

        print("=================================")
        print("SYNC TIME RESPONSE")
        print("=================================")
        print(response)

        return response

    # =====================================
    # LIMPAR LOGS
    # =====================================

    def clear_logs(self):

        response = self.send({

            "cmd": "clearlog"
        })

        print("=================================")
        print("CLEAR LOG RESPONSE")
        print("=================================")
        print(response)

        return response

    # =====================================
    # CAPACIDADE
    # =====================================

    def get_capacity(self):

        response = self.send({

            "cmd": "getcapacity"
        })

        print("=================================")
        print("GET CAPACITY RESPONSE")
        print("=================================")
        print(response)

        return response

    # =====================================
    # STATUS ONLINE
    # =====================================

    def ping(self):

        try:

            response = self.device_info()

            return {
                "online": True,
                "response": response
            }

        except Exception as e:

            return {
                "online": False,
                "error": str(e)
            }
    

    def test_command(self, cmd):

        response = self.send({

            "cmd": cmd

        })

        print("=================================")
        print("TEST COMMAND:", cmd)
        print("=================================")
        print(response)

        return response

    
    def get_logs(self, from_index=0):

        response = self.send({

            "cmd": "getlog",

            "from": from_index

        })

        return response

    def get_logs(self, from_index=0):

        return self.send({

            "cmd": "getlog",

            "from": from_index

        })