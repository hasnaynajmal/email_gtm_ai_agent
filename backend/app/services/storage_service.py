"""
Storage Service - JSON file-based storage for campaigns
"""
import json
import os
from datetime import datetime
from typing import List, Optional, Dict
from pathlib import Path
from agno.utils.log import logger

from app.schemas.outreach import CampaignExecutionResponse


class StorageService:
    """
    Service for storing and retrieving campaign results using JSON files.
    Simple file-based storage without database complexity.
    """

    def __init__(self, storage_dir: str = "data/campaigns"):
        """
        Initialize storage service.
        
        Args:
            storage_dir: Directory to store campaign JSON files
        """
        self.storage_dir = Path(storage_dir)
        self._ensure_storage_dir()

    def _ensure_storage_dir(self):
        """Create storage directory if it doesn't exist"""
        try:
            self.storage_dir.mkdir(parents=True, exist_ok=True)
            logger.info(f"Storage directory ready: {self.storage_dir}")
        except Exception as e:
            logger.error(f"Failed to create storage directory: {e}")
            raise

    def save_campaign(
        self,
        campaign_response: CampaignExecutionResponse,
        campaign_metadata: Optional[Dict] = None
    ) -> str:
        """
        Save campaign results to JSON file.
        
        Args:
            campaign_response: Campaign execution results
            campaign_metadata: Additional metadata (sender, config, etc.)
        
        Returns:
            Campaign ID (filename without extension)
        """
        try:
            # Generate campaign ID from timestamp
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            campaign_id = f"campaign_{timestamp}"
            
            # Prepare data to save
            campaign_data = {
                "campaign_id": campaign_id,
                "timestamp": timestamp,
                "created_at": datetime.now().isoformat(),
                "metadata": campaign_metadata or {},
                "results": campaign_response.model_dump(),
            }
            
            # Save to JSON file
            filepath = self.storage_dir / f"{campaign_id}.json"
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(campaign_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Campaign saved: {campaign_id}")
            logger.info(f"File: {filepath}")
            
            return campaign_id
            
        except Exception as e:
            logger.error(f"Failed to save campaign: {e}")
            raise

    def get_campaign(self, campaign_id: str) -> Optional[Dict]:
        """
        Retrieve campaign by ID.
        
        Args:
            campaign_id: Campaign identifier
        
        Returns:
            Campaign data dictionary or None if not found
        """
        try:
            filepath = self.storage_dir / f"{campaign_id}.json"
            
            if not filepath.exists():
                logger.warning(f"Campaign not found: {campaign_id}")
                return None
            
            with open(filepath, "r", encoding="utf-8") as f:
                campaign_data = json.load(f)
            
            logger.info(f"Campaign loaded: {campaign_id}")
            return campaign_data
            
        except Exception as e:
            logger.error(f"Failed to load campaign {campaign_id}: {e}")
            return None

    def list_campaigns(
        self,
        limit: Optional[int] = None,
        offset: int = 0
    ) -> List[Dict]:
        """
        List all campaigns with optional pagination.
        
        Args:
            limit: Maximum number of campaigns to return
            offset: Number of campaigns to skip
        
        Returns:
            List of campaign summaries (metadata only, no full results)
        """
        try:
            # Get all JSON files
            json_files = sorted(
                self.storage_dir.glob("campaign_*.json"),
                key=lambda p: p.stat().st_mtime,
                reverse=True  # Newest first
            )
            
            # Apply pagination
            if limit:
                json_files = json_files[offset:offset + limit]
            else:
                json_files = json_files[offset:]
            
            campaigns = []
            for filepath in json_files:
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    
                    # Create summary (without full results to save memory)
                    summary = {
                        "campaign_id": data.get("campaign_id"),
                        "timestamp": data.get("timestamp"),
                        "created_at": data.get("created_at"),
                        "metadata": data.get("metadata", {}),
                        "stats": {
                            "total_companies": data.get("results", {}).get("total_companies", 0),
                            "total_contacts": data.get("results", {}).get("total_contacts", 0),
                            "total_emails": data.get("results", {}).get("total_emails", 0),
                            "execution_time": data.get("results", {}).get("execution_time", 0),
                        }
                    }
                    campaigns.append(summary)
                    
                except Exception as e:
                    logger.warning(f"Failed to load campaign summary from {filepath}: {e}")
                    continue
            
            logger.info(f"Listed {len(campaigns)} campaigns")
            return campaigns
            
        except Exception as e:
            logger.error(f"Failed to list campaigns: {e}")
            return []

    def delete_campaign(self, campaign_id: str) -> bool:
        """
        Delete a campaign by ID.
        
        Args:
            campaign_id: Campaign identifier
        
        Returns:
            True if deleted, False if not found or error
        """
        try:
            filepath = self.storage_dir / f"{campaign_id}.json"
            
            if not filepath.exists():
                logger.warning(f"Campaign not found for deletion: {campaign_id}")
                return False
            
            filepath.unlink()
            logger.info(f"Campaign deleted: {campaign_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to delete campaign {campaign_id}: {e}")
            return False

    def get_campaign_count(self) -> int:
        """
        Get total number of saved campaigns.
        
        Returns:
            Total campaign count
        """
        try:
            json_files = list(self.storage_dir.glob("campaign_*.json"))
            count = len(json_files)
            logger.info(f"Total campaigns: {count}")
            return count
        except Exception as e:
            logger.error(f"Failed to count campaigns: {e}")
            return 0

    def export_campaign(self, campaign_id: str, export_path: str) -> bool:
        """
        Export campaign to a specific location.
        
        Args:
            campaign_id: Campaign identifier
            export_path: Destination file path
        
        Returns:
            True if exported successfully
        """
        try:
            campaign_data = self.get_campaign(campaign_id)
            if not campaign_data:
                return False
            
            export_path = Path(export_path)
            export_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(export_path, "w", encoding="utf-8") as f:
                json.dump(campaign_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Campaign exported to: {export_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to export campaign {campaign_id}: {e}")
            return False


# Global storage service instance
_storage_service: Optional[StorageService] = None


def get_storage_service() -> StorageService:
    """
    Get or create the global storage service instance.
    """
    global _storage_service
    if _storage_service is None:
        _storage_service = StorageService()
    return _storage_service
