"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { Plus } from "lucide-react";
import { CampaignSummary } from "@/lib/types";
import { getCampaignHistory } from "@/lib/api";
import { Button } from "@/components/ui/Button";
import { StatisticsCards } from "@/components/campaign/StatisticsCards";
import { CampaignHistoryList } from "@/components/campaign/CampaignHistoryList";

/**
 * Campaign History Page
 * Displays all past campaigns with statistics and details
 */
export default function HistoryPage() {
  const router = useRouter();
  const [campaigns, setCampaigns] = useState<CampaignSummary[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadCampaigns();
  }, []);

  const loadCampaigns = async () => {
    try {
      setLoading(true);
      const data = await getCampaignHistory();
      setCampaigns(data);
    } catch (error) {
      console.error("Failed to load campaigns:", error);
    } finally {
      setLoading(false);
    }
  };

  const calculateStats = () => {
    return {
      totalCampaigns: campaigns.length,
      totalCompanies: campaigns.reduce(
        (sum, c) => sum + c.stats.total_companies,
        0,
      ),
      totalContacts: campaigns.reduce(
        (sum, c) => sum + c.stats.total_contacts,
        0,
      ),
      totalEmails: campaigns.reduce((sum, c) => sum + c.stats.total_emails, 0),
    };
  };

  const stats = calculateStats();

  return (
    <div className="max-w-7xl mx-auto">
      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Campaign History
          </h1>
          <p className="text-gray-600">
            View and manage all your past outreach campaigns
          </p>
        </div>
        <Button onClick={() => router.push("/campaign/new")}>
          <Plus className="w-5 h-5 mr-2" />
          New Campaign
        </Button>
      </div>

      {/* Statistics */}
      {!loading && campaigns.length > 0 && (
        <StatisticsCards
          totalCampaigns={stats.totalCampaigns}
          totalCompanies={stats.totalCompanies}
          totalContacts={stats.totalContacts}
          totalEmails={stats.totalEmails}
        />
      )}

      {/* Campaign List */}
      <CampaignHistoryList />
    </div>
  );
}
