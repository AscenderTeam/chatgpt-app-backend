from clis.controller_cli.cli_processor import ControllerCLI
from clis.migrate_cli import MigrateCLI
from clis.tests.cluster_tests import ClusterTestsCLI
from core.application import Application
from core.cli.processor import CLI
from fastapi.middleware.cors import CORSMiddleware


class Bootstrap:

    @staticmethod
    def server_boot_up(app: Application):
        app.use_database()
        app.use_sio()
        app.use_authentication()
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"]
        )
        app.loader_module.register_controller({
            'name': "API Service",
            'base_path': 'controllers',
            'exclude_controllers': [],
            'initialize_all_controllers': True,
        })
        # Load all controllers
        app.loader_module.load_all_controllers()

    @staticmethod
    def cli_boot_up(_: Application, cli: CLI):
        cli.register_generic(MigrateCLI())
        cli.register_generic(ControllerCLI())
        # Tests
        cli.register_generic(ClusterTestsCLI())
