from django.utils.translation import gettext_lazy as _
from saas_base.registry import perm_registry

perm_registry.register_permission(
    key='user.session.view',
    label=_('View Sessions'),
    module='User',
    description=_('List all active sessions for the user'),
)

perm_registry.register_permission(
    key='user.session.manage',
    label=_('Manage Sessions'),
    module='User',
    description=_('Delete any active sessions for the user'),
)

perm_registry.register_permission(
    key='user.token.view',
    label=_('View Tokens'),
    module='User',
    description=_('List all API tokens for the user'),
)

perm_registry.register_permission(
    key='user.token.manage',
    label=_('Manage Tokens'),
    module='User',
    description=_('Add, update, delete any API tokens for the user'),
)
