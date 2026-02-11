"""
Contact Service - Finds decision makers at target companies
"""
from typing import List, Dict, Optional
from agno.utils.log import logger

from app.schemas.outreach import ContactInfo, OutreachConfig
from app.services.agent_service import get_agent_service
from app.core.constants import COMPANY_CATEGORIES


class ContactFinderService:
    """
    Service for finding decision maker contacts at target companies.
    Uses AI agent to discover key personnel and their contact information.
    """

    def __init__(self):
        """Initialize the contact finder service"""
        self.agent_service = get_agent_service()

    def find_contacts(
        self,
        company_data: Dict,
        config: OutreachConfig,
    ) -> List[ContactInfo]:
        """
        Find decision makers at a target company.

        Args:
            company_data: Company information from discovery
            config: Outreach configuration with target departments

        Returns:
            List of ContactInfo objects for decision makers
        """
        company_name = company_data.get("company_name", "Unknown")
        logger.info(f"Finding decision makers at: {company_name}")
        logger.info(f"Target departments: {config.target_departments}")

        # Build contact search query
        search_query = self._build_contact_query(company_data, config)

        try:
            logger.info("Running contact finder agent...")
            response = self.agent_service.contact_finder.run(search_query)

            if not response or not response.content:
                logger.warning(f"No contacts found for {company_name}")
                return []

            logger.info(f"Contacts found for {company_name}")
            logger.debug(f"Response length: {len(response.content)} characters")

            # Parse contacts from response
            contacts = self._parse_contacts_response(
                response.content,
                company_name
            )

            logger.info(f"Parsed {len(contacts)} contacts")
            return contacts

        except Exception as e:
            logger.error(f"Error finding contacts for {company_name}: {e}")
            return []

    def _build_contact_query(self, company_data: Dict, config: OutreachConfig) -> str:
        """
        Build a contact search query for the agent.

        Args:
            company_data: Company information
            config: Outreach configuration

        Returns:
            Formatted search query string
        """
        company_name = company_data.get("company_name", "Unknown")
        website = company_data.get("website_url", "")

        # Get typical roles for this company category
        category_info = COMPANY_CATEGORIES.get(config.company_category, {})
        typical_roles = category_info.get("typical_roles", [])

        query = f"""
Find decision makers and key contacts at the following company:

Company Name: {company_name}
Website: {website}
Industry: {company_data.get('industry', 'Unknown')}

Target Departments: {', '.join(config.target_departments)}
Service Offering: {config.service_type}

Focus on finding people in these types of roles:
{chr(10).join(f"- {role}" for role in typical_roles) if typical_roles else "- C-level executives, VPs, Directors, Managers"}

For each contact found, provide:
1. Full Name
2. Job Title/Position
3. Department (if known)
4. Email Address (if available)
5. LinkedIn Profile URL (if available)
6. Brief professional background (1-2 sentences)

Search on:
- Company website team/about pages
- LinkedIn company page
- Recent press releases or news mentioning key personnel
- Industry databases

Format your response clearly with each contact separated and labeled (Contact 1, Contact 2, etc.).
Prioritize contacts most relevant to {config.service_type} and {', '.join(config.target_departments)}.
"""
        return query

    def _parse_contacts_response(
        self,
        response_text: str,
        company_name: str
    ) -> List[ContactInfo]:
        """
        Parse the agent response into ContactInfo objects.

        Args:
            response_text: Raw text response from agent
            company_name: Company name for the contacts

        Returns:
            List of ContactInfo objects
        """
        contacts = []

        # Split by contact markers
        contact_sections = response_text.split("Contact ")

        for section in contact_sections:
            if not section.strip() or section.strip().startswith("Focus"):
                continue

            try:
                contact_data = {
                    "name": self._extract_field(section, ["name", "full name"]),
                    "title": self._extract_field(section, ["title", "position", "role", "job title"]),
                    "email": self._extract_field(section, ["email", "e-mail"]),
                    "linkedin": self._extract_field(section, ["linkedin", "profile"]),
                    "department": self._extract_field(section, ["department", "division"]),
                    "background": self._extract_field(section, ["background", "bio", "about"]),
                    "company": company_name,
                }

                # Only add if we have at least a name and title
                if contact_data["name"] and contact_data["title"]:
                    contact_info = ContactInfo(**contact_data)
                    contacts.append(contact_info)

            except Exception as e:
                logger.warning(f"Error parsing contact section: {e}")
                continue

        return contacts

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
                        if value and not value.startswith("http") or "@" in value or "linkedin" in keyword.lower():
                            return value
                    elif "-" in line and not line.strip().startswith("-"):
                        value = line.split("-", 1)[1].strip()
                        if value:
                            return value

        return None

    def format_contacts_for_email(self, contacts: List[ContactInfo]) -> str:
        """
        Format contacts for email generation context.

        Args:
            contacts: List of ContactInfo objects

        Returns:
            Formatted string describing contacts
        """
        if not contacts:
            return "No specific contacts identified"

        formatted = []
        for i, contact in enumerate(contacts, 1):
            contact_str = f"""
Contact {i}:
- Name: {contact.name}
- Title: {contact.title}
- Department: {contact.department or 'N/A'}
- Email: {contact.email or 'Not available'}
- LinkedIn: {contact.linkedin or 'Not available'}
- Background: {contact.background or 'N/A'}
"""
            formatted.append(contact_str.strip())

        return "\n\n".join(formatted)


# Service instance helper
def get_contact_service() -> ContactFinderService:
    """Get a contact finder service instance"""
    return ContactFinderService()
