/**
 * Company Information Card
 */
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import type { CompanyInfo } from "@/lib/types";

interface CompanyCardProps {
  company: CompanyInfo;
}

export function CompanyCard({ company }: CompanyCardProps) {
  return (
    <Card>
      <CardHeader>
        <div className="flex justify-between items-start">
          <div>
            <CardTitle>{company.company_name}</CardTitle>
            <a
              href={company.website_url}
              target="_blank"
              rel="noopener noreferrer"
              className="text-sm text-blue-600 hover:underline"
            >
              {company.website_url}
            </a>
          </div>
          {company.company_size && (
            <Badge variant="default">{company.company_size}</Badge>
          )}
        </div>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {/* Core Business */}
          {company.core_business && (
            <div>
              <h4 className="text-sm font-semibold text-gray-900 mb-1">
                Core Business
              </h4>
              <p className="text-sm text-gray-700">{company.core_business}</p>
            </div>
          )}

          {/* Value Proposition */}
          {company.value_proposition && (
            <div>
              <h4 className="text-sm font-semibold text-gray-900 mb-1">
                Value Proposition
              </h4>
              <p className="text-sm text-gray-700">
                {company.value_proposition}
              </p>
            </div>
          )}

          {/* Key Info Grid */}
          <div className="grid md:grid-cols-2 gap-4 pt-2">
            {company.industry && (
              <div>
                <span className="text-xs font-medium text-gray-500">
                  Industry
                </span>
                <p className="text-sm text-gray-900 mt-0.5">
                  {company.industry}
                </p>
              </div>
            )}
            {company.founded_year && (
              <div>
                <span className="text-xs font-medium text-gray-500">
                  Founded
                </span>
                <p className="text-sm text-gray-900 mt-0.5">
                  {company.founded_year}
                </p>
              </div>
            )}
            {company.locations && company.locations.length > 0 && (
              <div>
                <span className="text-xs font-medium text-gray-500">
                  Locations
                </span>
                <p className="text-sm text-gray-900 mt-0.5">
                  {company.locations.join(", ")}
                </p>
              </div>
            )}
            {company.funding_status && (
              <div>
                <span className="text-xs font-medium text-gray-500">
                  Funding
                </span>
                <p className="text-sm text-gray-900 mt-0.5">
                  {company.funding_status}
                </p>
              </div>
            )}
          </div>

          {/* Technologies */}
          {company.technologies && company.technologies.length > 0 && (
            <div>
              <h4 className="text-xs font-medium text-gray-500 mb-2">
                Technologies
              </h4>
              <div className="flex flex-wrap gap-1">
                {company.technologies.slice(0, 10).map((tech, index) => (
                  <Badge key={index} variant="default" className="text-xs">
                    {tech}
                  </Badge>
                ))}
              </div>
            </div>
          )}

          {/* Recent News */}
          {company.recent_news && company.recent_news.length > 0 && (
            <div>
              <h4 className="text-sm font-semibold text-gray-900 mb-2">
                Recent News
              </h4>
              <ul className="space-y-1">
                {company.recent_news.slice(0, 3).map((news, index) => (
                  <li
                    key={index}
                    className="text-sm text-gray-700 flex items-start"
                  >
                    <span className="text-blue-600 mr-2">•</span>
                    <span>{news}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Challenges */}
          {company.challenges && company.challenges.length > 0 && (
            <div>
              <h4 className="text-sm font-semibold text-gray-900 mb-2">
                Identified Challenges
              </h4>
              <ul className="space-y-1">
                {company.challenges.slice(0, 3).map((challenge, index) => (
                  <li
                    key={index}
                    className="text-sm text-gray-700 flex items-start"
                  >
                    <span className="text-orange-600 mr-2">•</span>
                    <span>{challenge}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  );
}
