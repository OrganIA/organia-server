# import logging

# from . import config
# from .log import WebhookHandler

# logging.basicConfig(
#     level=logging.DEBUG,
#     # handlers=[WebhookHandler(config.DISCORD_LOGS)],
# )

# logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)

# sqlalchemy_logger = logging.getLogger('sqlalchemy')
# sqlalchemy_logger.setLevel(logging.WARNING)


from . import models
