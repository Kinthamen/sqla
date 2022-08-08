from ..mixins.session_mixin import SessionMixin
from ..mixins.serializer_mixin import SerializerMixin
from ..mixins.audit_mixin import AuditMixin

class Base(SessionMixin, SerializerMixin):
    """Base mixing with all basic needs"""

class BaseAudit(SessionMixin, SerializerMixin, AuditMixin):
    """Base mixing with all basic needs and audit fields"""

