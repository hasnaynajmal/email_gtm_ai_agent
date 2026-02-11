/**
 * Sender Details Form - Step 2
 */
import { Input, Textarea } from '@/components/ui/Input';
import type { SenderDetails } from '@/lib/types';

interface SenderFormProps {
  details: SenderDetails;
  onChange: (details: SenderDetails) => void;
}

export function SenderForm({ details, onChange }: SenderFormProps) {
  return (
    <div className="space-y-6">
      {/* Required Fields */}
      <div className="pb-4 border-b border-gray-200">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Required Information</h3>
        
        <div className="space-y-4">
          <Input
            label="Your Name"
            required
            value={details.name}
            onChange={(e) => onChange({ ...details, name: e.target.value })}
            placeholder="John Doe"
          />

          <Input
            type="email"
            label="Your Email"
            required
            value={details.email}
            onChange={(e) => onChange({ ...details, email: e.target.value })}
            placeholder="john@company.com"
            helperText="This will be included in email signatures"
          />

          <Input
            label="Organization"
            required
            value={details.organization}
            onChange={(e) => onChange({ ...details, organization: e.target.value })}
            placeholder="Your Company Inc."
          />

          <Textarea
            label="Service Offered"
            required
            value={details.service_offered}
            onChange={(e) => onChange({ ...details, service_offered: e.target.value })}
            placeholder="Describe what you're offering (e.g., 'AI-powered analytics platform for e-commerce')"
            rows={3}
            helperText="Be specific - this helps generate more relevant emails"
          />
        </div>
      </div>

      {/* Optional Fields */}
      <div>
        <h3 className="text-lg font-semibold text-gray-900 mb-2">
          Optional Information
          <span className="text-sm font-normal text-gray-500 ml-2">
            (Improves email personalization)
          </span>
        </h3>
        <p className="text-sm text-gray-600 mb-4">
          Adding these details will make your emails more professional and actionable
        </p>

        <div className="space-y-4">
          <Input
            type="url"
            label="Calendar Link"
            value={details.calendar_link || ''}
            onChange={(e) => onChange({ ...details, calendar_link: e.target.value })}
            placeholder="https://calendly.com/yourname"
            helperText="Calendly, Cal.com, or any scheduling link"
          />

          <Input
            type="url"
            label="LinkedIn Profile"
            value={details.linkedin || ''}
            onChange={(e) => onChange({ ...details, linkedin: e.target.value })}
            placeholder="https://linkedin.com/in/yourname"
          />

          <Input
            type="tel"
            label="Phone Number"
            value={details.phone || ''}
            onChange={(e) => onChange({ ...details, phone: e.target.value })}
            placeholder="+1 (555) 123-4567"
          />

          <Input
            type="url"
            label="Website"
            value={details.website || ''}
            onChange={(e) => onChange({ ...details, website: e.target.value })}
            placeholder="https://yourcompany.com"
          />
        </div>
      </div>

      {/* Preview */}
      <div className="bg-gray-50 p-4 rounded-lg border border-gray-200">
        <h4 className="text-sm font-semibold text-gray-700 mb-2">Email Signature Preview</h4>
        <div className="text-sm text-gray-900 space-y-1">
          <p className="font-medium">{details.name || 'Your Name'}</p>
          <p>{details.organization || 'Your Organization'}</p>
          {details.email && <p className="text-blue-600">{details.email}</p>}
          {details.phone && <p>{details.phone}</p>}
          {details.website && (
            <p>
              <a href={details.website} className="text-blue-600 hover:underline">
                {details.website.replace(/^https?:\/\//, '')}
              </a>
            </p>
          )}
          {details.linkedin && (
            <p>
              <a href={details.linkedin} className="text-blue-600 hover:underline">
                LinkedIn Profile
              </a>
            </p>
          )}
          {details.calendar_link && (
            <p>
              <a href={details.calendar_link} className="text-blue-600 hover:underline">
                Schedule a Meeting
              </a>
            </p>
          )}
        </div>
      </div>
    </div>
  );
}
