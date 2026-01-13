from django.utils.translation import gettext_lazy as _
from saas_base.registry import perm_registry

perm_registry.register_permission(
    key='user.sessions.view',
    label=_('View Sessions'),
    module='User',
    description=_('List all active sessions for the user'),
)

perm_registry.register_permission(
    key='user.sessions.manage',
    label=_('Manage Sessions'),
    module='User',
    description=_('Delete any active sessions for the user'),
)

perm_registry.register_permission(
    key='user.tokens.view',
    label=_('View Tokens'),
    module='User',
    description=_('List all API tokens for the user'),
)

perm_registry.register_permission(
    key='user.tokens.manage',
    label=_('Manage Tokens'),
    module='User',
    description=_('Add, update, delete any API tokens for the user'),
)
