"""
Company Discovery Service - Finds target companies using Exa search
"""
from typing import List, Dict, Optional
from agno.utils.log import logger

from app.schemas.outreach import OutreachConfig, CompanyInfo
from app.services.agent_service import get_agent_service
from app.core.constants import COMPANY_CATEGORIES


class CompanyDiscoveryService:
    """
    Service for discovering target companies based on outreach criteria.
    Uses Exa-powered AI agent to find companies matching specific requirements.
    """

    def __init__(self):
        """Initialize the company discovery service"""
        self.agent_service = get_agent_service()

    def discover_companies(
        self,
        config: OutreachConfig,
        num_companies: int = 5,
    ) -> List[Dict]:
        """
        Discover companies matching the outreach criteria.

        Args:
            config: Outreach configuration with targeting criteria
            num_companies: Number of companies to discover

        Returns:
            List of discovered companies with basic information
        """
        logger.info(f"Starting company discovery for {num_companies} companies")
        logger.info(f"Category: {config.company_category}")
        logger.info(f"Service Type: {config.service_type}")
        logger.info(f"Company Size: {config.company_size_preference}")

        # Build search query based on configuration
        search_query = self._build_search_query(config, num_companies)

        # Use company finder agent to discover companies
        try:
            logger.info("Running company finder agent...")
            response = self.agent_service.company_finder.run(search_query)

            if not response or not response.content:
                logger.error("No companies found by agent")
                return []

            logger.info("Companies discovered successfully")
            logger.debug(f"Response: {response.content[:200]}...")

            # Parse the response into structured data
            companies = self._parse_companies_response(response.content)
            logger.info(f"Parsed {len(companies)} companies from response")

            return companies

        except Exception as e:
            logger.error(f"Error discovering companies: {e}")
            raise

    def _build_search_query(self, config: OutreachConfig, num_companies: int) -> str:
        """
        Build a search query for the company finder agent.

        Args:
            config: Outreach configuration
            num_companies: Number of companies to find

        Returns:
            Formatted search query string
        """
        category_info = COMPANY_CATEGORIES.get(config.company_category, {})
        category_description = category_info.get("description", config.company_category)

        query = f"""
Find {num_companies} {config.company_category} companies that would be excellent prospects for {config.service_type}.

Company Criteria:
- Industry: {config.company_category} ({category_description})
- Size Preference: {config.company_size_preference}
- Target Departments: {', '.join(config.target_departments)}
- Service Offering: {config.service_type}

Search Focus:
- Look for companies showing growth, recent funding, or expansion
- Companies that are actively hiring or expanding their teams
- Companies with recent product launches or market entry
- Companies that match the size preference: {config.company_size_preference}

For each company, provide:
1. Company Name
2. Website URL
3. Industry/Sector
4. Brief Description (1-2 sentences)
5. Company Size (estimated)
6. Location (HQ)
7. Why they're a good prospect (recent activity, growth indicators)

Format your response clearly with each company separated and labeled (Company 1, Company 2, etc.).
"""
        return query

    def _parse_companies_response(self, response_text: str) -> List[Dict]:
        """
        Parse the agent response into structured company data.

        Args:
            response_text: Raw text response from the agent

        Returns:
            List of company dictionaries
        """
        companies = []

        # Simple parsing - split by company markers
        # In production, you might want more robust parsing
        company_sections = response_text.split("Company ")

        for section in company_sections:
            if not section.strip() or section.strip().startswith("Criteria"):
                continue

            try:
                # Extract basic information from the section
                lines = section.strip().split("\n")
                company_data = {
                    "raw_text": section.strip(),
                    "company_name": self._extract_field(section, ["name", "company name"]),
                    "website_url": self._extract_field(section, ["website", "url", "site"]),
                    "industry": self._extract_field(section, ["industry", "sector"]),
                    "description": self._extract_field(section, ["description", "about"]),
                    "company_size": self._extract_field(section, ["size", "employees"]),
                    "location": self._extract_field(section, ["location", "hq", "headquarters"]),
                    "why_prospect": self._extract_field(section, ["why", "prospect", "reason"]),
                }

                if company_data["company_name"]:
                    companies.append(company_data)

            except Exception as e:
                logger.warning(f"Error parsing company section: {e}")
                continue

        return companies

    def _extract_field(self, text: str, keywords: List[str]) -> Optional[str]:
        """
        Extract a field value from text based on keywords.

        Args:
            text: Text to search in
            keywords: List of possible field names

        Returns:
            Extracted field value or None
        """
        lines = text.split("\n")

        for line in lines:
            line_lower = line.lower()
            for keyword in keywords:
                if keyword in line_lower:
                    # Extract value after colon or dash
                    if ":" in line:
                        value = line.split(":", 1)[1].strip()
                        if value:
                            return value
                    elif "-" in line and not line.strip().startswith("-"):
                        value = line.split("-", 1)[1].strip()
                        if value:
                            return value

        return None

    def format_company_for_research(self, company_data: Dict) -> str:
        """
        Format company data for research agent input.

        Args:
            company_data: Company information dictionary

        Returns:
            Formatted string for research
        """
        formatted = f"""
Company: {company_data.get('company_name', 'Unknown')}
Website: {company_data.get('website_url', 'N/A')}
Industry: {company_data.get('industry', 'N/A')}
Description: {company_data.get('description', 'N/A')}
Size: {company_data.get('company_size', 'N/A')}
Location: {company_data.get('location', 'N/A')}
Why Prospect: {company_data.get('why_prospect', 'N/A')}
"""
        return formatted.strip()


# Service instance helper
def get_company_service() -> CompanyDiscoveryService:
    """Get a company discovery service instance"""
    return CompanyDiscoveryService()
