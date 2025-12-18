import React, { useState, useMemo } from 'react';
import { Layout } from '@/components/layout/Layout';
import { CaseCard } from '@/components/cases/CaseCard';
import { CaseFilters, FilterState } from '@/components/cases/CaseFilters';
import { CaseUploadModal } from '@/components/cases/CaseUploadModal';
import { mockCases } from '@/data/mockCases';
import { useRole } from '@/contexts/RoleContext';
import { Button } from '@/components/ui/button';
import { Plus, FileText, Users, AlertTriangle, CheckCircle } from 'lucide-react';

const defaultFilters: FilterState = {
  search: '',
  district: '',
  status: '',
  dateFrom: undefined,
  dateTo: undefined,
};

const Dashboard: React.FC = () => {
  const { canUpload } = useRole();
  const [filters, setFilters] = useState<FilterState>(defaultFilters);
  const [uploadModalOpen, setUploadModalOpen] = useState(false);

  const filteredCases = useMemo(() => {
    return mockCases.filter((c) => {
      if (filters.search) {
        const searchLower = filters.search.toLowerCase();
        const matchesCaseNumber = c.caseNumber.toLowerCase().includes(searchLower);
        const matchesAccused = c.accused.some((a) =>
          a.name.toLowerCase().includes(searchLower)
        );
        if (!matchesCaseNumber && !matchesAccused) return false;
      }

      if (filters.district && filters.district !== 'all' && c.district !== filters.district) {
        return false;
      }

      if (filters.status && filters.status !== 'all' && c.status !== filters.status) {
        return false;
      }

      if (filters.dateFrom) {
        const offenceDate = new Date(c.dateOfOffence);
        if (offenceDate < filters.dateFrom) return false;
      }

      if (filters.dateTo) {
        const offenceDate = new Date(c.dateOfOffence);
        if (offenceDate > filters.dateTo) return false;
      }

      return true;
    });
  }, [filters]);

  const stats = useMemo(() => {
    return {
      total: mockCases.length,
      underInvestigation: mockCases.filter((c) => c.status === 'Under Investigation').length,
      pendingTrial: mockCases.filter((c) => c.status === 'Pending Trial').length,
      closed: mockCases.filter((c) => c.status === 'Closed' || c.status === 'Convicted').length,
    };
  }, []);

  return (
    <Layout>
      <div className="container py-8 space-y-8">
        

        

        <CaseFilters
          filters={filters}
          onFilterChange={setFilters}
          onReset={() => setFilters(defaultFilters)}
        />

        <div className="flex items-center justify-between">
          <p className="text-sm text-muted-foreground">
            Showing {filteredCases.length} of {mockCases.length} cases
          </p>
        </div>

        {filteredCases.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredCases.map((c) => (
              <CaseCard key={c.id} caseData={c} />
            ))}
          </div>
        ) : (
          <div className="text-center py-12">
            <FileText className="h-12 w-12 mx-auto text-muted-foreground mb-4" />
            <h3 className="text-lg font-medium mb-2">No cases found</h3>
            <p className="text-muted-foreground">
              Try adjusting your filters to see more results
            </p>
          </div>
        )}
      </div>

      <CaseUploadModal open={uploadModalOpen} onOpenChange={setUploadModalOpen} />
    </Layout>
  );
};

export default Dashboard;