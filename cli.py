import click
from sqlalchemy import text

from maine_lpr_db_models.base import Base, create_database_engine


def insert_status(connection, id, name):
    sql_stmt = text(
        "INSERT INTO lprdb.lpr_masked_event_statuses (id, name) "
        "VALUES(:id, :name) ON DUPLICATE KEY UPDATE name = VALUES(name)"
    )

    connection.execute(sql_stmt, {"id": id, "name": name})


def insert_camera_vendor(connection, id, name):
    sql_stmt = text(
        "INSERT INTO lprdb.lpr_camera_vendors (id, name) "
        "VALUES(:id, :name) ON DUPLICATE KEY UPDATE name = VALUES(name)"
    )

    connection.execute(sql_stmt, {"id": id, "name": name})


def insert_camera_vendor_data(engine):
    from maine_lpr_db_models.lprcamervendors import LprCameraVendorsEnum

    with engine.connect() as connection:
        try:
            insert_camera_vendor(
                connection,
                LprCameraVendorsEnum.OPENALPR.value,
                "OpenALPR",
            )
            connection.commit()
        except Exception:
            connection.rollback()
        try:
            insert_camera_vendor(
                connection,
                LprCameraVendorsEnum.LAB18.value,
                "Lab18",
            )
            connection.commit()
        except Exception:
            connection.rollback()
        try:
            insert_camera_vendor(
                connection,
                LprCameraVendorsEnum.SURVISION.value,
                "Survision",
            )
            connection.commit()
        except Exception:
            connection.rollback()


def insert_status_table_data(engine):
    from maine_lpr_db_models.lprmaskedeventsstatus import LprMaskedEventStatusesEnum

    with engine.connect() as connection:
        try:
            insert_status(
                connection,
                LprMaskedEventStatusesEnum.PENDING_DATA_ENTRY.value,
                "Pending data entry",
            )
            connection.commit()
        except Exception as ex:
            print(ex)
            connection.rollback()
        try:
            insert_status(
                connection,
                LprMaskedEventStatusesEnum.RESERVED_FOR_DATA_ENTRY.value,
                "Reserved by data entry operator",
            )
            connection.commit()
        except Exception:
            connection.rollback()
        try:
            insert_status(
                connection,
                LprMaskedEventStatusesEnum.PENDING_DELIVERY.value,
                "Data entry completed and pending delivery",
            )
            connection.commit()
        except Exception:
            connection.rollback()
        try:
            insert_status(
                connection,
                LprMaskedEventStatusesEnum.DELIVERED.value,
                "Delivered to destination",
            )
            connection.commit()
        except Exception:
            connection.rollback()
        try:
            insert_status(
                connection,
                LprMaskedEventStatusesEnum.DELIVERY_FAILED.value,
                "Delivery to destination failed",
            )
            connection.commit()
        except Exception:
            connection.rollback()




@click.command()
@click.option("--db-url", envvar="DATABASE_URL", required=True)
def init_db(db_url):
    db_engine = create_database_engine(db_url)
    Base.metadata.create_all(bind=db_engine)
    insert_status_table_data(db_engine)
    insert_camera_vendor_data(db_engine)
    click.echo("Database initialized!")
