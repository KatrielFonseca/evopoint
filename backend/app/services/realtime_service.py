import time

from datetime import datetime

from app.database.database import SessionLocal

from app.models.time_record import TimeRecord
from app.models.settings import Settings

from app.devices_evo.commands import EvoCommands


# =====================================================
# REALTIME SERVICE
# =====================================================
from app.models.deleted_log import DeletedLog

# =========================================
# STATUS GLOBAL DO REALTIME
# =========================================

REALTIME_STATUS = {

    "capture": False,

    "evo_online": False

}


# =========================================
# SINCRONIZA HISTÓRICO
# =========================================

def sync_historical_logs():

    db = SessionLocal()

    try:

        settings = db.query(
            Settings
        ).first()

        if not settings:
            return

        evo = EvoCommands(

            settings.evo_ip,

            settings.evo_port,

            settings.evo_password

        )

        from_index = settings.last_log_index or 0

        print("================================")
        print("ULTIMO INDEX SALVO:")
        print(settings.last_log_index)
        print("FROM INDEX:")
        print(from_index)
        print("================================")

        logs = evo.get_logs(from_index)

        print(logs)

        records = logs.get("record", [])

        if not records:

            print("SEM LOGS HISTÓRICOS")

            return

            print(
                f"IMPORTANDO {len(records)} LOGS"
            )

        for log in records:

            try:

                enrollid = str(
                    log.get(
                        "enrollid",
                        ""
                    )
                ).strip()

                if (
                    not enrollid
                    or
                    enrollid == "99999999"
                ):
                    continue

                log_time_raw = str(
                    log.get(
                        "time",
                        ""
                    )
                ).strip()

                if not log_time_raw:
                    continue

                log_time = datetime.strptime(
                    log_time_raw,
                    "%Y-%m-%d %H:%M:%S"
                )

                deleted = db.query(
                    DeletedLog
                ).filter(

                    DeletedLog.employee_registration
                    == enrollid,

                    DeletedLog.record_time
                    == log_time

                ).first()

                if deleted:
                    continue

                existing = db.query(
                    TimeRecord
                ).filter(

                    TimeRecord.employee_registration
                    == enrollid,

                    TimeRecord.record_time
                    == log_time

                ).first()

                if existing:
                    continue

                novo = TimeRecord(

                    employee_registration=
                    enrollid,

                    employee_name=
                    log.get(
                        "name",
                        ""
                    ),

                    record_time=
                    log_time,

                    verification_mode=
                    "Facial",

                    device_event=
                    str(
                        log.get(
                            "event",
                            ""
                        )
                    ),

                    inout=0

                )

                db.add(novo)

            except Exception as e:

                print(
                    "ERRO:",
                    e
                )

        db.commit()

        print("INDEX SALVO:")
        print(from_index)

        print(
            "HISTÓRICO IMPORTADO"
        )

    finally:

        db.close()


# =========================================
# REALTIME SERVICE
# =========================================


