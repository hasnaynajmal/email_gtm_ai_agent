export default function Home() {
  return (
    <div className="space-y-6">
      {/* Hero Section */}
      <div className="text-center py-12 bg-white rounded-lg shadow-md">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">
          AI Email GTM Outreach Agent
        </h1>
        <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
          Automated B2B cold email outreach powered by AI. Find companies,
          research prospects, and generate personalized emails at scale.
        </p>
        <div className="flex justify-center gap-4">
          <a
            href="/campaign/new"
            className="bg-blue-600 text-white px-6 py-3 rounded-lg font-medium hover:bg-blue-700 transition-colors"
          >
            Create Campaign
          </a>
          <a
            href="/history"
            className="border-2 border-gray-300 text-gray-700 px-6 py-3 rounded-lg font-medium hover:bg-gray-50 transition-colors"
          >
            View History
          </a>
        </div>
      </div>

      {/* Features Grid */}
      <div className="grid md:grid-cols-3 gap-6">
        <div className="bg-white p-6 rounded-lg shadow-md">
          <div className="bg-blue-100 w-12 h-12 rounded-lg flex items-center justify-center mb-4">
            <svg
              className="w-6 h-6 text-blue-600"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
              />
            </svg>
          </div>
          <h3 className="text-lg font-semibold text-gray-900 mb-2">
            Company Discovery
          </h3>
          <p className="text-gray-600">
            Powered by Exa AI to find relevant companies matching your target
            criteria
          </p>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-md">
          <div className="bg-green-100 w-12 h-12 rounded-lg flex items-center justify-center mb-4">
            <svg
              className="w-6 h-6 text-green-600"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
              />
            </svg>
          </div>
          <h3 className="text-lg font-semibold text-gray-900 mb-2">
            Deep Research
          </h3>
          <p className="text-gray-600">
            Gather comprehensive intelligence on each company and decision maker
          </p>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-md">
          <div className="bg-purple-100 w-12 h-12 rounded-lg flex items-center justify-center mb-4">
            <svg
              className="w-6 h-6 text-purple-600"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"
              />
            </svg>
          </div>
          <h3 className="text-lg font-semibold text-gray-900 mb-2">
            Personalized Emails
          </h3>
          <p className="text-gray-600">
            Generate highly personalized cold emails based on research insights
          </p>
        </div>
      </div>

      {/* Quick Start Guide */}
      <div className="bg-white p-8 rounded-lg shadow-md">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">How It Works</h2>
        <div className="space-y-4">
          <div className="flex gap-4">
            <div className="bg-blue-600 text-white w-8 h-8 rounded-full flex items-center justify-center font-bold flex-shrink-0">
              1
            </div>
            <div>
              <h3 className="font-semibold text-gray-900 mb-1">
                Configure Campaign
              </h3>
              <p className="text-gray-600">
                Select your target company category, departments, and
                personalization level
              </p>
            </div>
          </div>
          <div className="flex gap-4">
            <div className="bg-blue-600 text-white w-8 h-8 rounded-full flex items-center justify-center font-bold flex-shrink-0">
              2
            </div>
            <div>
              <h3 className="font-semibold text-gray-900 mb-1">
                Add Your Details
              </h3>
              <p className="text-gray-600">
                Provide sender information and service offering for email
                customization
              </p>
            </div>
          </div>
          <div className="flex gap-4">
            <div className="bg-blue-600 text-white w-8 h-8 rounded-full flex items-center justify-center font-bold flex-shrink-0">
              3
            </div>
            <div>
              <h3 className="font-semibold text-gray-900 mb-1">
                Execute & Review
              </h3>
              <p className="text-gray-600">
                Run the campaign and review generated emails before sending
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
