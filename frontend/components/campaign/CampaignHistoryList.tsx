import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { Clock, Mail, Building2, ChevronRight, Trash2 } from "lucide-react";
import { CampaignSummary } from "@/lib/types";
import { getCampaignHistory, deleteCampaign } from "@/lib/api";
import { Card } from "../ui/Card";
import { Button } from "../ui/Button";
import { Badge } from "../ui/Badge";
import toast from "react-hot-toast";

export function CampaignHistoryList() {
  const router = useRouter();
  const [campaigns, setCampaigns] = useState<CampaignSummary[]>([]);
  const [loading, setLoading] = useState(true);
  const [deletingId, setDeletingId] = useState<string | null>(null);

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
      toast.error("Failed to load campaign history");
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (campaignId: string) => {
    if (
      !confirm(
        "Are you sure you want to delete this campaign? This action cannot be undone.",
      )
    ) {
      return;
    }

    try {
      setDeletingId(campaignId);
      await deleteCampaign(campaignId);
      toast.success("Campaign deleted successfully");
      setCampaigns(campaigns.filter((c) => c.campaign_id !== campaignId));
    } catch (error) {
      console.error("Failed to delete campaign:", error);
      toast.error("Failed to delete campaign");
    } finally {
      setDeletingId(null);
    }
  };

  const handleViewDetails = (campaignId: string) => {
    router.push(`/campaigns/${campaignId}`);
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return new Intl.DateTimeFormat("en-US", {
      month: "short",
      day: "numeric",
      year: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    }).format(date);
  };

  const getStatusColor = () => {
    // All campaigns are completed once stored
    return "success" as const;
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (campaigns.length === 0) {
    return (
      <Card>
        <div className="text-center py-12">
          <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <Mail className="w-8 h-8 text-gray-400" />
          </div>
          <h3 className="text-lg font-semibold text-gray-900 mb-2">
            No campaigns yet
          </h3>
          <p className="text-gray-600 mb-6">
            Create your first campaign to start generating personalized outreach
            emails.
          </p>
          <Button onClick={() => router.push("/campaign/new")}>
            Create Campaign
          </Button>
        </div>
      </Card>
    );
  }

  return (
    <div className="space-y-4">
      {campaigns.map((campaign) => (
        <Card
          key={campaign.campaign_id}
          className="hover:shadow-md transition-shadow"
        >
          <div className="flex items-start justify-between">
            <div className="flex-1">
              {/* Campaign Header */}
              <div className="flex items-center gap-3 mb-3">
                <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
                  <Mail className="w-5 h-5 text-blue-600" />
                </div>
                <div>
                  <h3 className="font-semibold text-gray-900">
                    {campaign.metadata.company_category} Campaign
                  </h3>
                  <div className="flex items-center gap-2 text-sm text-gray-500">
                    <Clock className="w-4 h-4" />
                    {formatDate(campaign.created_at)}
                  </div>
                </div>
                <Badge variant={getStatusColor()}>Completed</Badge>
              </div>

              {/* Campaign Details */}
              <div className="grid grid-cols-3 gap-4 mb-4">
                <div>
                  <p className="text-sm text-gray-600 mb-1">Companies</p>
                  <div className="flex items-center gap-2">
                    <Building2 className="w-4 h-4 text-gray-400" />
                    <span className="font-semibold text-gray-900">
                      {campaign.stats.total_companies}
                    </span>
                  </div>
                </div>
                <div>
                  <p className="text-sm text-gray-600 mb-1">Contacts</p>
                  <span className="font-semibold text-gray-900">
                    {campaign.stats.total_contacts}
                  </span>
                </div>
                <div>
                  <p className="text-sm text-gray-600 mb-1">Emails Generated</p>
                  <span className="font-semibold text-gray-900">
                    {campaign.stats.total_emails}
                  </span>
                </div>
              </div>

              {/* Configuration Summary */}
              <div className="flex flex-wrap gap-2">
                <span className="px-2 py-1 bg-gray-100 text-gray-700 rounded text-xs">
                  {campaign.metadata.service_type}
                </span>
                <span className="px-2 py-1 bg-gray-100 text-gray-700 rounded text-xs">
                  {campaign.metadata.num_companies_requested} companies
                  requested
                </span>
              </div>
            </div>

            {/* Actions */}
            <div className="flex gap-2 ml-4">
              <Button
                variant="outline"
                size="sm"
                onClick={() => handleViewDetails(campaign.campaign_id)}
              >
                View Details
                <ChevronRight className="w-4 h-4 ml-1" />
              </Button>
              <Button
                variant="outline"
                size="sm"
                onClick={() => handleDelete(campaign.campaign_id)}
                disabled={deletingId === campaign.campaign_id}
              >
                {deletingId === campaign.campaign_id ? (
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-red-600"></div>
                ) : (
                  <Trash2 className="w-4 h-4 text-red-600" />
                )}
              </Button>
            </div>
          </div>
        </Card>
      ))}
    </div>
  );
}
