/**
 * Campaign Execution Page - Real-time campaign execution with streaming
 */
"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import toast from "react-hot-toast";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { ExecutionProgress } from "@/components/campaign/ExecutionProgress";
import { ResultsDisplay } from "@/components/campaign/ResultsDisplay";
import type { CampaignConfig, CampaignExecutionResponse } from "@/lib/types";

export default function ExecutePage() {
  const router = useRouter();
  const [config, setConfig] = useState<CampaignConfig | null>(null);
  const [isExecuting, setIsExecuting] = useState(false);
  const [results, setResults] = useState<CampaignExecutionResponse | null>(
    null,
  );
  const [error, setError] = useState<string | null>(null);

  // Progress tracking
  const [progress, setProgress] = useState(0);
  const [currentStatus, setCurrentStatus] = useState("");
  const [companiesFound, setCompaniesFound] = useState(0);
  const [contactsFound, setContactsFound] = useState(0);
  const [emailsGenerated, setEmailsGenerated] = useState(0);

  useEffect(() => {
    // Load config from sessionStorage
    const storedConfig = sessionStorage.getItem("campaignConfig");
    if (!storedConfig) {
      toast.error("No campaign configuration found");
      router.push("/campaign/new");
      return;
    }

    try {
      const parsedConfig = JSON.parse(storedConfig);
      setConfig(parsedConfig);
    } catch (err) {
      toast.error("Invalid campaign configuration");
      router.push("/campaign/new");
    }
  }, [router]);

  const executeCampaign = async () => {
    if (!config) return;

    setIsExecuting(true);
    setError(null);
    setProgress(0);
    setCurrentStatus("Initializing...");

    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
      const response = await fetch(`${apiUrl}/api/v1/execute/campaign/stream`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(config),
      });

      if (!response.ok) {
        throw new Error("Failed to start campaign execution");
      }

      const reader = response.body?.getReader();
      const decoder = new TextDecoder();

      if (!reader) {
        throw new Error("No response body");
      }

      let buffer = "";

      while (true) {
        const { done, value } = await reader.read();

        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split("\n");
        buffer = lines.pop() || "";

        for (const line of lines) {
          if (line.startsWith("data: ")) {
            const data = line.slice(6);

            if (data === "[DONE]") {
              continue;
            }

            try {
              const update = JSON.parse(data);

              // Update progress
              if (update.progress !== undefined) {
                setProgress(update.progress);
              }

              if (update.message) {
                setCurrentStatus(update.message);
              }

              // Update stats
              if (update.companies_found !== undefined) {
                setCompaniesFound(update.companies_found);
              }
              if (update.contacts_found !== undefined) {
                setContactsFound(update.contacts_found);
              }
              if (update.emails_generated !== undefined) {
                setEmailsGenerated(update.emails_generated);
              }

              // Check for completion
              if (update.status === "completed" && update.results) {
                setResults({
                  results: update.results,
                  total_companies: update.results.length,
                  total_contacts: update.total_contacts || 0,
                  total_emails: update.total_emails || 0,
                  execution_time: update.execution_time,
                });
              }

              // Check for errors
              if (update.status === "error") {
                throw new Error(update.message || "Campaign execution failed");
              }
            } catch (parseError) {
              console.error("Failed to parse update:", parseError);
            }
          }
        }
      }

      toast.success("Campaign completed successfully!");
    } catch (err: any) {
      console.error("Execution error:", err);
      setError(err.message || "Failed to execute campaign");
      toast.error(err.message || "Campaign execution failed");
    } finally {
      setIsExecuting(false);
    }
  };

  const handleStartNew = () => {
    sessionStorage.removeItem("campaignConfig");
    router.push("/campaign/new");
  };

  if (!config) {
    return null;
  }

  return (
    <div className="max-w-6xl mx-auto space-y-6">
      {/* Header */}
      <div className="flex justify-between items-start">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Campaign Execution
          </h1>
          <p className="text-gray-600">
            Targeting {config.num_companies}{" "}
            {config.outreach_config.company_category} companies
          </p>
        </div>
        {results && (
          <Button onClick={handleStartNew} variant="outline">
            Start New Campaign
          </Button>
        )}
      </div>

      {/* Configuration Summary */}
      {!isExecuting && !results && (
        <Card padding="lg">
          <div className="space-y-4">
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-3">
                Campaign Configuration
              </h3>
              <div className="grid md:grid-cols-2 gap-4 text-sm">
                <div>
                  <span className="font-medium text-gray-700">Category:</span>
                  <span className="ml-2 text-gray-600">
                    {config.outreach_config.company_category}
                  </span>
                </div>
                <div>
                  <span className="font-medium text-gray-700">
                    Departments:
                  </span>
                  <span className="ml-2 text-gray-600">
                    {config.outreach_config.target_departments.join(", ")}
                  </span>
                </div>
                <div>
                  <span className="font-medium text-gray-700">
                    Service Type:
                  </span>
                  <span className="ml-2 text-gray-600">
                    {config.outreach_config.service_type}
                  </span>
                </div>
                <div>
                  <span className="font-medium text-gray-700">
                    Company Size:
                  </span>
                  <span className="ml-2 text-gray-600">
                    {config.outreach_config.company_size_preference}
                  </span>
                </div>
                <div>
                  <span className="font-medium text-gray-700">
                    Personalization:
                  </span>
                  <span className="ml-2 text-gray-600">
                    {config.outreach_config.personalization_level}
                  </span>
                </div>
                <div>
                  <span className="font-medium text-gray-700">Companies:</span>
                  <span className="ml-2 text-gray-600">
                    {config.num_companies}
                  </span>
                </div>
              </div>
            </div>

            <div className="pt-4 border-t border-gray-200">
              <h4 className="font-medium text-gray-900 mb-2">
                Sender Information
              </h4>
              <div className="text-sm text-gray-600">
                <p>
                  {config.sender_details.name} from{" "}
                  {config.sender_details.organization}
                </p>
                <p className="text-xs text-gray-500 mt-1">
                  {config.sender_details.service_offered}
                </p>
              </div>
            </div>

            <Button onClick={executeCampaign} size="lg" className="w-full">
              🚀 Execute Campaign
            </Button>
          </div>
        </Card>
      )}

      {/* Execution Progress */}
      {isExecuting && (
        <ExecutionProgress
          progress={progress}
          status={currentStatus}
          companiesFound={companiesFound}
          contactsFound={contactsFound}
          emailsGenerated={emailsGenerated}
        />
      )}

      {/* Error Display */}
      {error && (
        <Card>
          <div className="bg-red-50 border border-red-200 rounded-lg p-4">
            <div className="flex items-start">
              <svg
                className="w-5 h-5 text-red-600 mt-0.5"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                />
              </svg>
              <div className="ml-3">
                <h3 className="text-sm font-medium text-red-800">
                  Campaign Execution Failed
                </h3>
                <p className="mt-1 text-sm text-red-700">{error}</p>
              </div>
            </div>
            <div className="mt-4 flex gap-2">
              <Button onClick={executeCampaign} variant="secondary" size="sm">
                Try Again
              </Button>
              <Button onClick={handleStartNew} variant="outline" size="sm">
                Start New Campaign
              </Button>
            </div>
          </div>
        </Card>
      )}

      {/* Results Display */}
      {results && (
        <ResultsDisplay
          results={results}
          senderDetails={config.sender_details}
        />
      )}
    </div>
  );
}
