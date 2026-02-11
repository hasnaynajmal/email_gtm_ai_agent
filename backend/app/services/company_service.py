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
            logger.info(f"Response content: {response.content[:500]}...")  # Log more for debugging

            # Parse the response into structured data
            companies = self._parse_companies_response(response.content)
            logger.info(f"Parsed {len(companies)} companies from response")
            
            if not companies:
                logger.warning("No companies parsed from response. Full response:")
                logger.warning(response.content)

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
        Handles the format: **Company X: Name** followed by numbered list.

        Args:
            response_text: Raw text response from the agent

        Returns:
            List of company dictionaries
        """
        companies = []
        
        import re
        
        # Match **Company X: Name** pattern
        company_pattern = r'\*\*Company\s+(\d+):\s+([^*]+)\*\*'
        matches = list(re.finditer(company_pattern, response_text, flags=re.MULTILINE | re.IGNORECASE))
        
        logger.info(f"Found {len(matches)} company headers")
        
        if not matches:
            logger.warning("No company headers found in response")
            return companies
        
        # Extract sections for each company
        for i, match in enumerate(matches):
            company_name = match.group(2).strip()
            start_pos = match.end()
            
            # Determine end position (start of next company or end of text)
            end_pos = matches[i + 1].start() if i + 1 < len(matches) else len(response_text)
            section = response_text[start_pos:end_pos].strip()
            
            if not section or len(section) < 20:
                continue

            try:
                # Extract information from numbered list items
                company_data = {
                    "raw_text": section,
                    "company_name": company_name,
                    "website_url": self._extract_numbered_field(section, ["website", "url"]),
                    "industry": self._extract_numbered_field(section, ["industry", "sector"]),
                    "description": self._extract_numbered_field(section, ["description", "brief description"]),
                    "company_size": self._extract_numbered_field(section, ["company size", "size", "employees"]),
                    "location": self._extract_numbered_field(section, ["location", "hq", "headquarters"]),
                    "why_prospect": self._extract_numbered_field(section, ["why", "prospect", "good prospect"]),
                }

                # If no website URL found, try markdown link or plain URL extraction
                if not company_data["website_url"]:
                    # Try to extract from markdown link first
                    md_url = self._extract_markdown_url(section)
                    if md_url:
                        company_data["website_url"] = md_url
                    else:
                        # Fallback to plain URL
                        extracted_url = self._extract_url(section)
                        if extracted_url:
                            company_data["website_url"] = extracted_url

                # If we have at least company name and website, consider it valid
                if company_data["company_name"] and company_data["website_url"]:
                    logger.info(f"Parsed company: {company_data['company_name']} - {company_data['website_url']}")
                    companies.append(company_data)
                else:
                    logger.warning(f"Skipping company '{company_name}' - missing website URL")
            except Exception as e:
                logger.warning(f"Error parsing company '{company_name}': {e}")
                continue

        return companies

    def _extract_markdown_url(self, text: str) -> Optional[str]:
        """
        Extract URL from markdown link format [text](url).

        Args:
            text: Text containing markdown links

        Returns:
            First URL found in markdown format or None
        """
        import re
        # Match [text](url) format
        md_link_pattern = r'\[([^\]]+)\]\((https?://[^\)]+)\)'
        match = re.search(md_link_pattern, text)
        if match:
            return match.group(2).strip()
        return None

    def _extract_url(self, text: str) -> Optional[str]:
        """
        Extract URL from text using regex pattern.
        Fallback method for URLs not explicitly labeled.

        Args:
            text: Text to search for URLs

        Returns:
            First URL found or None
        """
        import re
        url_pattern = r'https?://(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&/=]*)'
        match = re.search(url_pattern, text)
        return match.group(0) if match else None

    def _extract_numbered_field(self, text: str, keywords: List[str]) -> Optional[str]:
        """
        Extract field value from numbered list format.
        Format: "1. **Field Name:** Value" or with markdown link.

        Args:
            text: Text to search in
            keywords: List of possible field names

        Returns:
            Extracted field value or None
        """
        import re
        lines = text.split("\n")

        for line in lines:
            line_lower = line.lower().strip()
            
            for keyword in keywords:
                if keyword.lower() in line_lower:
                    # Remove leading number, bullet, or dash
                    cleaned_line = re.sub(r'^[\d\.\-\*•\s]+', '', line).strip()
                    
                    # Remove markdown bold
                    cleaned_line = cleaned_line.replace("**", "")
                    
                    # Extract value after colon
                    if ":" in cleaned_line:
                        parts = cleaned_line.split(":", 1)
                        if keyword.lower() in parts[0].lower():
                            value = parts[1].strip()
                            
                            # For markdown links [text](url), extract the URL
                            md_match = re.search(r'\[([^\]]+)\]\((https?://[^\)]+)\)', value)
                            if md_match:
                                return md_match.group(2).strip()
                            
                            # Otherwise just return the value
                            if value and len(value) > 1:
                                return value

        return None

    def _extract_field(self, text: str, keywords: List[str]) -> Optional[str]:
        """
        Extract a field value from text based on keywords.
        Improved to handle multiple formats including markdown.

        Args:
            text: Text to search in
            keywords: List of possible field names

        Returns:
            Extracted field value or None
        """
        lines = text.split("\n")

        for line in lines:
            line_lower = line.lower().strip()
            
            for keyword in keywords:
                # Check if keyword appears in the line
                if keyword.lower() in line_lower:
                    # Try multiple extraction patterns
                    
                    # Pattern 1: "Keyword: Value"
                    if ":" in line:
                        parts = line.split(":", 1)
                        if keyword.lower() in parts[0].lower():
                            value = parts[1].strip()
                            # Remove markdown formatting
                            value = value.replace("**", "").replace("*", "").strip()
                            if value and len(value) > 1:
                                return value
                    
                    # Pattern 2: "- Keyword: Value" or "* Keyword: Value"
                    if line.strip().startswith(("-", "*", "•")):
                        if ":" in line:
                            value = line.split(":", 1)[1].strip()
                            value = value.replace("**", "").replace("*", "").strip()
                            if value and len(value) > 1:
                                return value
                    
                    # Pattern 3: "**Keyword**: Value" (markdown bold)
                    if "**" in line and ":" in line:
                        value = line.split(":", 1)[1].strip()
                        value = value.replace("**", "").replace("*", "").strip()
                        if value and len(value) > 1:
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
