"""
AI Agent Service - Initializes and manages all Agno agents
"""
import os
from textwrap import dedent
from typing import Optional

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.exa import ExaTools
from agno.utils.log import logger

from app.core.config import settings


class AgentService:
    """
    Service for managing AI agents used in the email outreach workflow.
    Initializes and configures all Agno agents with their specific instructions.
    """

    def __init__(self):
        """Initialize the agent service with API keys from settings"""
        self.exa_api_key = settings.EXA_API_KEY
        self.openai_api_key = settings.OPENAI_API_KEY
        self.openai_model = settings.OPENAI_MODEL

        # Set environment variables for agents
        if self.exa_api_key:
            os.environ["EXA_API_KEY"] = self.exa_api_key
        if self.openai_api_key:
            os.environ["OPENAI_API_KEY"] = self.openai_api_key

        # Validate API keys
        if not self.exa_api_key:
            logger.warning("EXA_API_KEY not set - company discovery will not work")
        if not self.openai_api_key:
            logger.warning("OPENAI_API_KEY not set - AI generation will not work")

        # Initialize agents
        self._company_finder: Optional[Agent] = None
        self._contact_finder: Optional[Agent] = None
        self._company_researcher: Optional[Agent] = None
        self._email_creator: Optional[Agent] = None

    @property
    def company_finder(self) -> Agent:
        """
        Agent specialized in discovering companies that match specific criteria.
        Uses Exa search to find potential prospects.
        """
        if self._company_finder is None:
            self._company_finder = Agent(
                model=OpenAIChat(id=self.openai_model),
                tools=[ExaTools(api_key=self.exa_api_key)] if self.exa_api_key else [],
                description="Expert at finding companies that match specific criteria using web search",
                instructions=dedent("""\
                    You are a company discovery specialist. Your job is to find companies that match the given criteria.
                    
                    Search for companies based on:
                    - Industry/sector
                    - Company size
                    - Geographic location
                    - Business model
                    - Technology stack
                    - Recent funding/growth
                    
                    For each company found, provide:
                    - Company name
                    - Website URL
                    - Brief description
                    - Industry
                    - Estimated size
                    - Location
                    
                    Focus on finding companies that would be good prospects for the specified service offering.
                    Look for companies showing signs of growth, funding, or expansion.
                """),
            )
            logger.info("Company finder agent initialized")
        return self._company_finder

    @property
    def contact_finder(self) -> Agent:
        """
        Agent specialized in finding decision maker contacts at companies.
        Searches for key personnel and their contact information.
        """
        if self._contact_finder is None:
            self._contact_finder = Agent(
                model=OpenAIChat(id=self.openai_model),
                tools=[ExaTools(api_key=self.exa_api_key)] if self.exa_api_key else [],
                description="Expert at finding contact information for decision makers at companies",
                instructions=dedent("""\
                    You are a contact research specialist. Find decision makers and their contact information.
                    
                    For each company, search for:
                    - Key decision makers in target departments
                    - Their email addresses
                    - LinkedIn profiles
                    - Professional backgrounds
                    - Current role and responsibilities
                    
                    Focus on finding people in roles like:
                    - CEO, CTO, VP of Engineering (for tech solutions)
                    - CMO, VP Marketing, Growth Lead (for marketing solutions)
                    - VP Sales, Sales Director (for sales solutions)
                    - HR Director, People Ops (for HR solutions)
                    
                    Provide verified contact information when possible.
                    Structure your response with clear contact details.
                """),
            )
            logger.info("Contact finder agent initialized")
        return self._contact_finder

    @property
    def company_researcher(self) -> Agent:
        """
        Agent specialized in deep company research for personalization.
        Gathers comprehensive intelligence about target companies.
        """
        if self._company_researcher is None:
            self._company_researcher = Agent(
                model=OpenAIChat(id=self.openai_model),
                tools=[ExaTools(api_key=self.exa_api_key)] if self.exa_api_key else [],
                description="Expert at researching company details for personalization",
                instructions=dedent("""\
                    Research companies in depth to enable personalized outreach.
                    
                    Analyze:
                    - Company website and messaging
                    - Recent news and updates
                    - Product/service offerings
                    - Technology stack
                    - Growth indicators
                    - Pain points and challenges
                    - Recent achievements
                    - Market position
                    - Notable customers and case studies
                    - Company culture and values
                    
                    Focus on insights that would be relevant for B2B outreach:
                    - Scaling challenges
                    - Technology needs
                    - Market expansion
                    - Competitive positioning
                    - Recent wins or milestones
                    - Areas for improvement
                    
                    Provide detailed, structured information that can be used for email personalization.
                """),
            )
            logger.info("Company researcher agent initialized")
        return self._company_researcher

    @property
    def email_creator(self) -> Agent:
        """
        Agent specialized in creating personalized cold emails.
        Uses a friendly, conversational tone inspired by a young sales rep.
        """
        if self._email_creator is None:
            self._email_creator = Agent(
                model=OpenAIChat(id=self.openai_model),
                description=dedent("""\
                    You are writing for a friendly, empathetic 20-year-old sales rep whose
                    style is cool, concise, and respectful. Tone is casual yet professional.

                    - Be polite but natural, using simple language.
                    - Never sound robotic or use big cliché words like "delve", "synergy" or "revolutionary."
                    - Clearly address problems the prospect might be facing and how we solve them.
                    - Keep paragraphs short and friendly, with a natural voice.
                    - End on a warm, upbeat note, showing willingness to help.\
                """),
                instructions=dedent("""\
                    Please craft a highly personalized email that has:

                    1. A simple, personal subject line referencing the problem or opportunity.
                    2. At least one area for improvement or highlight from research.
                    3. A quick explanation of how we can help them (no heavy jargon).
                    4. References a known challenge from the research.
                    5. Avoid words like "delve", "explore", "synergy", "amplify", "game changer", "revolutionary", "breakthrough".
                    6. Use first-person language ("I") naturally.
                    7. Maintain a 20-year-old's friendly style—brief and to the point.
                    8. Avoid placing the recipient's name in the subject line.

                    Use the appropriate template based on the target professional type and outreach purpose.
                    Ensure the final tone feels personal and conversation-like, not automatically generated.
                    
                    Format your response with:
                    - Subject: [subject line]
                    - Body: [email body]
                    
                    Keep it concise but impactful.
                """),
            )
            logger.info("Email creator agent initialized")
        return self._email_creator

    def validate_agents(self) -> bool:
        """
        Validate that all required agents can be initialized.
        Returns True if all agents are ready, False otherwise.
        """
        try:
            # Try to access all agents to ensure they initialize
            _ = self.company_finder
            _ = self.contact_finder
            _ = self.company_researcher
            _ = self.email_creator
            logger.info("All agents validated successfully")
            return True
        except Exception as e:
            logger.error(f"Agent validation failed: {e}")
            return False

    def reset_agents(self):
        """Reset all agents (useful for testing or re-initialization)"""
        self._company_finder = None
        self._contact_finder = None
        self._company_researcher = None
        self._email_creator = None
        logger.info("All agents reset")


# Global agent service instance
_agent_service: Optional[AgentService] = None


def get_agent_service() -> AgentService:
    """
    Get or create the global agent service instance.
    This ensures we reuse agents across requests.
    """
    global _agent_service
    if _agent_service is None:
        _agent_service = AgentService()
    return _agent_service
