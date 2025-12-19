import React, { useState, useMemo } from 'react';
import { Layout } from '@/components/layout/Layout';
import { CaseCard } from '@/components/cases/CaseCard';
import { CaseFilters, FilterState } from '@/components/cases/CaseFilters';
import { CaseUploadModal } from '@/components/cases/CaseUploadModal';
import { useRole } from '@/contexts/RoleContext';
import { Button } from '@/components/ui/button';
import { Plus, FileText, Users, AlertTriangle, CheckCircle } from 'lucide-react';

import { cases } from '@/services/api';

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
  const [caseList, setCaseList] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  React.useEffect(() => {
    const fetchCases = async () => {
      try {
        const data = await cases.list();
        setCaseList(data);
      } catch (error) {
        console.error("Failed to fetch cases", error);
      } finally {
        setLoading(false);
      }
    };
    fetchCases();
  }, [uploadModalOpen]); // Refresh when upload modal closes

  const filteredCases = useMemo(() => {
    return caseList.filter((c) => {
      if (filters.search) {
        const searchLower = filters.search.toLowerCase();
        // Handle optional fields safely
        const matchesCaseNumber = c.caseNumber?.toLowerCase().includes(searchLower) || false;
        const matchesAccused = c.accused?.some((a: any) =>
          a.name?.toLowerCase().includes(searchLower)
        ) || false;
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
  }, [filters, caseList]);

  const stats = useMemo(() => {
    return {
      total: caseList.length,
      underInvestigation: caseList.filter((c) => c.status === 'Under Investigation').length,
      pendingTrial: caseList.filter((c) => c.status === 'Pending Trial').length,
      closed: caseList.filter((c) => c.status === 'Closed' || c.status === 'Convicted').length,
    };
  }, [caseList]);

  return (
    <Layout>
      <div className="container py-8 space-y-8">
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
          <div>
            <h1 className="text-3xl font-bold text-foreground">Case Dashboard</h1>
            <p className="text-muted-foreground mt-1">
              Manage and monitor all criminal cases in the system
            </p>
          </div>
          {canUpload && (
            <Button onClick={() => setUploadModalOpen(true)} size="lg" className="gap-2">
              <Plus className="h-5 w-5" />
              Upload Case
            </Button>
          )}
        </div>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="bg-card rounded-xl border border-border p-4">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-primary/10 rounded-lg">
                <FileText className="h-5 w-5 text-primary" />
              </div>
              <div>
                <p className="text-2xl font-bold">{stats.total}</p>
                <p className="text-sm text-muted-foreground">Total Cases</p>
              </div>
            </div>
          </div>
          <div className="bg-card rounded-xl border border-border p-4">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-warning/10 rounded-lg">
                <AlertTriangle className="h-5 w-5 text-warning" />
              </div>
              <div>
                <p className="text-2xl font-bold">{stats.underInvestigation}</p>
                <p className="text-sm text-muted-foreground">Under Investigation</p>
              </div>
            </div>
          </div>
          <div className="bg-card rounded-xl border border-border p-4">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-info/10 rounded-lg">
                <Users className="h-5 w-5 text-info" />
              </div>
              <div>
                <p className="text-2xl font-bold">{stats.pendingTrial}</p>
                <p className="text-sm text-muted-foreground">Pending Trial</p>
              </div>
            </div>
          </div>
          <div className="bg-card rounded-xl border border-border p-4">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-success/10 rounded-lg">
                <CheckCircle className="h-5 w-5 text-success" />
              </div>
              <div>
                <p className="text-2xl font-bold">{stats.closed}</p>
                <p className="text-sm text-muted-foreground">Closed/Convicted</p>
              </div>
            </div>
          </div>
        </div>

        <CaseFilters
          filters={filters}
          onFilterChange={setFilters}
          onReset={() => setFilters(defaultFilters)}
        />

        <div className="flex items-center justify-between">
          <p className="text-sm text-muted-foreground">
            Showing {filteredCases.length} of {caseList.length} cases
          </p>
        </div>

        {loading ? (
          <div className="text-center py-12">Loading cases...</div>
        ) : filteredCases.length > 0 ? (
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