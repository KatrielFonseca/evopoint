import time

from datetime import datetime

from app.database.database import SessionLocal

from app.models.time_record import TimeRecord

from app.devices_evo.commands import EvoCommands


# =====================================================
# REALTIME SERVICE
# =====================================================

def start_realtime_capture():

    print("================================")
    print("REALTIME SERVICE INICIADO")
    print("================================")

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

            evo = EvoCommands("192.168.88.9")

            logs = evo.get_real_time_logs()

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

                    if log_time < service_started_at:

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