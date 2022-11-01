from flask.cli import AppGroup
from service import Application as root


cli = AppGroup("sql", help="database operations")


@cli.command("create", help="creates the database")
def create_db():
    root.postgres.drop_all()
    root.postgres.create_all()


@cli.command("drop", help="drops the database")
def drop_db():
    root.postgres.drop_all()
