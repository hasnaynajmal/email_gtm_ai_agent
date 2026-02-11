"""
Research Service - Deep company intelligence gathering
"""
from typing import Dict, Optional, List
from agno.utils.log import logger

from app.schemas.outreach import CompanyInfo, OutreachConfig
from app.services.agent_service import get_agent_service
from app.core.constants import RESEARCH_DEPTH


class CompanyResearchService:
    """
    Service for conducting deep research on target companies.
    Uses AI agent to gather comprehensive company intelligence for personalization.
    """

    def __init__(self):
        """Initialize the research service"""
        self.agent_service = get_agent_service()

    def research_company(
        self,
        company_data: Dict,
        config: OutreachConfig,
    ) -> CompanyInfo:
        """
        Research a company in depth for email personalization.

        Args:
            company_data: Basic company information from discovery
            config: Outreach configuration with personalization level

        Returns:
            CompanyInfo object with comprehensive company data
        """
        company_name = company_data.get("company_name", "Unknown")
        logger.info(f"Starting deep research for: {company_name}")
        logger.info(f"Personalization level: {config.personalization_level}")

        # Build research query based on personalization level
        research_query = self._build_research_query(company_data, config)

        try:
            logger.info("Running company researcher agent...")
            response = self.agent_service.company_researcher.run(research_query)

            if not response or not response.content:
                logger.warning(f"No research data returned for {company_name}")
                return self._create_basic_company_info(company_data)

            logger.info(f"Research completed for {company_name}")
            logger.debug(f"Response length: {len(response.content)} characters")

            # Parse research response into CompanyInfo
            company_info = self._parse_research_response(
                response.content,
                company_data,
                config
            )

            return company_info

        except Exception as e:
            logger.error(f"Error researching company {company_name}: {e}")
            # Return basic info on error
            return self._create_basic_company_info(company_data)

    def _build_research_query(self, company_data: Dict, config: OutreachConfig) -> str:
        """
        Build a research query based on personalization level.

        Args:
            company_data: Basic company information
            config: Outreach configuration

        Returns:
            Formatted research query string
        """
        company_name = company_data.get("company_name", "Unknown Company")
        website = company_data.get("website_url", "")

        # Get research requirements for this personalization level
        research_level = RESEARCH_DEPTH.get(
            config.personalization_level,
            RESEARCH_DEPTH["Deep"]
        )

        base_query = f"""
Research the following company in depth for B2B outreach personalization:

Company Name: {company_name}
Website: {website}
Industry: {company_data.get('industry', 'Unknown')}
Current Info: {company_data.get('description', 'N/A')}

Personalization Level: {config.personalization_level}
Target Departments: {', '.join(config.target_departments)}
Service Offering: {config.service_type}
"""

        # Add specific research focuses based on personalization level
        if config.personalization_level == "Deep":
            base_query += """
Research Focus (Deep Personalization):
1. Recent company news, announcements, and press releases (last 3-6 months)
2. Product/service offerings and key features
3. Technology stack and integrations
4. Recent achievements, awards, or milestones
5. Known challenges or pain points in their industry
6. Growth indicators (funding, hiring, expansion)
7. Notable customers or case studies
8. Competitive positioning and unique selling points
9. Company culture and values
10. Blog topics and content focus areas

Identify specific opportunities where our {config.service_type} could help them.
"""
        elif config.personalization_level == "Medium":
            base_query += """
Research Focus (Medium Personalization):
1. Recent company news or major announcements
2. Core business focus and offerings
3. Company size and growth stage
4. Recent achievements or notable developments
5. General pain points in their industry

Provide enough detail for meaningful personalization.
"""
        else:  # Basic
            base_query += """
Research Focus (Basic Personalization):
1. Company industry and business model
2. Main products/services
3. Company size

Provide essential information for basic personalization.
"""

        base_query += """
Format your response with clear sections and bullet points for easy parsing.
Focus on actionable insights that can be used in cold email outreach.
"""

        return base_query

    def _parse_research_response(
        self,
        response_text: str,
        company_data: Dict,
        config: OutreachConfig
    ) -> CompanyInfo:
        """
        Parse the research response into a CompanyInfo object.

        Args:
            response_text: Raw research response from agent
            company_data: Basic company data
            config: Outreach configuration

        Returns:
            CompanyInfo object with parsed research data
        """
        # Start with basic info from discovery
        company_info_dict = {
            "company_name": company_data.get("company_name", "Unknown"),
            "website_url": company_data.get("website_url", ""),
            "industry": company_data.get("industry"),
            "core_business": company_data.get("description"),
            "company_size": company_data.get("company_size"),
            "location": company_data.get("location"),
        }

        # Parse additional fields from research response
        try:
            # Extract specific sections from research
            company_info_dict.update({
                "recent_news": self._extract_list_field(response_text, ["recent news", "announcements", "press releases"]),
                "key_features": self._extract_list_field(response_text, ["features", "offerings", "products"]),
                "technologies": self._extract_list_field(response_text, ["technology", "tech stack", "tools"]),
                "challenges": self._extract_list_field(response_text, ["challenges", "pain points", "problems"]),
                "growth_areas": self._extract_list_field(response_text, ["growth", "opportunities", "expansion"]),
                "customers": self._extract_list_field(response_text, ["customers", "clients", "case studies"]),
                "awards": self._extract_list_field(response_text, ["awards", "recognition", "achievements"]),
                "competitors": self._extract_list_field(response_text, ["competitors", "competition"]),
                "unique_selling_points": self._extract_list_field(response_text, ["unique", "differentiators", "usp"]),
                "value_proposition": self._extract_single_field(response_text, ["value proposition", "mission", "tagline"]),
                "market_position": self._extract_single_field(response_text, ["market position", "positioning"]),
                "funding_status": self._extract_single_field(response_text, ["funding", "investment", "series"]),
            })

        except Exception as e:
            logger.warning(f"Error parsing some research fields: {e}")

        # Create CompanyInfo object
        return CompanyInfo(**company_info_dict)

    def _extract_list_field(self, text: str, keywords: List[str]) -> Optional[List[str]]:
        """
        Extract a list of items from text based on keywords.

        Args:
            text: Text to search in
            keywords: List of possible section names

        Returns:
            List of extracted items or None
        """
        text_lower = text.lower()
        items = []

        for keyword in keywords:
            if keyword in text_lower:
                # Find the section
                start_idx = text_lower.find(keyword)
                # Get text after keyword until next section or end
                section_text = text[start_idx:start_idx + 500]  # Get next 500 chars

                # Extract bullet points or numbered items
                lines = section_text.split("\n")
                for line in lines[1:]:  # Skip header line
                    line = line.strip()
                    if line.startswith("-") or line.startswith("•") or line.startswith("*"):
                        item = line.lstrip("-•*").strip()
                        if item:
                            items.append(item)
                    elif line and line[0].isdigit() and ("." in line or ")" in line):
                        # Numbered list
                        item = line.split(".", 1)[-1].split(")", 1)[-1].strip()
                        if item:
                            items.append(item)

                if items:
                    break

        return items if items else None

    def _extract_single_field(self, text: str, keywords: List[str]) -> Optional[str]:
        """
        Extract a single field value from text based on keywords.

        Args:
            text: Text to search in
            keywords: List of possible field names

        Returns:
            Extracted field value or None
        """
        text_lower = text.lower()

        for keyword in keywords:
            if keyword in text_lower:
                start_idx = text_lower.find(keyword)
                # Get text after keyword
                section_text = text[start_idx:start_idx + 300]
                lines = section_text.split("\n")

                # First line might have the value
                if ":" in lines[0]:
                    value = lines[0].split(":", 1)[1].strip()
                    if value:
                        return value

                # Or it might be in the next line
                if len(lines) > 1:
                    value = lines[1].strip()
                    if value and not value.startswith("#"):
                        return value

        return None

    def _create_basic_company_info(self, company_data: Dict) -> CompanyInfo:
        """
        Create a basic CompanyInfo object from discovery data.

        Args:
            company_data: Basic company data from discovery

        Returns:
            CompanyInfo object with minimal data
        """
        return CompanyInfo(
            company_name=company_data.get("company_name", "Unknown"),
            website_url=company_data.get("website_url", ""),
            industry=company_data.get("industry"),
            core_business=company_data.get("description"),
            company_size=company_data.get("company_size"),
        )


# Service instance helper
def get_research_service() -> CompanyResearchService:
    """Get a company research service instance"""
    return CompanyResearchService()
