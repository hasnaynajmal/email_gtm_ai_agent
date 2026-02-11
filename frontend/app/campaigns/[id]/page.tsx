"use client";

import { useState, useEffect, useCallback } from "react";
import { useParams, useRouter } from "next/navigation";
import { ArrowLeft, Clock, Building2 } from "lucide-react";
import { CampaignExecutionResponse } from "@/lib/types";
import { getCampaignDetails } from "@/lib/api";
import { Button } from "@/components/ui/Button";
import { Card } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";

import toast from "react-hot-toast";

/**
 * Campaign Detail Page
 * Shows detailed information about a specific campaign
 */
export default function CampaignDetailPage() {
  const params = useParams();
  const router = useRouter();
  const campaignId = params.id as string;

  const [campaign, setCampaign] = useState<CampaignExecutionResponse | null>(
    null,
  );
  const [loading, setLoading] = useState(true);

  const loadCampaignDetails = useCallback(async () => {
    try {
      setLoading(true);
      const data = await getCampaignDetails(campaignId);
      setCampaign(data);
    } catch (error) {
      console.error("Failed to load campaign:", error);
      toast.error("Failed to load campaign details");
    } finally {
      setLoading(false);
    }
  }, [campaignId]);

  useEffect(() => {
    if (campaignId) {
      loadCampaignDetails();
    }
  }, [campaignId, loadCampaignDetails]);

  const getStatusColor = () => {
    // All stored campaigns are completed
    return "success" as const;
  };

  if (loading) {
    return (
      <div className="max-w-7xl mx-auto">
        <div className="flex items-center justify-center py-12">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        </div>
      </div>
    );
  }

  if (!campaign) {
    return (
      <div className="max-w-7xl mx-auto">
        <Card>
          <div className="text-center py-12">
            <h3 className="text-lg font-semibold text-gray-900 mb-2">
              Campaign not found
            </h3>
            <p className="text-gray-600 mb-6">
              The campaign you&apos;re looking for doesn&apos;t exist or has
              been deleted.
            </p>
            <Button onClick={() => router.push("/history")}>
              <ArrowLeft className="w-4 h-4 mr-2" />
              Back to History
            </Button>
          </div>
        </Card>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto">
      {/* Header */}
      <div className="mb-6">
        <Button
          variant="ghost"
          onClick={() => router.push("/history")}
          className="mb-4"
        >
          <ArrowLeft className="w-4 h-4 mr-2" />
          Back to History
        </Button>

        <div className="flex items-start justify-between">
          <div>
            <div className="flex items-center gap-3 mb-2">
              <h1 className="text-3xl font-bold text-gray-900">
                Campaign Results
              </h1>
              <Badge variant={getStatusColor()}>Completed</Badge>
            </div>
            <div className="flex items-center gap-4 text-gray-600">
              <div className="flex items-center gap-2">
                <Clock className="w-4 h-4" />
                Campaign ID: {campaignId}
              </div>
              <div className="flex items-center gap-2">
                <Building2 className="w-4 h-4" />
                {campaign.total_companies} companies
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Campaign Statistics */}
      <Card className="mb-6">
        <div className="p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">
            Campaign Statistics
          </h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
            <div>
              <p className="text-sm text-gray-600 mb-1">Companies Found</p>
              <p className="font-semibold text-gray-900">
                {campaign.total_companies}
              </p>
            </div>
            <div>
              <p className="text-sm text-gray-600 mb-1">Contacts Found</p>
              <p className="font-semibold text-gray-900">
                {campaign.total_contacts}
              </p>
            </div>
            <div>
              <p className="text-sm text-gray-600 mb-1">Emails Generated</p>
              <p className="font-semibold text-gray-900">
                {campaign.total_emails}
              </p>
            </div>
            <div>
              <p className="text-sm text-gray-600 mb-1">Execution Time</p>
              <p className="font-semibold text-gray-900">
                {campaign.execution_time
                  ? `${campaign.execution_time.toFixed(1)}s`
                  : "N/A"}
              </p>
            </div>
          </div>
        </div>
      </Card>

      {/* Results */}
      {campaign.results && campaign.results.length > 0 && (
        <div className="space-y-6">
          {campaign.results.map((result, index) => (
            <Card key={index}>
              <div className="p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">
                  {result.company_info.company_name}
                </h3>
                <div className="text-sm text-gray-600 mb-4">
                  {result.company_info.website_url && (
                    <a
                      href={result.company_info.website_url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-blue-600 hover:underline"
                    >
                      {result.company_info.website_url}
                    </a>
                  )}
                </div>
                <div className="space-y-4">
                  <div>
                    <h4 className="font-medium text-gray-900 mb-2">
                      Contacts ({result.contacts.length})
                    </h4>
                    <div className="space-y-2">
                      {result.contacts.map((contact, cIndex) => (
                        <div key={cIndex} className="text-sm">
                          <p className="font-medium">{contact.name}</p>
                          <p className="text-gray-600">{contact.title}</p>
                          {contact.email && (
                            <p className="text-blue-600">{contact.email}</p>
                          )}
                        </div>
                      ))}
                    </div>
                  </div>
                  <div>
                    <h4 className="font-medium text-gray-900 mb-2">
                      Generated Emails ({result.generated_emails.length})
                    </h4>
                    <div className="space-y-3">
                      {result.generated_emails.map((email, eIndex) => (
                        <div
                          key={eIndex}
                          className="border border-gray-200 rounded p-3"
                        >
                          <p className="font-medium text-sm mb-1">
                            Subject: {email.subject}
                          </p>
                          <div className="text-sm text-gray-700 whitespace-pre-wrap">
                            {email.body}
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
