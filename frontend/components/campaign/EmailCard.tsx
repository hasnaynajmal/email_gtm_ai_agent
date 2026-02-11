/**
 * Email Display Card with Copy Functionality
 */
import { useState } from "react";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { copyToClipboard } from "@/lib/utils";
import toast from "react-hot-toast";
import type { ContactInfo, GeneratedEmail, SenderDetails } from "@/lib/types";

interface EmailCardProps {
  contact: ContactInfo;
  email: GeneratedEmail;
  senderDetails: SenderDetails;
}

export function EmailCard({ contact, email, senderDetails }: EmailCardProps) {
  const [showFullEmail, setShowFullEmail] = useState(false);

  const fullEmailContent = `Subject: ${email.subject}

${email.body}

Best regards,
${senderDetails.name}
${senderDetails.organization}
${senderDetails.email}${senderDetails.phone ? `\n${senderDetails.phone}` : ""}${senderDetails.website ? `\n${senderDetails.website}` : ""}${senderDetails.linkedin ? `\nLinkedIn: ${senderDetails.linkedin}` : ""}${senderDetails.calendar_link ? `\nSchedule a call: ${senderDetails.calendar_link}` : ""}`;

  const handleCopyEmail = async () => {
    const success = await copyToClipboard(fullEmailContent);
    if (success) {
      toast.success("Email copied to clipboard!");
    } else {
      toast.error("Failed to copy email");
    }
  };

  const handleCopySubject = async () => {
    const success = await copyToClipboard(email.subject);
    if (success) {
      toast.success("Subject copied!");
    }
  };

  const handleCopyBody = async () => {
    const bodyWithSignature = `${email.body}

Best regards,
${senderDetails.name}
${senderDetails.organization}
${senderDetails.email}${senderDetails.phone ? `\n${senderDetails.phone}` : ""}${senderDetails.website ? `\n${senderDetails.website}` : ""}${senderDetails.linkedin ? `\nLinkedIn: ${senderDetails.linkedin}` : ""}${senderDetails.calendar_link ? `\nSchedule a call: ${senderDetails.calendar_link}` : ""}`;

    const success = await copyToClipboard(bodyWithSignature);
    if (success) {
      toast.success("Email body copied!");
    }
  };

  return (
    <Card className="border-l-4 border-l-blue-500">
      <div className="p-6 space-y-4">
        {/* Contact Header */}
        <div className="flex justify-between items-start">
          <div>
            <h3 className="text-lg font-semibold text-gray-900">
              {contact.name}
            </h3>
            <p className="text-sm text-gray-600">{contact.title}</p>
            <div className="flex gap-3 mt-2 text-sm">
              {contact.email && (
                <a
                  href={`mailto:${contact.email}`}
                  className="text-blue-600 hover:underline"
                >
                  {contact.email}
                </a>
              )}
              {contact.linkedin && (
                <a
                  href={contact.linkedin}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-blue-600 hover:underline"
                >
                  LinkedIn
                </a>
              )}
            </div>
          </div>
          {contact.department && (
            <Badge variant="info">{contact.department}</Badge>
          )}
        </div>

        {/* Email Subject */}
        <div className="bg-gray-50 rounded-lg p-4">
          <div className="flex justify-between items-start gap-2">
            <div className="flex-1">
              <p className="text-xs font-medium text-gray-500 mb-1">SUBJECT</p>
              <p className="text-sm font-semibold text-gray-900">
                {email.subject}
              </p>
            </div>
            <Button onClick={handleCopySubject} variant="ghost" size="sm">
              📋
            </Button>
          </div>
        </div>

        {/* Email Body Preview */}
        <div>
          <p className="text-xs font-medium text-gray-500 mb-2">EMAIL BODY</p>
          <div className="bg-white border border-gray-200 rounded-lg p-4">
            <pre className="whitespace-pre-wrap font-sans text-sm text-gray-800">
              {showFullEmail
                ? fullEmailContent
                : email.body.slice(0, 300) +
                  (email.body.length > 300 ? "..." : "")}
            </pre>
            {email.body.length > 300 && (
              <button
                onClick={() => setShowFullEmail(!showFullEmail)}
                className="text-blue-600 hover:underline text-sm mt-2"
              >
                {showFullEmail ? "Show less" : "Show more"}
              </button>
            )}
          </div>
        </div>

        {/* Personalization Notes */}
        {email.personalization_notes && (
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-3">
            <p className="text-xs font-medium text-blue-900 mb-1">
              💡 PERSONALIZATION INSIGHTS
            </p>
            <p className="text-sm text-blue-800">
              {email.personalization_notes}
            </p>
          </div>
        )}

        {/* Action Buttons */}
        <div className="flex gap-2 pt-2">
          <Button
            onClick={handleCopyEmail}
            variant="primary"
            size="sm"
            className="flex-1"
          >
            📋 Copy Full Email
          </Button>
          <Button onClick={handleCopyBody} variant="outline" size="sm">
            Copy Body
          </Button>
        </div>
      </div>
    </Card>
  );
}
