import { Mail, Building2, Users, TrendingUp } from "lucide-react";
import { Card } from "../ui/Card";

interface StatisticsCardsProps {
  totalCampaigns: number;
  totalCompanies: number;
  totalContacts: number;
  totalEmails: number;
}

export function StatisticsCards({
  totalCampaigns,
  totalCompanies,
  totalContacts,
  totalEmails,
}: StatisticsCardsProps) {
  const stats = [
    {
      label: "Total Campaigns",
      value: totalCampaigns,
      icon: TrendingUp,
      color: "blue",
    },
    {
      label: "Companies Discovered",
      value: totalCompanies,
      icon: Building2,
      color: "green",
    },
    {
      label: "Contacts Found",
      value: totalContacts,
      icon: Users,
      color: "purple",
    },
    {
      label: "Emails Generated",
      value: totalEmails,
      icon: Mail,
      color: "orange",
    },
  ];

  const getColorClasses = (color: string) => {
    const colors = {
      blue: "bg-blue-100 text-blue-600",
      green: "bg-green-100 text-green-600",
      purple: "bg-purple-100 text-purple-600",
      orange: "bg-orange-100 text-orange-600",
    };
    return colors[color as keyof typeof colors] || colors.blue;
  };

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
      {stats.map((stat) => {
        const Icon = stat.icon;
        const colorClasses = getColorClasses(stat.color);

        return (
          <Card key={stat.label}>
            <div className="flex items-center gap-4">
              <div
                className={`w-12 h-12 rounded-lg flex items-center justify-center ${colorClasses}`}
              >
                <Icon className="w-6 h-6" />
              </div>
              <div>
                <p className="text-sm text-gray-600 mb-1">{stat.label}</p>
                <p className="text-2xl font-bold text-gray-900">
                  {stat.value.toLocaleString()}
                </p>
              </div>
            </div>
          </Card>
        );
      })}
    </div>
  );
}
