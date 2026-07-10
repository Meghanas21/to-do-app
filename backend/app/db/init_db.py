"""Create tables and seed roles/admin accounts on startup."""
from app.core.config import settings
from app.core.security import hash_password
from app.db.database import Base, SessionLocal, engine
from app.models import activity_log, document, role, task, user  # noqa: F401
from app.models.role import Role
from app.models.user import User


def init_db() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        if db.query(Role).count() == 0:
            db.add_all([Role(name="admin"), Role(name="user")])
            db.commit()

        admin_role = db.query(Role).filter(Role.name == "admin").first()
        user_role = db.query(Role).filter(Role.name == "user").first()
        if admin_role and user_role and db.query(User).count() == 0:
            db.add(
                User(
                    email=settings.DEFAULT_ADMIN_EMAIL,
                    hashed_password=hash_password(settings.DEFAULT_ADMIN_PASSWORD),
                    role_id=admin_role.id,
                )
            )
            db.commit()
    finally:
        db.close()
