import os
import logging

logger = logging.getLogger(__file__)

SETTINGS_DIR = 'agrawat_backend.settings'


def get_env_settings_file_name():
    deployment_env = os.getenv('DEPLOYMENT_ENVIRONMENT')

    if deployment_env not in {'dev', 'demo', 'prod'}:
        logger.warning(
            'No valid DEPLOYMENT_ENVIRONMENT given. Should be one of dev, prod, or demo.')
        settings_file = 'prod'
    else:
        settings_file = deployment_env

    logger.info(f'Using {settings_file} database.')

    return f'{SETTINGS_DIR}.{settings_file}'
