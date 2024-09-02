import os
import sys

from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import NullPool


class DatabaseConnection:
    """
    Manages the database connection, provides connection and session objects,
    and reflects database tables for ORM use.

    Attributes:
    -----------
    engine : sqlalchemy.engine.Engine
        The SQLAlchemy engine object used for database connections.
    session_factory : sqlalchemy.orm.session.sessionmaker
        A session factory to create new session objects.
    metadata : sqlalchemy.ext.automap.AutomapBase
        The metadata object containing reflected table information.
    app_config : dict
        A dictionary containing database configuration settings.

    Methods:
    --------
    get_engine():
        Returns the created engine object for database connection.

    get_session():
        Returns a new session object based on the engine.

    get_metadata():
        Returns the reflected metadata object containing table information.
    """

    def __init__(self, app_config):
        self.engine = None
        self.session_factory = None
        self.metadata = None
        self.app_config = app_config
        self._connect()

    def _connect(self):
        try:
            engine_string = self._load_engine_string()
            self.engine = create_engine(engine_string,
                                        connect_args={'connect_timeout': int(self.app_config.get("TIMEOUT"))},
                                        poolclass=NullPool)

            if self.engine.connect():
                self.session_factory = sessionmaker(bind=self.engine)
                # Reflect tables from database
                declarative_base()
                Base = automap_base()
                # reflect the tables
                Base.prepare(self.engine, reflect=True)
                self.metadata = Base
            else:
                raise ConnectionError("Failed to connect to the Database")

        except Exception as error:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print('_connect Error: {0} {1} {2}'.format(exc_type, fname, exc_tb.tb_lineno))
            raise error

    def _load_engine_string(self):
        driver = self.app_config.get("DRIVER")
        engine_string = "{0}://{1}:{2}@{3}:{4}/{5}"
        return engine_string.format(driver,
                                    self.app_config.get("USER"),
                                    self.app_config.get("PASSWORD"),
                                    self.app_config.get("HOST"),
                                    self.app_config.get("PORT"),
                                    self.app_config.get("DATABASE"))

    def get_engine(self):
        return self.engine

    def get_session(self):
        if self.session_factory:
            return self.session_factory()
        else:
            raise ConnectionError("Database connection not established")

    def get_metadata(self):
        return self.metadata
