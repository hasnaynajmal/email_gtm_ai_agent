"""
Email Generation Service - Creates personalized cold emails
"""
import json
from typing import List, Dict, Optional
from agno.utils.log import logger

from app.schemas.outreach import (
    CompanyInfo,
    ContactInfo,
    SenderDetails,
    OutreachConfig,
    GeneratedEmail,
)
from app.services.agent_service import get_agent_service
from app.core.constants import DEPARTMENT_TEMPLATES, EMAIL_TONE_GUIDELINES


class EmailGenerationService:
    """
    Service for generating personalized cold emails.
    Uses AI agent to create engaging, personalized outreach emails.
    """

    def __init__(self):
        """Initialize the email generation service"""
        self.agent_service = get_agent_service()

    def generate_email(
        self,
        company_info: CompanyInfo,
        contacts: List[ContactInfo],
        sender_details: SenderDetails,
        config: OutreachConfig,
    ) -> GeneratedEmail:
        """
        Generate a personalized email for a company contact.

        Args:
            company_info: Company research data
            contacts: List of decision makers at the company
            sender_details: Sender information
            config: Outreach configuration

        Returns:
            GeneratedEmail object with subject and body
        """
        logger.info(f"Generating email for: {company_info.company_name}")

        # Select appropriate template
        template = self._select_template(config)

        # Build email generation context
        email_context = self._build_email_context(
            company_info,
            contacts,
            sender_details,
            config,
            template
        )

        try:
            logger.info("Running email creator agent...")
            response = self.agent_service.email_creator.run(email_context)

            if not response or not response.content:
                logger.error(f"No email generated for {company_info.company_name}")
                return self._create_fallback_email(company_info, sender_details)

            logger.info("Email generated successfully")

            # Parse the email response
            email = self._parse_email_response(response.content, company_info)
            return email

        except Exception as e:
            logger.error(f"Error generating email: {e}")
            return self._create_fallback_email(company_info, sender_details)

    def _select_template(self, config: OutreachConfig) -> str:
        """
        Select appropriate email template based on configuration.

        Args:
            config: Outreach configuration

        Returns:
            Email template string
        """
        # Get primary target department
        primary_dept = config.target_departments[0] if config.target_departments else "GTM (Sales & Marketing)"

        # Try to get template for department and service type
        if primary_dept in DEPARTMENT_TEMPLATES:
            dept_templates = DEPARTMENT_TEMPLATES[primary_dept]
            if config.service_type in dept_templates:
                logger.info(f"Selected template: {primary_dept} - {config.service_type}")
                return dept_templates[config.service_type]

        # Fallback to GTM Software Solution template
        logger.warning(f"No specific template found, using default")
        return DEPARTMENT_TEMPLATES["GTM (Sales & Marketing)"]["Software Solution"]

    def _build_email_context(
        self,
        company_info: CompanyInfo,
        contacts: List[ContactInfo],
        sender_details: SenderDetails,
        config: OutreachConfig,
        template: str
    ) -> str:
        """
        Build comprehensive context for email generation.

        Args:
            company_info: Company research data
            contacts: Contact information
            sender_details: Sender details
            config: Outreach configuration
            template: Selected email template

        Returns:
            Formatted context string for the agent
        """
        # Get primary contact
        primary_contact = contacts[0] if contacts else None

        # Build company insights
        company_insights = self._extract_company_insights(company_info, config)

        context = f"""
Generate a highly personalized cold email using the following information:

=== TEMPLATE ===
{template}

=== RECIPIENT INFORMATION ===
"""

        if primary_contact:
            context += f"""
Name: {primary_contact.name}
Title: {primary_contact.title}
Department: {primary_contact.department or 'Unknown'}
Company: {company_info.company_name}
Background: {primary_contact.background or 'N/A'}
"""
        else:
            context += f"""
Company: {company_info.company_name}
(No specific contact identified - address to relevant department)
"""

        context += f"""

=== COMPANY RESEARCH ===
Company Name: {company_info.company_name}
Website: {company_info.website_url}
Industry: {company_info.industry or 'N/A'}
Business: {company_info.core_business or 'N/A'}
Size: {company_info.company_size or 'N/A'}

{company_insights}

=== SENDER INFORMATION ===
Name: {sender_details.name}
Email: {sender_details.email}
Organization: {sender_details.organization}
Service Offered: {sender_details.service_offered}
Calendar Link: {sender_details.calendar_link or 'N/A'}
LinkedIn: {sender_details.linkedin or 'N/A'}
Phone: {sender_details.phone or 'N/A'}
Website: {sender_details.website or 'N/A'}

=== OUTREACH CONFIGURATION ===
Service Type: {config.service_type}
Target Departments: {', '.join(config.target_departments)}
Personalization Level: {config.personalization_level}

=== TONE & STYLE GUIDELINES ===
Tone: {EMAIL_TONE_GUIDELINES['tone']}
Style: {EMAIL_TONE_GUIDELINES['style']}
Avoid: {', '.join(EMAIL_TONE_GUIDELINES['avoid'])}
Include: {', '.join(EMAIL_TONE_GUIDELINES['include'])}

=== INSTRUCTIONS ===
1. Use the template as a GUIDE, not a strict format
2. Personalize heavily using the company research
3. Reference specific achievements, challenges, or news from the research
4. Make it feel like you genuinely know about their company
5. Keep the tone friendly and conversational (like a 20-year-old sales rep)
6. Avoid corporate jargon and buzzwords
7. Clear value proposition for {config.service_type}
8. Strong, simple call-to-action (calendar link)

Format your response as:
Subject: [compelling subject line]

[email body]

Best,
{sender_details.name}
{sender_details.organization}
[Include calendar link in signature]
"""

        return context

    def _extract_company_insights(
        self,
        company_info: CompanyInfo,
        config: OutreachConfig
    ) -> str:
        """
        Extract relevant insights from company research.

        Args:
            company_info: Company information
            config: Outreach configuration

        Returns:
            Formatted insights string
        """
        insights = []

        if company_info.recent_news:
            insights.append("Recent News:")
            for news in company_info.recent_news[:3]:
                insights.append(f"  - {news}")

        if company_info.challenges:
            insights.append("\nPotential Challenges:")
            for challenge in company_info.challenges[:3]:
                insights.append(f"  - {challenge}")

        if company_info.growth_areas:
            insights.append("\nGrowth Opportunities:")
            for growth in company_info.growth_areas[:3]:
                insights.append(f"  - {growth}")

        if company_info.technologies:
            insights.append(f"\nTechnology Stack: {', '.join(company_info.technologies[:5])}")

        if company_info.unique_selling_points:
            insights.append("\nUnique Selling Points:")
            for usp in company_info.unique_selling_points[:3]:
                insights.append(f"  - {usp}")

        if company_info.awards:
            insights.append(f"\nAwards/Recognition: {', '.join(company_info.awards[:3])}")

        return "\n".join(insights) if insights else "Limited research data available"

    def _parse_email_response(
        self,
        response_text: str,
        company_info: CompanyInfo
    ) -> GeneratedEmail:
        """
        Parse the email response into a GeneratedEmail object.

        Args:
            response_text: Raw response from agent
            company_info: Company information for context

        Returns:
            GeneratedEmail object
        """
        # Split into subject and body
        lines = response_text.strip().split("\n")

        subject = ""
        body_lines = []
        in_body = False

        for line in lines:
            if line.strip().lower().startswith("subject:"):
                subject = line.split(":", 1)[1].strip()
            elif not in_body and line.strip() == "":
                in_body = True
            elif in_body:
                body_lines.append(line)

        body = "\n".join(body_lines).strip()

        # If parsing failed, use the whole response as body
        if not subject or not body:
            subject = f"Quick question about {company_info.company_name}"
            body = response_text.strip()

        # Generate personalization notes
        notes = self._generate_personalization_notes(company_info)

        return GeneratedEmail(
            subject=subject,
            body=body,
            personalization_notes=notes
        )

    def _generate_personalization_notes(self, company_info: CompanyInfo) -> str:
        """
        Generate notes about what personalization was used.

        Args:
            company_info: Company information

        Returns:
            Notes string
        """
        notes = []

        if company_info.recent_news:
            notes.append(f"Referenced recent company news ({len(company_info.recent_news)} items)")

        if company_info.challenges:
            notes.append(f"Addressed potential challenges ({len(company_info.challenges)} identified)")

        if company_info.growth_areas:
            notes.append(f"Highlighted growth opportunities ({len(company_info.growth_areas)} areas)")

        if company_info.technologies:
            notes.append(f"Mentioned technology stack")

        return " | ".join(notes) if notes else "Basic personalization applied"

    def _create_fallback_email(
        self,
        company_info: CompanyInfo,
        sender_details: SenderDetails
    ) -> GeneratedEmail:
        """
        Create a basic fallback email if generation fails.

        Args:
            company_info: Company information
            sender_details: Sender details

        Returns:
            Basic GeneratedEmail object
        """
        subject = f"Thought you'd be interested - {company_info.company_name}"

        body = f"""Hey there,

I came across {company_info.company_name} and was impressed by what you're building in the {company_info.industry or 'industry'}.

We at {sender_details.organization} {sender_details.service_offered.lower()}.

Would love to chat if you're open to it. Here's my calendar: {sender_details.calendar_link or 'Let me know a time that works!'}

Best,
{sender_details.name}
{sender_details.organization}
"""

        return GeneratedEmail(
            subject=subject,
            body=body,
            personalization_notes="Fallback email template used due to generation error"
        )


# Service instance helper
def get_email_service() -> EmailGenerationService:
    """Get an email generation service instance"""
    return EmailGenerationService()
