/**
 * Campaign Results Display Component
 */
import { useState } from "react";
import {
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
} from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { CompanyCard } from "./CompanyCard";
import { EmailCard } from "./EmailCard";
import { formatExecutionTime, downloadAsFile } from "@/lib/utils";
import type { CampaignExecutionResponse, SenderDetails } from "@/lib/types";

interface ResultsDisplayProps {
  results: CampaignExecutionResponse;
  senderDetails: SenderDetails;
}

export function ResultsDisplay({
  results,
  senderDetails,
}: ResultsDisplayProps) {
  const [selectedCompanyIndex, setSelectedCompanyIndex] = useState(0);

  const selectedResult = results.results[selectedCompanyIndex];

  const exportAllEmails = () => {
    let content = `Campaign Results - ${new Date().toLocaleDateString()}\n`;
    content += `Total Companies: ${results.total_companies}\n`;
    content += `Total Contacts: ${results.total_contacts}\n`;
    content += `Total Emails: ${results.total_emails}\n`;
    if (results.execution_time) {
      content += `Execution Time: ${formatExecutionTime(results.execution_time)}\n`;
    }
    content += `\n${"=".repeat(80)}\n\n`;

    results.results.forEach((result, index) => {
      content += `\n\n${"=".repeat(80)}\n`;
      content += `COMPANY ${index + 1}: ${result.company_info.company_name}\n`;
      content += `${"=".repeat(80)}\n\n`;
      content += `Website: ${result.company_info.website_url}\n`;
      if (result.company_info.industry) {
        content += `Industry: ${result.company_info.industry}\n`;
      }
      content += `\n`;

      result.contacts.forEach((contact, contactIndex) => {
        content += `\n${"-".repeat(60)}\n`;
        content += `Contact ${contactIndex + 1}: ${contact.name}\n`;
        content += `Title: ${contact.title}\n`;
        if (contact.email) content += `Email: ${contact.email}\n`;
        if (contact.linkedin) content += `LinkedIn: ${contact.linkedin}\n`;
        content += `${"-".repeat(60)}\n\n`;

        if (result.generated_emails[contactIndex]) {
          const email = result.generated_emails[contactIndex];
          content += `Subject: ${email.subject}\n\n`;
          content += `${email.body}\n\n`;
          if (email.personalization_notes) {
            content += `Personalization Notes:\n${email.personalization_notes}\n\n`;
          }
        }
      });
    });

    downloadAsFile(content, `campaign-results-${Date.now()}.txt`);
  };

  return (
    <div className="space-y-6">
      {/* Summary Stats */}
      <Card>
        <div className="grid md:grid-cols-4 gap-6">
          <div className="text-center">
            <div className="text-3xl font-bold text-blue-600">
              {results.total_companies}
            </div>
            <div className="text-sm text-gray-600 mt-1">Companies</div>
          </div>
          <div className="text-center">
            <div className="text-3xl font-bold text-green-600">
              {results.total_contacts}
            </div>
            <div className="text-sm text-gray-600 mt-1">Contacts</div>
          </div>
          <div className="text-center">
            <div className="text-3xl font-bold text-purple-600">
              {results.total_emails}
            </div>
            <div className="text-sm text-gray-600 mt-1">Emails</div>
          </div>
          <div className="text-center">
            <div className="text-3xl font-bold text-orange-600">
              {results.execution_time
                ? formatExecutionTime(results.execution_time)
                : "N/A"}
            </div>
            <div className="text-sm text-gray-600 mt-1">Duration</div>
          </div>
        </div>
      </Card>

      {/* Actions */}
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold text-gray-900">Campaign Results</h2>
        <Button onClick={exportAllEmails} variant="outline">
          📥 Export All Emails
        </Button>
      </div>

      {/* Company Selector */}
      <div className="flex gap-2 overflow-x-auto pb-2">
        {results.results.map((result, index) => (
          <button
            key={index}
            onClick={() => setSelectedCompanyIndex(index)}
            className={`flex-shrink-0 px-4 py-2 rounded-lg border-2 transition-colors ${
              selectedCompanyIndex === index
                ? "border-blue-600 bg-blue-50 text-blue-900"
                : "border-gray-200 bg-white text-gray-600 hover:border-gray-300"
            }`}
          >
            <div className="text-sm font-medium">
              {result.company_info.company_name}
            </div>
            <div className="text-xs text-gray-500 mt-0.5">
              {result.contacts.length} contact
              {result.contacts.length !== 1 ? "s" : ""}
            </div>
          </button>
        ))}
      </div>

      {/* Selected Company Details */}
      {selectedResult && (
        <div className="space-y-6">
          {/* Company Info */}
          <CompanyCard company={selectedResult.company_info} />

          {/* Contacts & Emails */}
          <div>
            <CardHeader>
              <CardTitle>
                Generated Emails
                <Badge variant="info" className="ml-2">
                  {selectedResult.generated_emails.length} email
                  {selectedResult.generated_emails.length !== 1 ? "s" : ""}
                </Badge>
              </CardTitle>
              <CardDescription>
                Personalized emails for each decision maker
              </CardDescription>
            </CardHeader>

            <div className="space-y-4 mt-4">
              {selectedResult.contacts.map((contact, index) => (
                <EmailCard
                  key={index}
                  contact={contact}
                  email={selectedResult.generated_emails[index]}
                  senderDetails={senderDetails}
                />
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
