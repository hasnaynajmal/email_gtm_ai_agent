/**
 * Campaign Configuration Page - Multi-step form
 */
'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import toast from 'react-hot-toast';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { LoadingPage } from '@/components/ui/Loading';
import { ConfigForm } from '@/components/campaign/ConfigForm';
import { SenderForm } from '@/components/campaign/SenderForm';
import { StepIndicator } from '@/components/campaign/StepIndicator';
import { api } from '@/lib/api';
import type { 
  CampaignConfig, 
  OutreachConfig, 
  SenderDetails,
  CampaignOptionsResponse 
} from '@/lib/types';

export default function NewCampaignPage() {
  const router = useRouter();
  const [currentStep, setCurrentStep] = useState<1 | 2>(1);
  const [isLoading, setIsLoading] = useState(true);
  const [isSaving, setIsSaving] = useState(false);
  const [options, setOptions] = useState<CampaignOptionsResponse | null>(null);

  // Form state
  const [outreachConfig, setOutreachConfig] = useState<OutreachConfig>({
    company_category: '',
    target_departments: [],
    service_type: 'Software Solution',
    company_size_preference: 'All Sizes',
    personalization_level: 'Medium',
  });

  const [senderDetails, setSenderDetails] = useState<SenderDetails>({
    name: '',
    email: '',
    organization: '',
    service_offered: '',
    calendar_link: '',
    linkedin: '',
    phone: '',
    website: '',
  });

  const [numCompanies, setNumCompanies] = useState(5);

  // Load campaign options on mount
  useEffect(() => {
    loadOptions();
  }, []);

  const loadOptions = async () => {
    try {
      const data = await api.getCampaignOptions();
      setOptions(data);
    } catch (error) {
      console.error('Failed to load options:', error);
      toast.error('Failed to load configuration options');
    } finally {
      setIsLoading(false);
    }
  };

  const validateStep1 = (): boolean => {
    if (!outreachConfig.company_category) {
      toast.error('Please select a company category');
      return false;
    }
    if (outreachConfig.target_departments.length === 0) {
      toast.error('Please select at least one target department');
      return false;
    }
    return true;
  };

  const validateStep2 = (): boolean => {
    if (!senderDetails.name.trim()) {
      toast.error('Please enter your name');
      return false;
    }
    if (!senderDetails.email.trim()) {
      toast.error('Please enter your email');
      return false;
    }
    // Basic email validation
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(senderDetails.email)) {
      toast.error('Please enter a valid email address');
      return false;
    }
    if (!senderDetails.organization.trim()) {
      toast.error('Please enter your organization');
      return false;
    }
    if (!senderDetails.service_offered.trim()) {
      toast.error('Please describe the service you offer');
      return false;
    }
    return true;
  };

  const handleNext = () => {
    if (validateStep1()) {
      setCurrentStep(2);
    }
  };

  const handleBack = () => {
    setCurrentStep(1);
  };

  const handleSubmit = async () => {
    if (!validateStep2()) return;

    setIsSaving(true);
    try {
      const config: CampaignConfig = {
        outreach_config: outreachConfig,
        sender_details: senderDetails,
        num_companies: numCompanies,
      };

      // Validate with backend
      const validation = await api.validateCampaignConfig(config);
      
      if (!validation.valid) {
        toast.error(validation.errors[0] || 'Invalid configuration');
        return;
      }

      // Show warnings if any
      if (validation.warnings.length > 0) {
        validation.warnings.forEach(warning => toast(warning, { icon: '⚠️' }));
      }

      // Store config in sessionStorage and navigate to execution page
      sessionStorage.setItem('campaignConfig', JSON.stringify(config));
      toast.success('Configuration validated! Proceeding to execution...');
      
      // Navigate to execution page
      router.push('/campaign/execute');
    } catch (error: any) {
      console.error('Validation failed:', error);
      toast.error(error.response?.data?.detail || 'Failed to validate configuration');
    } finally {
      setIsSaving(false);
    }
  };

  if (isLoading) {
    return <LoadingPage message="Loading campaign options..." />;
  }

  if (!options) {
    return (
      <div className="text-center py-12">
        <p className="text-red-600 mb-4">Failed to load campaign options</p>
        <Button onClick={loadOptions}>Retry</Button>
      </div>
    );
  }

  const steps = [
    { number: 1, title: 'Campaign Configuration', description: 'Target audience & preferences' },
    { number: 2, title: 'Sender Details', description: 'Your information & offering' },
  ];

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Create New Campaign</h1>
        <p className="text-gray-600">
          Configure your AI-powered outreach campaign in two simple steps
        </p>
      </div>

      {/* Step Indicator */}
      <StepIndicator steps={steps} currentStep={currentStep} />

      {/* Form Card */}
      <Card>
        <CardHeader>
          <CardTitle>{steps[currentStep - 1].title}</CardTitle>
          <CardDescription>{steps[currentStep - 1].description}</CardDescription>
        </CardHeader>
        <CardContent>
          {currentStep === 1 ? (
            <ConfigForm
              config={outreachConfig}
              onChange={setOutreachConfig}
              numCompanies={numCompanies}
              onNumCompaniesChange={setNumCompanies}
              options={options}
            />
          ) : (
            <SenderForm
              details={senderDetails}
              onChange={setSenderDetails}
            />
          )}
        </CardContent>
      </Card>

      {/* Navigation Buttons */}
      <div className="flex justify-between">
        <Button
          variant="outline"
          onClick={handleBack}
          disabled={currentStep === 1 || isSaving}
        >
          Back
        </Button>
        
        {currentStep === 1 ? (
          <Button onClick={handleNext}>
            Next
          </Button>
        ) : (
          <Button onClick={handleSubmit} isLoading={isSaving}>
            {isSaving ? 'Validating...' : 'Start Campaign'}
          </Button>
        )}
      </div>
    </div>
  );
}
