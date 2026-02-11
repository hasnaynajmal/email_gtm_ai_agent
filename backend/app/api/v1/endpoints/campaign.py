"""
Campaign Configuration Endpoints
"""
from typing import List, Dict
from fastapi import APIRouter, HTTPException
from agno.utils.log import logger

from app.schemas.outreach import (
    CampaignConfig,
    CampaignOptionsResponse,
    OutreachConfig,
)
from app.core.constants import (
    COMPANY_CATEGORIES,
    SERVICE_TYPES,
    COMPANY_SIZES,
    PERSONALIZATION_LEVELS,
    TARGET_DEPARTMENTS,
)
from app.services.agent_service import get_agent_service

router = APIRouter(prefix="/campaign", tags=["Campaign Configuration"])


@router.get("/options", response_model=CampaignOptionsResponse)
async def get_campaign_options():
    """
    Get all available options for campaign configuration.
    
    Returns:
    - Company categories with descriptions and typical roles
    - Available service types
    - Company size options
    - Personalization levels
    - Target departments
    
    Use this endpoint to populate dropdown menus and selection options in the UI.
    """
    try:
        logger.info("Fetching campaign configuration options")
        
        return CampaignOptionsResponse(
            company_categories=COMPANY_CATEGORIES,
            service_types=SERVICE_TYPES,
            company_sizes=COMPANY_SIZES,
            personalization_levels=PERSONALIZATION_LEVELS,
            target_departments=TARGET_DEPARTMENTS,
        )
    except Exception as e:
        logger.error(f"Error fetching campaign options: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/configure")
async def validate_campaign_config(campaign_config: CampaignConfig):
    """
    Validate campaign configuration before execution.
    
    Validates:
    - Outreach configuration parameters
    - Sender details completeness
    - Number of companies is within acceptable range
    - API keys are configured
    
    Returns validation status and any warnings/errors.
    """
    try:
        logger.info("Validating campaign configuration")
        logger.info(f"Category: {campaign_config.outreach_config.company_category}")
        logger.info(f"Service Type: {campaign_config.outreach_config.service_type}")
        logger.info(f"Num Companies: {campaign_config.num_companies}")
        
        validation_result = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "config_summary": {
                "company_category": campaign_config.outreach_config.company_category,
                "service_type": campaign_config.outreach_config.service_type,
                "target_departments": campaign_config.outreach_config.target_departments,
                "company_size": campaign_config.outreach_config.company_size_preference,
                "personalization_level": campaign_config.outreach_config.personalization_level,
                "num_companies": campaign_config.num_companies,
                "sender": campaign_config.sender_details.name,
                "organization": campaign_config.sender_details.organization,
            }
        }
        
        # Validate company category
        if campaign_config.outreach_config.company_category not in COMPANY_CATEGORIES:
            validation_result["errors"].append(
                f"Invalid company category: {campaign_config.outreach_config.company_category}"
            )
            validation_result["valid"] = False
        
        # Validate service type
        if campaign_config.outreach_config.service_type not in SERVICE_TYPES:
            validation_result["errors"].append(
                f"Invalid service type: {campaign_config.outreach_config.service_type}"
            )
            validation_result["valid"] = False
        
        # Validate target departments
        if not campaign_config.outreach_config.target_departments:
            validation_result["errors"].append("At least one target department is required")
            validation_result["valid"] = False
        
        for dept in campaign_config.outreach_config.target_departments:
            if dept not in TARGET_DEPARTMENTS:
                validation_result["warnings"].append(
                    f"Unknown department: {dept}"
                )
        
        # Validate number of companies
        if campaign_config.num_companies < 1 or campaign_config.num_companies > 20:
            validation_result["errors"].append(
                "Number of companies must be between 1 and 20"
            )
            validation_result["valid"] = False
        
        # Validate sender details
        if not campaign_config.sender_details.name:
            validation_result["errors"].append("Sender name is required")
            validation_result["valid"] = False
        
        if not campaign_config.sender_details.email:
            validation_result["errors"].append("Sender email is required")
            validation_result["valid"] = False
        
        if not campaign_config.sender_details.organization:
            validation_result["errors"].append("Organization name is required")
            validation_result["valid"] = False
        
        if not campaign_config.sender_details.service_offered:
            validation_result["errors"].append("Service description is required")
            validation_result["valid"] = False
        
        # Validate API keys
        agent_service = get_agent_service()
        if not agent_service.exa_api_key:
            validation_result["errors"].append(
                "EXA_API_KEY not configured - required for company discovery"
            )
            validation_result["valid"] = False
        
        if not agent_service.openai_api_key:
            validation_result["errors"].append(
                "OPENAI_API_KEY not configured - required for AI generation"
            )
            validation_result["valid"] = False
        
        # Add warnings
        if not campaign_config.sender_details.calendar_link:
            validation_result["warnings"].append(
                "Calendar link not provided - emails will lack booking link"
            )
        
        if campaign_config.num_companies > 10:
            validation_result["warnings"].append(
                f"Processing {campaign_config.num_companies} companies may take significant time"
            )
        
        logger.info(f"Validation result: {validation_result['valid']}")
        if validation_result["errors"]:
            logger.warning(f"Validation errors: {validation_result['errors']}")
        
        return validation_result
        
    except Exception as e:
        logger.error(f"Error validating campaign config: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/departments")
async def get_target_departments():
    """
    Get list of available target departments.
    
    Returns a simple list of department names that can be targeted.
    """
    return {
        "departments": TARGET_DEPARTMENTS,
        "count": len(TARGET_DEPARTMENTS)
    }


@router.get("/categories")
async def get_company_categories():
    """
    Get detailed information about company categories.
    
    Returns company categories with descriptions and typical roles for each.
    """
    return {
        "categories": COMPANY_CATEGORIES,
        "count": len(COMPANY_CATEGORIES)
    }


@router.get("/service-types")
async def get_service_types():
    """
    Get list of available service types.
    
    Returns service types that can be offered in outreach campaigns.
    """
    return {
        "service_types": SERVICE_TYPES,
        "count": len(SERVICE_TYPES)
    }