def start_realtime_capture():

    print("================================")
    print("REALTIME SERVICE INICIADO")
    print("================================")

    REALTIME_STATUS["capture"] = True


    sync_historical_logs()

    # =============================================
    # IGNORA LOGS ANTERIORES AO START DO SERVIÇO
    # =============================================

    service_started_at = datetime.now()

    print("IGNORANDO LOGS ANTERIORES A:")
    print(service_started_at)

    # =============================================
    # CACHE DE LOGS PROCESSADOS
    # EVITA DUPLICAÇÃO
    # =============================================

    processed_logs = set()

    while True:

        db = SessionLocal()

        try:

            # =========================================
            # CONECTA NO EVO
            # =========================================

            settings = db.query(
                Settings
            ).first()

            if not settings:

                print("CONFIGURAÇÕES EVO NÃO ENCONTRADAS")

                db.close()

                time.sleep(5)

                continue


            evo = EvoCommands(

                settings.evo_ip,

                settings.evo_port,

                settings.evo_password

            )


            logs = evo.get_real_time_logs()

            REALTIME_STATUS["evo_online"] = True

            records = logs.get("record", [])

            # =========================================
            # SEM REGISTROS
            # =========================================

            if not records:

                db.close()

                time.sleep(2)

                continue

            # =========================================
            # PROCESSA LOGS
            # =========================================

            for log in records:

                try:

                    enrollid = str(
                        log.get("enrollid", "")
                    ).strip()

                    employee_name = str(
                        log.get("name", "")
                    ).strip()

                    event = str(
                        log.get("event", "")
                    ).strip()

                    print("================================")
                    print("EVENTO RECEBIDO:")
                    print(log)
                    print("================================")

                    log_time_raw = str(
                        log.get("time", "")
                    ).strip()

                    # =================================
                    # VALIDAÇÕES
                    # =================================

                    if not enrollid:

                        continue

                    if enrollid == "99999999":

                        continue

                    if not log_time_raw:

                        continue

                    # =================================
                    # CONVERTE DATA
                    # =================================

                    log_time = datetime.strptime(
                        log_time_raw,
                        "%Y-%m-%d %H:%M:%S"
                    )

                    # =================================
                    # IGNORA LOGS ANTIGOS
                    # =================================

                    if log_time.year < 2025:
                        continue
                    # =================================
                    # CHAVE ÚNICA DO LOG
                    # =================================

                    log_key = (
                        f"{enrollid}_{log_time_raw}"
                    )

                    # =================================
                    # EVITA DUPLICAÇÃO EM MEMÓRIA
                    # =================================

                    if log_key in processed_logs:

                        continue

                    # =================================
                    # EVITA DUPLICAÇÃO NO BANCO
                    # =================================

                    existing = db.query(
                        TimeRecord
                    ).filter(

                        TimeRecord.employee_registration
                        == enrollid,

                        TimeRecord.record_time
                        == log_time

                    ).first()

                    if existing:

                        processed_logs.add(
                            log_key
                        )

                        continue

                    # =================================
                    # DEFINE ENTRADA / SAÍDA
                    # =================================

                    previous_record = db.query(
                        TimeRecord
                    ).filter(

                        TimeRecord.employee_registration
                        == enrollid

                    ).order_by(

                        TimeRecord.record_time.desc()

                    ).first()

                    inout = 0

                    if previous_record:

                        if previous_record.inout == 0:

                            inout = 1

                        else:

                            inout = 0

                    # =================================
                    # CRIA REGISTRO
                    # =================================

                    novo = TimeRecord(

                        employee_registration=
                            enrollid,

                        employee_name=
                            employee_name,

                        record_time=
                            log_time,

                        verification_mode=
                            "Facial",

                        device_event=
                            event,

                        inout=
                            inout
                    )

                    db.add(novo)

                    db.commit()

                    # =================================
                    # MARCA COMO PROCESSADO
                    # =================================

                    processed_logs.add(
                        log_key
                    )

                    # =================================
                    # LIMPA CACHE GRANDE
                    # =================================

                    if len(processed_logs) > 10000:

                        processed_logs.clear()

                    # =================================
                    # LOG
                    # =================================

                    print("================================")
                    print("NOVO PONTO REGISTRADO")
                    print("FUNCIONÁRIO:", employee_name)
                    print("MATRÍCULA:", enrollid)
                    print("HORÁRIO:", log_time)
                    print(
                        "TIPO:",
                        "ENTRADA"
                        if inout == 0
                        else "SAÍDA"
                    )
                    print("================================")

                except Exception as erro_log:

                    db.rollback()

                    print("================================")
                    print("ERRO AO PROCESSAR LOG")
                    print(str(erro_log))
                    print("LOG:")
                    print(log)
                    print("================================")

        except Exception as e:

            db.rollback()

            REALTIME_STATUS["evo_online"] = False

            print("================================")
            print("ERRO REALTIME")
            print(str(e))
            print("================================")

        finally:

            db.close()

        # =========================================
        # ESPERA
        # =========================================

        time.sleep(2)
