"""
Workflow Orchestration Service - Coordinates the full outreach campaign
"""
import time
from typing import List, Dict, Iterator, Optional
from agno.utils.log import logger

from app.schemas.outreach import (
    CampaignConfig,
    CampaignResult,
    CampaignExecutionResponse,
    CompanyInfo,
    ContactInfo,
    GeneratedEmail,
)
from app.services.agent_service import get_agent_service
from app.services.company_service import get_company_service
from app.services.research_service import get_research_service
from app.services.contact_service import get_contact_service
from app.services.email_service import get_email_service


class WorkflowOrchestrationService:
    """
    Service for orchestrating the complete B2B outreach workflow.
    Coordinates: company discovery → research → contact finding → email generation
    """

    def __init__(self):
        """Initialize the workflow orchestration service"""
        self.agent_service = get_agent_service()
        self.company_service = get_company_service()
        self.research_service = get_research_service()
        self.contact_service = get_contact_service()
        self.email_service = get_email_service()

    def execute_campaign(
        self,
        campaign_config: CampaignConfig,
    ) -> CampaignExecutionResponse:
        """
        Execute a complete automated outreach campaign.

        Workflow:
        1. Discover target companies
        2. Research each company in depth
        3. Find decision maker contacts
        4. Generate personalized emails

        Args:
            campaign_config: Complete campaign configuration

        Returns:
            CampaignExecutionResponse with all results
        """
        start_time = time.time()
        logger.info("=" * 60)
        logger.info("Starting Automated B2B Outreach Campaign")
        logger.info("=" * 60)
        logger.info(f"Target: {campaign_config.outreach_config.company_category}")
        logger.info(f"Service: {campaign_config.outreach_config.service_type}")
        logger.info(f"Companies: {campaign_config.num_companies}")
        logger.info(f"Sender: {campaign_config.sender_details.name} ({campaign_config.sender_details.organization})")
        logger.info("=" * 60)

        # Validate agents before starting
        if not self.agent_service.validate_agents():
            logger.error("Agent validation failed - cannot proceed")
            raise ValueError("AI agents are not properly configured. Check API keys.")

        campaign_results: List[CampaignResult] = []

        try:
            # Step 1: Discover companies
            logger.info("\n🔍 STEP 1: Discovering Target Companies")
            logger.info("-" * 60)

            companies = self.company_service.discover_companies(
                config=campaign_config.outreach_config,
                num_companies=campaign_config.num_companies,
            )

            logger.info(f"✓ Discovered {len(companies)} companies")

            if not companies:
                logger.warning("No companies discovered - ending campaign")
                return CampaignExecutionResponse(
                    results=[],
                    total_companies=0,
                    total_contacts=0,
                    total_emails=0,
                    execution_time=time.time() - start_time
                )

            # Step 2-5: Process each company
            for idx, company_data in enumerate(companies, 1):
                company_name = company_data.get("company_name", f"Company #{idx}")
                logger.info(f"\n{'=' * 60}")
                logger.info(f"Processing Company {idx}/{len(companies)}: {company_name}")
                logger.info(f"{'=' * 60}")

                try:
                    result = self._process_company(
                        company_data=company_data,
                        campaign_config=campaign_config,
                        company_number=idx,
                        total_companies=len(companies)
                    )

                    if result:
                        campaign_results.append(result)
                        logger.info(f"✓ Successfully processed {company_name}")
                    else:
                        logger.warning(f"✗ Failed to process {company_name}")

                except Exception as e:
                    logger.error(f"✗ Error processing {company_name}: {e}")
                    continue

            # Calculate statistics
            execution_time = time.time() - start_time
            total_contacts = sum(len(r.contacts) for r in campaign_results)
            total_emails = sum(len(r.generated_emails) for r in campaign_results)

            logger.info("\n" + "=" * 60)
            logger.info("Campaign Execution Complete!")
            logger.info("=" * 60)
            logger.info(f"Companies Processed: {len(campaign_results)}/{len(companies)}")
            logger.info(f"Total Contacts Found: {total_contacts}")
            logger.info(f"Total Emails Generated: {total_emails}")
            logger.info(f"Execution Time: {execution_time:.2f} seconds")
            logger.info("=" * 60)

            return CampaignExecutionResponse(
                results=campaign_results,
                total_companies=len(campaign_results),
                total_contacts=total_contacts,
                total_emails=total_emails,
                execution_time=execution_time
            )

        except Exception as e:
            logger.error(f"Campaign execution failed: {e}")
            raise

    def _process_company(
        self,
        company_data: Dict,
        campaign_config: CampaignConfig,
        company_number: int,
        total_companies: int
    ) -> Optional[CampaignResult]:
        """
        Process a single company through the complete workflow.

        Args:
            company_data: Company information from discovery
            campaign_config: Campaign configuration
            company_number: Current company index
            total_companies: Total number of companies

        Returns:
            CampaignResult or None if processing failed
        """
        company_name = company_data.get("company_name", "Unknown")

        try:
            # Step 2: Research company
            logger.info(f"\n🔬 STEP 2: Researching {company_name}")
            logger.info("-" * 60)

            company_info = self.research_service.research_company(
                company_data=company_data,
                config=campaign_config.outreach_config,
            )

            logger.info(f"✓ Research complete for {company_name}")
            self._log_research_summary(company_info)

            # Step 3: Find contacts
            logger.info(f"\n👥 STEP 3: Finding Decision Makers at {company_name}")
            logger.info("-" * 60)

            contacts = self.contact_service.find_contacts(
                company_data=company_data,
                config=campaign_config.outreach_config,
            )

            if not contacts:
                logger.warning(f"No contacts found for {company_name} - skipping email generation")
                # Still return result with company info
                return CampaignResult(
                    company_info=company_info,
                    contacts=[],
                    generated_emails=[],
                    research_summary=self._create_research_summary(company_info)
                )

            logger.info(f"✓ Found {len(contacts)} contacts at {company_name}")
            for contact in contacts:
                logger.info(f"  - {contact.name} ({contact.title})")

            # Step 4: Generate emails
            logger.info(f"\n✉️ STEP 4: Generating Personalized Emails")
            logger.info("-" * 60)

            generated_emails = []
            for contact in contacts:
                try:
                    logger.info(f"Generating email for {contact.name}...")

                    email = self.email_service.generate_email(
                        company_info=company_info,
                        contacts=[contact],  # Primary contact
                        sender_details=campaign_config.sender_details,
                        config=campaign_config.outreach_config,
                    )

                    generated_emails.append(email)
                    logger.info(f"✓ Email generated for {contact.name}")
                    logger.info(f"  Subject: {email.subject}")

                except Exception as e:
                    logger.error(f"Failed to generate email for {contact.name}: {e}")
                    continue

            if not generated_emails:
                logger.warning(f"No emails generated for {company_name}")

            logger.info(f"✓ Generated {len(generated_emails)} emails for {company_name}")

            # Create campaign result
            return CampaignResult(
                company_info=company_info,
                contacts=contacts,
                generated_emails=generated_emails,
                research_summary=self._create_research_summary(company_info)
            )

        except Exception as e:
            logger.error(f"Error processing company {company_name}: {e}")
            return None

    def _log_research_summary(self, company_info: CompanyInfo):
        """Log a summary of company research"""
        logger.info(f"  Industry: {company_info.industry or 'N/A'}")
        logger.info(f"  Size: {company_info.company_size or 'N/A'}")

        if company_info.recent_news:
            logger.info(f"  Recent News: {len(company_info.recent_news)} items found")

        if company_info.challenges:
            logger.info(f"  Challenges Identified: {len(company_info.challenges)}")

        if company_info.growth_areas:
            logger.info(f"  Growth Opportunities: {len(company_info.growth_areas)}")

    def _create_research_summary(self, company_info: CompanyInfo) -> str:
        """
        Create a text summary of company research.

        Args:
            company_info: Company information

        Returns:
            Summary string
        """
        summary_parts = [
            f"Company: {company_info.company_name}",
            f"Industry: {company_info.industry or 'N/A'}",
            f"Size: {company_info.company_size or 'N/A'}",
        ]

        if company_info.core_business:
            summary_parts.append(f"Business: {company_info.core_business}")

        if company_info.recent_news:
            summary_parts.append(f"\nRecent News ({len(company_info.recent_news)} items):")
            for news in company_info.recent_news[:3]:
                summary_parts.append(f"  - {news}")

        if company_info.challenges:
            summary_parts.append(f"\nChallenges ({len(company_info.challenges)}):")
            for challenge in company_info.challenges[:3]:
                summary_parts.append(f"  - {challenge}")

        if company_info.growth_areas:
            summary_parts.append(f"\nGrowth Opportunities ({len(company_info.growth_areas)}):")
            for growth in company_info.growth_areas[:3]:
                summary_parts.append(f"  - {growth}")

        return "\n".join(summary_parts)

    def execute_campaign_streaming(
        self,
        campaign_config: CampaignConfig,
    ) -> Iterator[Dict]:
        """
        Execute campaign with streaming progress updates (for real-time UI).

        Yields progress updates as the campaign executes.

        Args:
            campaign_config: Campaign configuration

        Yields:
            Progress update dictionaries
        """
        start_time = time.time()
        logger.info("Starting streaming campaign execution")

        yield {
            "status": "starting",
            "message": "Initializing campaign...",
            "progress": 0.0
        }

        # Validate agents
        if not self.agent_service.validate_agents():
            yield {
                "status": "error",
                "message": "AI agents validation failed",
                "progress": 0.0
            }
            return

        try:
            # Discover companies
            yield {
                "status": "discovering",
                "message": "Discovering target companies...",
                "progress": 0.1
            }

            companies = self.company_service.discover_companies(
                config=campaign_config.outreach_config,
                num_companies=campaign_config.num_companies,
            )

            yield {
                "status": "discovered",
                "message": f"Found {len(companies)} companies",
                "progress": 0.2,
                "companies_found": len(companies)
            }

            if not companies:
                yield {
                    "status": "completed",
                    "message": "No companies found",
                    "progress": 1.0,
                    "results": []
                }
                return

            # Process each company
            results = []
            for idx, company_data in enumerate(companies, 1):
                company_name = company_data.get("company_name", f"Company #{idx}")

                # Research
                yield {
                    "status": "processing",
                    "message": f"Researching {company_name}...",
                    "progress": 0.2 + (idx - 1) / len(companies) * 0.6,
                    "current_company": company_name,
                    "company_number": idx,
                    "total_companies": len(companies)
                }

                result = self._process_company(
                    company_data=company_data,
                    campaign_config=campaign_config,
                    company_number=idx,
                    total_companies=len(companies)
                )

                if result:
                    results.append(result)

                    yield {
                        "status": "completed_company",
                        "message": f"Completed {company_name}",
                        "progress": 0.2 + idx / len(companies) * 0.6,
                        "company_name": company_name,
                        "contacts_found": len(result.contacts),
                        "emails_generated": len(result.generated_emails)
                    }

            # Final results
            execution_time = time.time() - start_time
            total_contacts = sum(len(r.contacts) for r in results)
            total_emails = sum(len(r.generated_emails) for r in results)

            yield {
                "status": "completed",
                "message": "Campaign completed successfully",
                "progress": 1.0,
                "results": results,
                "total_companies": len(results),
                "total_contacts": total_contacts,
                "total_emails": total_emails,
                "execution_time": execution_time
            }

        except Exception as e:
            logger.error(f"Streaming campaign failed: {e}")
            yield {
                "status": "error",
                "message": f"Campaign failed: {str(e)}",
                "progress": 0.0
            }


# Service instance helper
def get_workflow_service() -> WorkflowOrchestrationService:
    """Get a workflow orchestration service instance"""
    return WorkflowOrchestrationService()
