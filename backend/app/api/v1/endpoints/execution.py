"""
Campaign Execution Endpoints
"""
from typing import List, Dict
from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import StreamingResponse
import json
from agno.utils.log import logger

from app.schemas.outreach import (
    CampaignConfig,
    CampaignExecutionResponse,
    EmailGenerationRequest,
    EmailGenerationResponse,
    OutreachConfig,
)
from app.services.workflow_service import get_workflow_service
from app.services.company_service import get_company_service
from app.services.email_service import get_email_service
from app.services.storage_service import get_storage_service

router = APIRouter(prefix="/execute", tags=["Campaign Execution"])


@router.post("/campaign", response_model=CampaignExecutionResponse)
async def execute_campaign(campaign_config: CampaignConfig):
    """
    Execute a complete automated outreach campaign.
    
    Workflow:
    1. Discovers target companies based on criteria
    2. Researches each company in depth
    3. Finds decision maker contacts
    4. Generates personalized emails for each contact
    
    This is a synchronous endpoint that returns results after the entire campaign completes.
    For large campaigns, consider using the streaming endpoint.
    
    Args:
        campaign_config: Complete campaign configuration including:
            - Outreach configuration (targeting, personalization)
            - Sender details
            - Number of companies to target
    
    Returns:
        CampaignExecutionResponse with all generated emails and statistics
    """
    try:
        logger.info("=" * 60)
        logger.info("Starting Campaign Execution via API")
        logger.info("=" * 60)
        logger.info(f"Requester: {campaign_config.sender_details.name}")
        logger.info(f"Organization: {campaign_config.sender_details.organization}")
        logger.info(f"Target Category: {campaign_config.outreach_config.company_category}")
        logger.info(f"Service Type: {campaign_config.outreach_config.service_type}")
        logger.info(f"Companies: {campaign_config.num_companies}")
        
        # Get workflow service
        workflow_service = get_workflow_service()
        
        # Execute campaign
        result = workflow_service.execute_campaign(campaign_config)
        
        # Save campaign to storage
        try:
            storage_service = get_storage_service()
            campaign_metadata = {
                "sender_name": campaign_config.sender_details.name,
                "organization": campaign_config.sender_details.organization,
                "company_category": campaign_config.outreach_config.company_category,
                "service_type": campaign_config.outreach_config.service_type,
                "num_companies_requested": campaign_config.num_companies,
            }
            campaign_id = storage_service.save_campaign(result, campaign_metadata)
            result.campaign_id = campaign_id
            logger.info(f"Campaign saved with ID: {campaign_id}")
        except Exception as e:
            logger.warning(f"Failed to save campaign to storage: {e}")
            # Don't fail the whole request if storage fails
        
        logger.info("Campaign execution completed via API")
        logger.info(f"Results: {result.total_companies} companies, {result.total_emails} emails")
        
        return result
        
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Campaign execution failed: {e}")
        raise HTTPException(status_code=500, detail=f"Campaign execution failed: {str(e)}")


@router.post("/campaign/stream")
async def execute_campaign_streaming(campaign_config: CampaignConfig):
    """
    Execute campaign with real-time streaming progress updates.
    
    Returns Server-Sent Events (SSE) stream with progress updates as the campaign executes.
    Useful for providing real-time feedback to users during long-running campaigns.
    
    Progress updates include:
    - Current step (discovering, researching, generating)
    - Current company being processed
    - Progress percentage (0.0 to 1.0)
    - Partial results as they become available
    
    Response format: JSON objects separated by newlines (NDJSON)
    """
    async def event_generator():
        """Generate SSE events for campaign progress"""
        try:
            workflow_service = get_workflow_service()
            
            for update in workflow_service.execute_campaign_streaming(campaign_config):
                # Convert update to JSON and send as SSE
                yield f"data: {json.dumps(update)}\n\n"
                
        except Exception as e:
            logger.error(f"Streaming campaign failed: {e}")
            yield f"data: {json.dumps({'status': 'error', 'message': str(e)})}\n\n"
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )


@router.post("/companies/discover")
async def discover_companies(
    outreach_config: OutreachConfig,
    num_companies: int = 5
):
    """
    Discover target companies only (without full campaign execution).
    
    Useful for:
    - Previewing potential targets before committing to full campaign
    - Building a prospect list for later use
    - Testing company discovery with different criteria
    
    Args:
        outreach_config: Targeting criteria and preferences
        num_companies: Number of companies to discover (1-20)
    
    Returns:
        List of discovered companies with basic information
    """
    try:
        if num_companies < 1 or num_companies > 20:
            raise HTTPException(
                status_code=400,
                detail="num_companies must be between 1 and 20"
            )
        
        logger.info(f"Discovering {num_companies} companies via API")
        logger.info(f"Category: {outreach_config.company_category}")
        
        # Get company service
        company_service = get_company_service()
        
        # Discover companies
        companies = company_service.discover_companies(
            config=outreach_config,
            num_companies=num_companies
        )
        
        logger.info(f"Discovered {len(companies)} companies")
        
        return {
            "status": "success",
            "companies_found": len(companies),
            "companies": companies,
            "config": {
                "category": outreach_config.company_category,
                "service_type": outreach_config.service_type,
                "company_size": outreach_config.company_size_preference,
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Company discovery failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Company discovery failed: {str(e)}"
        )


@router.post("/email/generate", response_model=EmailGenerationResponse)
async def generate_single_email(request: EmailGenerationRequest):
    """
    Generate a single personalized email for a specific company and contact.
    
    Useful for:
    - Generating emails for manually researched companies
    - Re-generating emails with different personalization
    - Testing email generation quality
    
    Args:
        request: Email generation request with:
            - Company information
            - Contact information
            - Sender details
            - Outreach configuration
    
    Returns:
        EmailGenerationResponse with generated email
    """
    try:
        logger.info(f"Generating single email for: {request.company_info.company_name}")
        logger.info(f"Contact: {request.contact_info.name}")
        
        # Get email service
        email_service = get_email_service()
        
        # Generate email
        generated_email = email_service.generate_email(
            company_info=request.company_info,
            contacts=[request.contact_info],
            sender_details=request.sender_details,
            config=request.outreach_config,
        )
        
        logger.info("Email generated successfully")
        logger.info(f"Subject: {generated_email.subject}")
        
        return EmailGenerationResponse(
            email=generated_email,
            company_info=request.company_info,
            contact_info=request.contact_info,
        )
        
    except Exception as e:
        logger.error(f"Email generation failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Email generation failed: {str(e)}"
        )


@router.get("/health")
async def execution_health_check():
    """
    Check if campaign execution services are operational.
    
    Validates:
    - AI agents are configured
    - API keys are available
    - Services can be initialized
    
    Returns health status and any configuration issues.
    """
    try:
        from app.services.agent_service import get_agent_service
        
        agent_service = get_agent_service()
        agents_valid = agent_service.validate_agents()
        
        health_status = {
            "status": "healthy" if agents_valid else "degraded",
            "agents_configured": agents_valid,
            "exa_api_configured": bool(agent_service.exa_api_key),
            "openai_api_configured": bool(agent_service.openai_api_key),
            "openai_model": agent_service.openai_model,
        }
        
        if not agents_valid:
            health_status["warnings"] = []
            if not agent_service.exa_api_key:
                health_status["warnings"].append("EXA_API_KEY not configured")
            if not agent_service.openai_api_key:
                health_status["warnings"].append("OPENAI_API_KEY not configured")
        
        return health_status
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            "status": "unhealthy",
            "error": str(e)
        }
