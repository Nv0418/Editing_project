"""
Asset Registry for VinVideo

Manages tracking of all generated assets (images, videos, audio) with their
original prompts and generation metadata for regeneration capabilities.
"""

from __future__ import annotations

import json
import uuid
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class AssetItem:
    """Represents a single asset in the registry."""
    asset_id: str
    asset_type: str  # 'image', 'video', 'audio'
    file_path: str
    original_prompt: str
    generator_model: str  # 'flux', 'wan_ltx', 'parakeet', etc.
    generation_params: Dict[str, Any]
    created_at: str
    quality_score: Optional[float] = None
    regeneration_count: int = 0
    status: str = 'active'  # 'active', 'flagged', 'replaced'


class AssetRegistry:
    """Central registry for all VinVideo generated assets."""
    
    def __init__(self, registry_path: Optional[Path] = None):
        self.registry_path = registry_path or Path("vinvideo_assets.json")
        self._assets: Dict[str, AssetItem] = {}
        self._load_registry()
    
    def _load_registry(self):
        """Load existing registry from disk."""
        if self.registry_path.exists():
            try:
                with open(self.registry_path, 'r') as f:
                    data = json.load(f)
                    self._assets = {
                        asset_id: AssetItem(**asset_data)
                        for asset_id, asset_data in data.items()
                    }
            except Exception as e:
                print(f"Warning: Could not load asset registry: {e}")
                self._assets = {}
    
    def _save_registry(self):
        """Save registry to disk."""
        try:
            with open(self.registry_path, 'w') as f:
                json.dump(
                    {asset_id: asdict(asset) for asset_id, asset in self._assets.items()},
                    f, indent=2
                )
        except Exception as e:
            print(f"Warning: Could not save asset registry: {e}")
    
    def register_asset(
        self,
        file_path: str | Path,
        asset_type: str,
        original_prompt: str,
        generator_model: str,
        generation_params: Dict[str, Any],
        asset_id: Optional[str] = None
    ) -> str:
        """Register a new asset in the registry."""
        if asset_id is None:
            asset_id = f"{asset_type.upper()}-{uuid.uuid4().hex[:8]}"
        
        asset = AssetItem(
            asset_id=asset_id,
            asset_type=asset_type,
            file_path=str(file_path),
            original_prompt=original_prompt,
            generator_model=generator_model,
            generation_params=generation_params,
            created_at=datetime.now().isoformat(),
            regeneration_count=0,
            status='active'
        )
        
        self._assets[asset_id] = asset
        self._save_registry()
        return asset_id
    
    def get_asset(self, asset_id: str) -> Optional[AssetItem]:
        """Get asset by ID."""
        return self._assets.get(asset_id)
    
    def get_asset_path(self, asset_id: str) -> Optional[Path]:
        """Get file path for asset."""
        asset = self.get_asset(asset_id)
        if asset and asset.status == 'active':
            return Path(asset.file_path)
        return None
    
    def flag_asset_for_regeneration(self, asset_id: str, reason: str = "quality_issue"):
        """Mark asset as needing regeneration."""
        if asset_id in self._assets:
            self._assets[asset_id].status = 'flagged'
            self._assets[asset_id].generation_params['regeneration_reason'] = reason
            self._save_registry()
    
    def update_quality_score(self, asset_id: str, score: float):
        """Update quality score for asset."""
        if asset_id in self._assets:
            self._assets[asset_id].quality_score = score
            self._save_registry()
    
    def get_flagged_assets(self) -> List[AssetItem]:
        """Get all assets flagged for regeneration."""
        return [asset for asset in self._assets.values() if asset.status == 'flagged']
