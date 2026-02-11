/**
 * Campaign Execution Progress Component
 */
import { Card } from "@/components/ui/Card";
import { LoadingSpinner } from "@/components/ui/Loading";

interface ExecutionProgressProps {
  progress: number;
  status: string;
  companiesFound: number;
  contactsFound: number;
  emailsGenerated: number;
}

export function ExecutionProgress({
  progress,
  status,
  companiesFound,
  contactsFound,
  emailsGenerated,
}: ExecutionProgressProps) {
  return (
    <Card padding="lg">
      <div className="space-y-6">
        {/* Status */}
        <div className="flex items-center gap-3">
          <LoadingSpinner size="md" />
          <div>
            <h3 className="text-lg font-semibold text-gray-900">
              Executing Campaign
            </h3>
            <p className="text-sm text-gray-600">{status}</p>
          </div>
        </div>

        {/* Progress Bar */}
        <div>
          <div className="flex justify-between text-sm font-medium text-gray-700 mb-2">
            <span>Progress</span>
            <span>{Math.round(progress)}%</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-3 overflow-hidden">
            <div
              className="bg-blue-600 h-full rounded-full transition-all duration-300 ease-out"
              style={{ width: `${progress}%` }}
            />
          </div>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-3 gap-4">
          <div className="bg-blue-50 rounded-lg p-4 text-center">
            <div className="text-3xl font-bold text-blue-600">
              {companiesFound}
            </div>
            <div className="text-sm text-gray-600 mt-1">Companies Found</div>
          </div>
          <div className="bg-green-50 rounded-lg p-4 text-center">
            <div className="text-3xl font-bold text-green-600">
              {contactsFound}
            </div>
            <div className="text-sm text-gray-600 mt-1">Contacts Found</div>
          </div>
          <div className="bg-purple-50 rounded-lg p-4 text-center">
            <div className="text-3xl font-bold text-purple-600">
              {emailsGenerated}
            </div>
            <div className="text-sm text-gray-600 mt-1">Emails Generated</div>
          </div>
        </div>

        {/* Info */}
        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
          <p className="text-sm text-yellow-800">
            ⏳ This may take a few minutes depending on the number of companies
            and personalization level...
          </p>
        </div>
      </div>
    </Card>
  );
}
