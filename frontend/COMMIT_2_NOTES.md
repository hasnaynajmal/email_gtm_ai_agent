# Frontend - UI Components & Design System

This commit establishes the foundational design system and reusable components for the AI Email GTM Agent frontend.

## What's Created

### Configuration Files

- `.env.local.example` - Environment variable template for API URL
- `next.config.ts` - Next.js configuration with API URL injection

### Type Definitions (`lib/types.ts`)

Complete TypeScript interfaces matching backend Pydantic schemas:

- Campaign configuration types (OutreachConfig, SenderDetails, CampaignConfig)
- Company and contact types (CompanyInfo, ContactInfo)
- Email generation types (GeneratedEmail)
- Campaign results and execution responses
- Campaign history and options
- Progress updates for streaming

### API Client (`lib/api.ts`)

Axios-based API client with:

- Base URL configuration from environment
- Health check endpoint
- Campaign configuration endpoints
- Campaign execution functions
- Campaign history management
- Typed responses using lib/types.ts

### Utility Functions (`lib/utils.ts`)

Helper functions for:

- Time formatting (formatExecutionTime)
- Date formatting (formatDate)
- Clipboard operations (copyToClipboard)
- File downloads (downloadAsFile)
- Email validation (isValidEmail)
- Text truncation and initials generation

### UI Components (`components/ui/`)

Reusable components built with Tailwind CSS:

- **Button.tsx** - Primary, secondary, outline, ghost, danger variants with loading states
- **Card.tsx** - Card container with Header, Title, Description, Content sub-components
- **Input.tsx** - Text input and Textarea with labels, errors, helper text
- **Select.tsx** - Single-select and MultiSelect (checkbox-based) dropdowns
- **Loading.tsx** - LoadingSpinner and LoadingPage components
- **Badge.tsx** - Label badges with success, warning, error, info variants

### Layout Components (`components/layout/`)

- **Header.tsx** - Navigation header with logo, active link highlighting, and routing to:
  - "/" - New Campaign
  - "/history" - Campaign History

### Pages

- **app/layout.tsx** - Root layout with Header, Toaster (react-hot-toast), and Inter font
- **app/page.tsx** - Landing page with:
  - Hero section explaining the product
  - Feature cards (Company Discovery, Deep Research, Personalized Emails)
  - "How It Works" 3-step guide
  - Call-to-action buttons

## Next.js Concepts Explained

### App Router

- Uses `app/` directory (not `pages/`)
- File-based routing: `app/page.tsx` → `/`, `app/campaign/new/page.tsx` → `/campaign/new`
- Layout nesting: `app/layout.tsx` wraps all pages

### TypeScript

- Interfaces define data shapes (compile-time type checking)
- `React.FC<Props>` or function with typed props
- Import types with `import type { ... }`

### Tailwind CSS

- Utility-first CSS: `bg-blue-600 text-white px-4 py-2`
- Responsive: `md:grid-cols-3` (3 columns on medium+ screens)
- Hover states: `hover:bg-blue-700`

### Component Pattern

```typescript
interface ComponentProps {
  variant?: 'primary' | 'secondary';
  children: React.ReactNode;
}

export function Component({ variant = 'primary', children }: ComponentProps) {
  return <div className={styles[variant]}>{children}</div>;
}
```

## Usage Example

```tsx
import { Button } from "@/components/ui/Button";
import { Card, CardHeader, CardTitle } from "@/components/ui/Card";

<Card>
  <CardHeader>
    <CardTitle>Campaign Setup</CardTitle>
  </CardHeader>
  <Button variant="primary" isLoading={loading}>
    Submit
  </Button>
</Card>;
```

## Next Steps

- Commit 3: Create campaign configuration page with multi-step form
- Commit 4: Build campaign execution and results display
- Commit 5: Implement campaign history and final polish
