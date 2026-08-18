"""
solich/inherit/

Extension infrastructure for Solich — model field injection and CBV replacement.

Key public symbols re-exported here for convenience:

    from solich.inherit import SolichViewInheritMixin   # view extension
    from solich.inherit import SolichModelBase           # model metaclass
    from solich.inherit import INJECTION_MAP              # migration routing
    from solich.inherit import VIEW_REGISTRY              # registered views
"""

from solich.inherit.extension_registry import INJECTION_MAP
from solich.inherit.model_inherit import EXTENSION_REGISTRY, SolichModelBase
from solich.inherit.view_inherit import SolichViewInheritMixin
from solich.inherit.view_registry import VIEW_REGISTRY

__all__ = [
    "SolichViewInheritMixin",
    "SolichModelBase",
    "INJECTION_MAP",
    "EXTENSION_REGISTRY",
    "VIEW_REGISTRY",
]
