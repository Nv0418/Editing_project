"""VinVideo-specific extensions for Movis."""

from .agent_connector import EditPlanParser, VinVideoComposition
from .asset_registry import AssetRegistry, AssetItem
from .social_formats import SocialMediaFormat, format_for_platform
from .transitions import SmartTransition, CrossFadeTransition, SlideTransition
from .qc_integration import QCPipeline, QCResult

__all__ = [
    'EditPlanParser',
    'VinVideoComposition', 
    'AssetRegistry',
    'AssetItem',
    'SocialMediaFormat',
    'format_for_platform',
    'SmartTransition',
    'CrossFadeTransition', 
    'SlideTransition',
    'QCPipeline',
    'QCResult'
]
