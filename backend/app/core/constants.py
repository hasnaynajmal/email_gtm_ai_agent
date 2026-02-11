"""
Constants and templates for AI Email GTM Outreach
"""
from typing import Dict

# Department-specific email templates
DEPARTMENT_TEMPLATES: Dict[str, Dict[str, str]] = {
    "GTM (Sales & Marketing)": {
        "Software Solution": """\
Hey [RECIPIENT_NAME],

I noticed [COMPANY_NAME]'s impressive [GTM_INITIATIVE] and your role in scaling [SPECIFIC_ACHIEVEMENT]. Your approach to [SALES_STRATEGY] caught my attention.

[PRODUCT_VALUE_FOR_GTM]

[GTM_SPECIFIC_BENEFIT]

Would love to show you how this could work for your team: [CALENDAR_LINK]

Best,
[SIGNATURE]\
""",
        "Consulting Services": """\
Hey [RECIPIENT_NAME],

Your team's recent success with [CAMPAIGN_NAME] is impressive, particularly the [SPECIFIC_METRIC].

[CONSULTING_VALUE_PROP]

[GTM_IMPROVEMENT_POTENTIAL]

Here's my calendar if you'd like to explore this: [CALENDAR_LINK]

Best,
[SIGNATURE]\
"""
    },
    "Human Resources": {
        "Software Solution": """\
Hey [RECIPIENT_NAME],

I've been following [COMPANY_NAME]'s growth and noticed your focus on [HR_INITIATIVE]. Your approach to [SPECIFIC_HR_PROGRAM] stands out.

[HR_TOOL_VALUE_PROP]

[HR_SPECIFIC_BENEFIT]

Would you be open to seeing how this could help your HR initiatives? [CALENDAR_LINK]

Best,
[SIGNATURE]\
""",
        "Consulting Services": """\
Hey [RECIPIENT_NAME],

I've been following [COMPANY_NAME]'s journey in [INDUSTRY], and your recent [ACHIEVEMENT] caught my attention. Your approach to [SPECIFIC_FOCUS] aligns perfectly with what we're building.

[PARTNERSHIP_VALUE_PROP]

[MUTUAL_BENEFIT]

Would love to explore potential synergies over a quick call: [CALENDAR_LINK]

Best,
[SIGNATURE]\
""",
        "Investment Opportunity": """\
Hey [RECIPIENT_NAME],

Your work at [COMPANY_NAME] in [SPECIFIC_FOCUS] is impressive, especially [RECENT_ACHIEVEMENT].

[INVESTMENT_THESIS]

[UNIQUE_VALUE_ADD]

Here's my calendar if you'd like to discuss: [CALENDAR_LINK]

Best,
[SIGNATURE]\
"""
    },
    "Marketing Professional": {
        "Product Demo": """\
Hey [RECIPIENT_NAME],

I noticed [COMPANY_NAME]'s recent [MARKETING_INITIATIVE] and was impressed by [SPECIFIC_DETAIL].

[PRODUCT_VALUE_PROP]

[BENEFIT_TO_MARKETING]

Would you be open to a quick demo? Here's my calendar: [CALENDAR_LINK]

Best,
[SIGNATURE]\
""",
        "Service Offering": """\
Hey [RECIPIENT_NAME],

Saw your team's work on [RECENT_CAMPAIGN] - great execution on [SPECIFIC_ELEMENT].

[SERVICE_VALUE_PROP]

[MARKETING_BENEFIT]

Here's my calendar if you'd like to explore this: [CALENDAR_LINK]

Best,
[SIGNATURE]\
"""
    },
    "B2B Sales Representative": {
        "Product Demo": """\
Hey [RECIPIENT_NAME],

Noticed your team at [COMPANY_NAME] is scaling [SALES_FOCUS]. Your approach to [SPECIFIC_STRATEGY] is spot-on.

[PRODUCT_VALUE_PROP]

[SALES_BENEFIT]

Would you be interested in seeing how this works? Here's my calendar: [CALENDAR_LINK]

Best,
[SIGNATURE]\
""",
        "Service Offering": """\
Hey [RECIPIENT_NAME],

Your sales team's success with [RECENT_WIN] caught my attention. Particularly impressed by [SPECIFIC_ACHIEVEMENT].

[SERVICE_VALUE_PROP]

[SALES_IMPROVEMENT]

Here's my calendar if you'd like to discuss: [CALENDAR_LINK]

Best,
[SIGNATURE]\
"""
    }
}

# Company categories with descriptions and typical roles
COMPANY_CATEGORIES: Dict[str, Dict[str, any]] = {
    "SaaS/Technology Companies": {
        "description": "Software, cloud services, and tech platforms",
        "typical_roles": [
            "CTO", 
            "Head of Engineering", 
            "VP of Product", 
            "Engineering Manager", 
            "Tech Lead"
        ]
    },
    "E-commerce/Retail": {
        "description": "Online retail, marketplaces, and D2C brands",
        "typical_roles": [
            "Head of Digital", 
            "E-commerce Manager", 
            "Marketing Director", 
            "Operations Head"
        ]
    },
    "Financial Services": {
        "description": "Banks, fintech, insurance, and investment firms",
        "typical_roles": [
            "CFO", 
            "Head of Innovation", 
            "Risk Manager", 
            "Product Manager"
        ]
    },
    "Healthcare/Biotech": {
        "description": "Healthcare providers, biotech, and health tech",
        "typical_roles": [
            "Medical Director", 
            "Head of R&D", 
            "Clinical Manager", 
            "Healthcare IT Lead"
        ]
    },
    "Manufacturing/Industrial": {
        "description": "Manufacturing, industrial automation, and supply chain",
        "typical_roles": [
            "Operations Director", 
            "Plant Manager", 
            "Supply Chain Head", 
            "Quality Manager"
        ]
    }
}

# Service types available
SERVICE_TYPES = [
    "Software Solution",
    "Consulting Services",
    "Professional Services",
    "Technology Platform",
    "Custom Development"
]

# Company size preferences
COMPANY_SIZES = [
    "Startup (1-50)",
    "SMB (51-500)",
    "Enterprise (500+)",
    "All Sizes"
]

# Personalization levels
PERSONALIZATION_LEVELS = [
    "Basic",
    "Medium",
    "Deep"
]

# Target departments
TARGET_DEPARTMENTS = [
    "GTM (Sales & Marketing)",
    "Human Resources",
    "Engineering/Tech",
    "Operations",
    "Finance",
    "Product",
    "Executive Leadership",
    "Marketing Professional",
    "B2B Sales Representative"
]

# Email tone and style guidelines
EMAIL_TONE_GUIDELINES = {
    "tone": "friendly and conversational",
    "style": "20-year-old sales rep",
    "avoid": [
        "corporate jargon",
        "buzzwords like 'synergy', 'leverage', 'ecosystem'",
        "overly formal language",
        "generic templates"
    ],
    "include": [
        "specific company achievements",
        "genuine compliments",
        "clear value proposition",
        "easy call-to-action"
    ]
}

# Research depth by personalization level
RESEARCH_DEPTH = {
    "Basic": {
        "company_info": ["name", "website", "industry"],
        "personalization": "Company name and basic industry info"
    },
    "Medium": {
        "company_info": [
            "name", "website", "industry", "recent_news", 
            "core_business", "company_size"
        ],
        "personalization": "Recent news and achievements"
    },
    "Deep": {
        "company_info": [
            "name", "website", "industry", "recent_news", 
            "core_business", "company_size", "challenges",
            "growth_areas", "technologies", "competitors"
        ],
        "personalization": "Specific pain points and opportunities"
    }
}
