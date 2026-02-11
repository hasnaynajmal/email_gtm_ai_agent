# Frontend - AI Email GTM Reachout Agent

Next.js 14 frontend with TypeScript and Tailwind CSS.

## Architecture

### App Router Structure

```
app/
├── page.tsx                 # Landing page
├── layout.tsx               # Root layout
├── campaign/
│   ├── new/page.tsx        # Campaign configuration
│   └── execute/page.tsx    # Campaign execution
├── campaigns/
│   └── [id]/page.tsx       # Campaign details
└── history/page.tsx        # Campaign history
```

### Component Library

```
components/
├── ui/                     # Reusable UI components
│   ├── Button.tsx
│   ├── Card.tsx
│   ├── Input.tsx
│   ├── Select.tsx
│   ├── Badge.tsx
│   └── Loading.tsx
├── campaign/               # Campaign-specific
│   ├── ConfigForm.tsx
│   ├── SenderForm.tsx
│   ├── StepIndicator.tsx
│   ├── ExecutionProgress.tsx
│   ├── ResultsDisplay.tsx
│   ├── CompanyCard.tsx
│   ├── EmailCard.tsx
│   ├── CampaignHistoryList.tsx
│   └── StatisticsCards.tsx
└── layout/
    └── Header.tsx          # Navigation header
```

## Setup

### 1. Install Dependencies

```bash
npm install
```

### 2. Configure Environment

Create `.env.local`:

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 3. Run Development Server

```bash
npm run dev
```

Visit http://localhost:3000

## Styling

### Tailwind CSS

- Utility-first CSS framework
- Custom color palette (blue primary)
- Responsive design (mobile-first)
- Component classes in `app/globals.css`

### Design System

- **Colors**: Blue (primary), Gray (neutral), Red (error), Green (success)
- **Typography**: System fonts, clear hierarchy
- **Spacing**: 4px base unit (Tailwind's scale)
- **Components**: Consistent border radius, shadows

## Key Features

### 1. Multi-Step Forms

- Step indicator with progress tracking
- Form validation (client + server)
- Session storage for state persistence

### 2. Real-Time Execution

- Server-Sent Events (SSE) for live updates
- Progress bars and status indicators
- Error handling with retry logic

### 3. Results Display

- Tabbed interface for multiple companies
- Expandable email cards
- Copy-to-clipboard functionality
- Export to text file

### 4. Campaign Management

- Filterable history list
- Statistics dashboard
- Detail view with full results
- Delete campaigns

## API Integration

### API Client (`lib/api.ts`)

```typescript
import { api } from "@/lib/api";

// Get campaign options
const options = await api.getCampaignOptions();

// Execute campaign
const result = await api.executeCampaign(config);

// Get history
const history = await api.getCampaignHistory(10, 0);
```

### TypeScript Types (`lib/types.ts`)

- Full type safety with interfaces
- Matches backend Pydantic models
- Auto-completion in IDE

## Components

### UI Components

#### Button

```tsx
<Button variant="primary" size="md" onClick={handleClick}>
  Click Me
</Button>
```

Variants: `primary` | `secondary` | `outline` | `ghost` | `danger`

#### Card

```tsx
<Card>
  <Card.Header>
    <Card.Title>Title</Card.Title>
  </Card.Header>
  <Card.Content>Content</Card.Content>
</Card>
```

#### Input

```tsx
<Input
  label="Email"
  type="email"
  value={email}
  onChange={(e) => setEmail(e.target.value)}
  error={errors.email}
/>
```

#### Select

```tsx
<Select
  label="Category"
  options={categories}
  value={category}
  onChange={setCategory}
/>
```

### Campaign Components

#### ConfigForm

Step 1 of campaign configuration:

- Category selection
- Department multi-select
- Service type, company size
- Personalization level

#### SenderForm

Step 2 of campaign configuration:

- Sender details (name, email, org)
- Service offering description
- Optional fields (calendar, LinkedIn)

#### ExecutionProgress

Real-time campaign execution:

- Progress bar
- Status messages
- Live statistics

#### ResultsDisplay

Campaign results viewer:

- Company tabs
- Email cards with copy/export
- Summary statistics

## Build & Deploy

### Development

```bash
npm run dev          # Start dev server
npm run lint         # Lint code
npm run format       # Format code
```

### Production Build

```bash
npm run build        # Build for production
npm start            # Start production server
```

### Deploy to Vercel

```bash
vercel deploy --prod
```

Environment variables:

- `NEXT_PUBLIC_API_URL`: Backend API URL

## Pages Guide

### Landing Page (`/`)

- Hero section
- Feature highlights
- CTA button to start campaign

### Campaign Configuration (`/campaign/new`)

- Two-step wizard
- Form validation
- Progress saving in sessionStorage

### Campaign Execution (`/campaign/execute`)

- Real-time SSE streaming
- Live progress updates
- Results display
- Export functionality

### Campaign History (`/history`)

- Statistics cards
- Filterable list
- Quick actions (view, delete)

### Campaign Details (`/campaigns/[id]`)

- Full configuration
- Complete results
- Export options

## Best Practices

### State Management

- Use React hooks (useState, useEffect)
- Session storage for form state
- No global state library needed (keep it simple)

### Error Handling

- Try-catch blocks for async operations
- Toast notifications for user feedback
- Graceful degradation

### Performance

- Code splitting with dynamic imports
- Image optimization (next/image)
- Lazy loading for heavy components

### Accessibility

- Semantic HTML
- ARIA labels
- Keyboard navigation
- Color contrast (WCAG AA)

## Troubleshooting

### Common Issues

**API Connection Failed**

```
Solution: Check NEXT_PUBLIC_API_URL in .env.local
```

**CORS Errors**

```
Solution: Ensure backend CORS_ORIGINS includes http://localhost:3000
```

**Build Errors**

```bash
# Clear cache and rebuild
rm -rf .next
npm run build
```

**TypeScript Errors**

```bash
# Check types
npx tsc --noEmit
```

## Adding New Pages

1. Create page file in `app/[route]/page.tsx`
2. Add 'use client' directive if using hooks
3. Import and use components
4. Add navigation link in Header.tsx

Example:

```tsx
"use client";

import { useState } from "react";
import Button from "@/components/ui/Button";

export default function NewPage() {
  const [state, setState] = useState("");

  return (
    <div className="max-w-7xl mx-auto">
      <h1 className="text-3xl font-bold">New Page</h1>
      <Button onClick={() => setState("clicked")}>Click Me</Button>
    </div>
  );
}
```

## Learning Resources

### Next.js

- [Next.js Documentation](https://nextjs.org/docs)
- [App Router Guide](https://nextjs.org/docs/app)
- [TypeScript Support](https://nextjs.org/docs/app/building-your-application/configuring/typescript)

### React

- [React Hooks](https://react.dev/reference/react)
- [TypeScript with React](https://react.dev/learn/typescript)

### Tailwind CSS

- [Tailwind Documentation](https://tailwindcss.com/docs)
- [Utility Classes](https://tailwindcss.com/docs/utility-first)

---

**Built with Next.js 14 and TypeScript**
