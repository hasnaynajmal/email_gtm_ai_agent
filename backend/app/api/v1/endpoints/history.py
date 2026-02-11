"""
Campaign History Endpoints
"""
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query
from agno.utils.log import logger

from app.services.storage_service import get_storage_service

router = APIRouter(prefix="/campaigns", tags=["Campaign History"])


@router.get("/history")
async def get_campaign_history(
    limit: int = Query(default=10, ge=1, le=100, description="Number of campaigns to return"),
    offset: int = Query(default=0, ge=0, description="Number of campaigns to skip"),
):
    """
    Get campaign history with pagination.
    
    Returns a list of campaign summaries (without full results) sorted by newest first.
    Use this to show users their past campaigns.
    
    Args:
        limit: Maximum number of campaigns to return (1-100, default 10)
        offset: Number of campaigns to skip for pagination (default 0)
    
    Returns:
        List of campaign summaries with metadata and statistics
    """
    try:
        logger.info(f"Fetching campaign history (limit={limit}, offset={offset})")
        
        storage_service = get_storage_service()
        campaigns = storage_service.list_campaigns(limit=limit, offset=offset)
        total_count = storage_service.get_campaign_count()
        
        logger.info(f"Retrieved {len(campaigns)} campaigns (total: {total_count})")
        
        return {
            "campaigns": campaigns,
            "total": total_count,
            "limit": limit,
            "offset": offset,
            "has_more": (offset + len(campaigns)) < total_count
        }
        
    except Exception as e:
        logger.error(f"Failed to fetch campaign history: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch campaign history: {str(e)}")


@router.get("/{campaign_id}")
async def get_campaign_details(campaign_id: str):
    """
    Get full details of a specific campaign by ID.
    
    Returns complete campaign data including all results, contacts, and generated emails.
    
    Args:
        campaign_id: Campaign identifier (e.g., "campaign_2026-02-11_12-30-45")
    
    Returns:
        Complete campaign data with all results
    """
    try:
        logger.info(f"Fetching campaign details: {campaign_id}")
        
        storage_service = get_storage_service()
        campaign_data = storage_service.get_campaign(campaign_id)
        
        if not campaign_data:
            logger.warning(f"Campaign not found: {campaign_id}")
            raise HTTPException(status_code=404, detail=f"Campaign not found: {campaign_id}")
        
        logger.info(f"Campaign retrieved: {campaign_id}")
        return campaign_data
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to fetch campaign {campaign_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch campaign: {str(e)}")


@router.delete("/{campaign_id}")
async def delete_campaign(campaign_id: str):
    """
    Delete a campaign by ID.
    
    Permanently removes the campaign JSON file from storage.
    
    Args:
        campaign_id: Campaign identifier to delete
    
    Returns:
        Deletion confirmation
    """
    try:
        logger.info(f"Deleting campaign: {campaign_id}")
        
        storage_service = get_storage_service()
        success = storage_service.delete_campaign(campaign_id)
        
        if not success:
            raise HTTPException(status_code=404, detail=f"Campaign not found: {campaign_id}")
        
        logger.info(f"Campaign deleted successfully: {campaign_id}")
        return {
            "success": True,
            "message": f"Campaign {campaign_id} deleted successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to delete campaign {campaign_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to delete campaign: {str(e)}")


@router.get("/{campaign_id}/export")
async def export_campaign(campaign_id: str):
    """
    Export campaign data as downloadable JSON.
    
    Returns the campaign data in a format suitable for download/sharing.
    
    Args:
        campaign_id: Campaign identifier to export
    
    Returns:
        Campaign data as JSON
    """
    try:
        logger.info(f"Exporting campaign: {campaign_id}")
        
        storage_service = get_storage_service()
        campaign_data = storage_service.get_campaign(campaign_id)
        
        if not campaign_data:
            raise HTTPException(status_code=404, detail=f"Campaign not found: {campaign_id}")
        
        logger.info(f"Campaign exported: {campaign_id}")
        return campaign_data
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to export campaign {campaign_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to export campaign: {str(e)}")


@router.get("/stats/summary")
async def get_campaigns_summary():
    """
    Get summary statistics across all campaigns.
    
    Returns aggregate statistics for all stored campaigns.
    
    Returns:
        Summary statistics (total campaigns, avg emails per campaign, etc.)
    """
    try:
        logger.info("Fetching campaign statistics")
        
        storage_service = get_storage_service()
        campaigns = storage_service.list_campaigns()
        
        if not campaigns:
            return {
                "total_campaigns": 0,
                "total_companies_processed": 0,
                "total_contacts_found": 0,
                "total_emails_generated": 0,
                "avg_companies_per_campaign": 0,
                "avg_emails_per_campaign": 0,
            }
        
        # Calculate statistics
        total_companies = sum(c["stats"]["total_companies"] for c in campaigns)
        total_contacts = sum(c["stats"]["total_contacts"] for c in campaigns)
        total_emails = sum(c["stats"]["total_emails"] for c in campaigns)
        
        stats = {
            "total_campaigns": len(campaigns),
            "total_companies_processed": total_companies,
            "total_contacts_found": total_contacts,
            "total_emails_generated": total_emails,
            "avg_companies_per_campaign": round(total_companies / len(campaigns), 2) if campaigns else 0,
            "avg_emails_per_campaign": round(total_emails / len(campaigns), 2) if campaigns else 0,
        }
        
        logger.info(f"Campaign statistics: {stats}")
        return stats
        
    except Exception as e:
        logger.error(f"Failed to fetch campaign statistics: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch statistics: {str(e)}")
