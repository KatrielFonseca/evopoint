from app.models.settings import Settings

def bump_system_version(db):

    settings = db.query(
        Settings
    ).first()

    if not settings:

        settings = Settings()

        settings.system_version = 1

        db.add(settings)

    else:

        settings.system_version = (
            settings.system_version or 1
        ) + 1