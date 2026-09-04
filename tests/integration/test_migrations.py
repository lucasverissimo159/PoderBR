from alembic.config import Config

from alembic import command


def test_migrations_smoke():
    """
    Ensures that alembic migrations can be run forwards and backwards
    without catastrophic syntax or dependency errors.
    """
    alembic_cfg = Config("alembic.ini")

    # Run all migrations up
    command.upgrade(alembic_cfg, "head")

    # Downgrade back to base
    command.downgrade(alembic_cfg, "base")

    # Upgrade back to head to leave the DB in a usable state
    # for other tests if they share it
    command.upgrade(alembic_cfg, "head")

    assert True
