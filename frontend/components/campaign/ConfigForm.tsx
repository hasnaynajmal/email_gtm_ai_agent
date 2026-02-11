/**
 * Campaign Configuration Form - Step 1
 */
import { Select, MultiSelect } from "@/components/ui/Select";
import { Input } from "@/components/ui/Input";
import type { OutreachConfig, CampaignOptionsResponse } from "@/lib/types";

interface ConfigFormProps {
  config: OutreachConfig;
  onChange: (config: OutreachConfig) => void;
  numCompanies: number;
  onNumCompaniesChange: (num: number) => void;
  options: CampaignOptionsResponse;
}

export function ConfigForm({
  config,
  onChange,
  numCompanies,
  onNumCompaniesChange,
  options,
}: ConfigFormProps) {
  const categoryOptions = Object.keys(options.company_categories).map(
    (key) => ({
      value: key,
      label: key,
    }),
  );

  const serviceTypeOptions = options.service_types.map((type) => ({
    value: type,
    label: type,
  }));

  const companySizeOptions = options.company_sizes.map((size) => ({
    value: size,
    label: size,
  }));

  const personalizationOptions = options.personalization_levels.map(
    (level) => ({
      value: level,
      label: level,
    }),
  );

  const departmentOptions = options.target_departments.map((dept) => ({
    value: dept,
    label: dept,
  }));

  const selectedCategory = config.company_category
    ? options.company_categories[config.company_category]
    : null;

  return (
    <div className="space-y-6">
      {/* Company Category */}
      <div>
        <Select
          label="Company Category"
          required
          value={config.company_category}
          onChange={(e) =>
            onChange({ ...config, company_category: e.target.value })
          }
          options={categoryOptions}
          helperText="Type of companies you want to target"
        />
        {selectedCategory && (
          <div className="mt-2 p-3 bg-blue-50 rounded-lg">
            <p className="text-sm text-blue-900 font-medium mb-1">
              About this category:
            </p>
            <p className="text-sm text-blue-800">
              {selectedCategory.description}
            </p>
            <p className="text-xs text-blue-700 mt-2">
              <span className="font-medium">Typical roles:</span>{" "}
              {selectedCategory.typical_roles.join(", ")}
            </p>
          </div>
        )}
      </div>

      {/* Target Departments */}
      <MultiSelect
        label="Target Departments"
        required
        value={config.target_departments}
        onChange={(value) => onChange({ ...config, target_departments: value })}
        options={departmentOptions}
        helperText="Select one or more departments to target"
      />

      {/* Service Type */}
      <Select
        label="Service Type"
        required
        value={config.service_type}
        onChange={(e) =>
          onChange({
            ...config,
            service_type: e.target.value as OutreachConfig["service_type"],
          })
        }
        options={serviceTypeOptions}
        helperText="Type of service or solution you're offering"
      />

      {/* Company Size Preference */}
      <Select
        label="Company Size Preference"
        required
        value={config.company_size_preference}
        onChange={(e) =>
          onChange({
            ...config,
            company_size_preference: e.target
              .value as OutreachConfig["company_size_preference"],
          })
        }
        options={companySizeOptions}
        helperText="Preferred company size to target"
      />

      {/* Personalization Level */}
      <div>
        <Select
          label="Personalization Level"
          required
          value={config.personalization_level}
          onChange={(e) =>
            onChange({
              ...config,
              personalization_level: e.target
                .value as OutreachConfig["personalization_level"],
            })
          }
          options={personalizationOptions}
          helperText="Depth of research and personalization"
        />
        <div className="mt-2 text-sm text-gray-600">
          {config.personalization_level === "Basic" &&
            "• Quick research with basic company info"}
          {config.personalization_level === "Medium" &&
            "• Moderate research with company details and recent news"}
          {config.personalization_level === "Deep" &&
            "• Comprehensive research with detailed insights and competitive analysis"}
        </div>
      </div>

      {/* Number of Companies */}
      <div>
        <Input
          type="number"
          label="Number of Companies"
          required
          min={1}
          max={20}
          value={numCompanies}
          onChange={(e) => onNumCompaniesChange(parseInt(e.target.value) || 1)}
          helperText="How many companies to discover (1-20)"
        />
        {numCompanies > 10 && (
          <p className="mt-1 text-sm text-yellow-600">
            ⚠️ Higher numbers will take longer to process
          </p>
        )}
      </div>
    </div>
  );
}
