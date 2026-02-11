"""
Pydantic schemas for AI Email GTM Outreach
"""
from typing import Dict, List, Optional, Literal
from pydantic import BaseModel, Field


class OutreachConfig(BaseModel):
    """Configuration for email outreach campaign"""
    company_category: str = Field(..., description="Type of companies to target")
    target_departments: List[str] = Field(
        ..., 
        description="Departments to target (e.g., GTM, HR, Engineering)"
    )
    service_type: Literal[
        "Software Solution",
        "Consulting Services",
        "Professional Services",
        "Technology Platform",
        "Custom Development"
    ] = Field(..., description="Type of service being offered")
    company_size_preference: Literal[
        "Startup (1-50)", 
        "SMB (51-500)", 
        "Enterprise (500+)", 
        "All Sizes"
    ] = Field(
        default="All Sizes",
        description="Preferred company size"
    )
    personalization_level: Literal["Basic", "Medium", "Deep"] = Field(
        default="Deep", 
        description="Level of personalization"
    )


class ContactInfo(BaseModel):
    """Contact information for decision makers"""
    name: str = Field(..., description="Contact's full name")
    title: str = Field(..., description="Job title/position")
    email: Optional[str] = Field(None, description="Email address")
    linkedin: Optional[str] = Field(None, description="LinkedIn profile URL")
    company: str = Field(..., description="Company name")
    department: Optional[str] = Field(None, description="Department")
    background: Optional[str] = Field(None, description="Professional background")


class CompanyInfo(BaseModel):
    """
    Stores in-depth data about a company gathered during the research phase.
    """
    # Basic Information
    company_name: str = Field(..., description="Company name")
    website_url: str = Field(..., description="Company website URL")

    # Business Details
    industry: Optional[str] = Field(None, description="Primary industry")
    core_business: Optional[str] = Field(None, description="Main business focus")
    business_model: Optional[str] = Field(None, description="B2B, B2C, etc.")

    # Marketing Information
    motto: Optional[str] = Field(None, description="Company tagline/slogan")
    value_proposition: Optional[str] = Field(None, description="Main value proposition")
    target_audience: Optional[List[str]] = Field(
        None, description="Target customer segments"
    )

    # Company Metrics
    company_size: Optional[str] = Field(None, description="Employee count range")
    founded_year: Optional[int] = Field(None, description="Year founded")
    locations: Optional[List[str]] = Field(None, description="Office locations")

    # Technical Details
    technologies: Optional[List[str]] = Field(None, description="Technology stack")
    integrations: Optional[List[str]] = Field(None, description="Software integrations")

    # Market Position
    competitors: Optional[List[str]] = Field(None, description="Main competitors")
    unique_selling_points: Optional[List[str]] = Field(
        None, description="Key differentiators"
    )
    market_position: Optional[str] = Field(None, description="Market positioning")

    # Social Proof
    customers: Optional[List[str]] = Field(None, description="Notable customers")
    case_studies: Optional[List[str]] = Field(None, description="Success stories")
    awards: Optional[List[str]] = Field(None, description="Awards and recognition")

    # Recent Activity
    recent_news: Optional[List[str]] = Field(None, description="Recent news/updates")
    blog_topics: Optional[List[str]] = Field(None, description="Recent blog topics")

    # Pain Points & Opportunities
    challenges: Optional[List[str]] = Field(None, description="Potential pain points")
    growth_areas: Optional[List[str]] = Field(None, description="Growth opportunities")

    # Contact Information
    email_address: Optional[str] = Field(None, description="Contact email")
    phone: Optional[str] = Field(None, description="Contact phone")
    social_media: Optional[Dict[str, str]] = Field(
        None, description="Social media links"
    )

    # Additional Fields
    pricing_model: Optional[str] = Field(None, description="Pricing strategy and tiers")
    user_base: Optional[str] = Field(None, description="Estimated user base size")
    key_features: Optional[List[str]] = Field(None, description="Main product features")
    integration_ecosystem: Optional[List[str]] = Field(
        None, description="Integration partners"
    )
    funding_status: Optional[str] = Field(
        None, description="Latest funding information"
    )
    growth_metrics: Optional[Dict[str, str]] = Field(
        None, description="Key growth indicators"
    )


class SenderDetails(BaseModel):
    """Sender information for outreach emails"""
    name: str = Field(..., description="Sender's full name")
    email: str = Field(..., description="Sender's email address")
    organization: str = Field(..., description="Organization name")
    service_offered: str = Field(..., description="Description of service offered")
    calendar_link: Optional[str] = Field(None, description="Calendar booking link")
    linkedin: Optional[str] = Field(None, description="LinkedIn profile URL")
    phone: Optional[str] = Field(None, description="Contact phone number")
    website: Optional[str] = Field(None, description="Company website URL")


class EmailGenerationRequest(BaseModel):
    """Request to generate a personalized email"""
    company_info: CompanyInfo
    contact_info: ContactInfo
    sender_details: SenderDetails
    outreach_config: OutreachConfig


class GeneratedEmail(BaseModel):
    """Generated email output"""
    subject: str = Field(..., description="Email subject line")
    body: str = Field(..., description="Email body content")
    personalization_notes: Optional[str] = Field(
        None, 
        description="Notes about personalization used"
    )


class EmailGenerationResponse(BaseModel):
    """Response with generated email"""
    email: GeneratedEmail
    company_info: CompanyInfo
    contact_info: ContactInfo


class CampaignConfig(BaseModel):
    """Complete campaign configuration"""
    outreach_config: OutreachConfig
    sender_details: SenderDetails
    num_companies: int = Field(
        default=5, 
        ge=1, 
        le=20, 
        description="Number of companies to target"
    )


class CampaignResult(BaseModel):
    """Result of a complete campaign execution"""
    company_info: CompanyInfo
    contacts: List[ContactInfo]
    generated_emails: List[GeneratedEmail]
    research_summary: Optional[str] = Field(
        None, 
        description="Summary of company research"
    )


class CampaignExecutionResponse(BaseModel):
    """Response from campaign execution"""
    campaign_id: Optional[str] = Field(None, description="Campaign identifier")
    results: List[CampaignResult]
    total_companies: int
    total_contacts: int
    total_emails: int
    execution_time: Optional[float] = Field(None, description="Execution time in seconds")


class CampaignOptionsResponse(BaseModel):
    """Available options for campaign configuration"""
    company_categories: Dict[str, Dict[str, any]]
    service_types: List[str]
    company_sizes: List[str]
    personalization_levels: List[str]
    target_departments: List[str]
