import React, { useState } from 'react';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Badge } from '@/components/ui/badge';
import { districts, contrabandTypes, accusedStatuses } from '@/data/mockCases';
import {
  FileText,
  User,
  Package,
  Upload,
  MessageSquare,
  Plus,
  X,
  Phone,
} from 'lucide-react';
import { useToast } from '@/hooks/use-toast';

interface CaseUploadModalProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
}

interface CustomField {
  id: string;
  label: string;
  value: string;
}

interface AccusedInfo {
  name: string;
  fatherName: string;
  age: string;
  gender: string;
  address: string;
  mobile: string;
  status: string;
}

export const CaseUploadModal: React.FC<CaseUploadModalProps> = ({
  open,
  onOpenChange,
}) => {
  const { toast } = useToast();
  const [activeTab, setActiveTab] = useState('case-details');
  const [customFields, setCustomFields] = useState<CustomField[]>([]);
  const [lawSections, setLawSections] = useState<string[]>([]);
  const [newLawSection, setNewLawSection] = useState('');
  const [accused, setAccused] = useState<AccusedInfo[]>([
    {
      name: '',
      fatherName: '',
      age: '',
      gender: '',
      address: '',
      mobile: '',
      status: '',
    },
  ]);
  const [publicAlertEnabled, setPublicAlertEnabled] = useState(false);
  const [publicAlertMessage, setPublicAlertMessage] = useState('');
  const [publicAlertMobile, setPublicAlertMobile] = useState('');

  const addLawSection = () => {
    if (newLawSection && !lawSections.includes(newLawSection)) {
      setLawSections([...lawSections, newLawSection]);
      setNewLawSection('');
    }
  };

  const removeLawSection = (section: string) => {
    setLawSections(lawSections.filter((s) => s !== section));
  };

  const addCustomField = () => {
    setCustomFields([
      ...customFields,
      { id: Date.now().toString(), label: '', value: '' },
    ]);
  };

  const updateCustomField = (id: string, field: 'label' | 'value', value: string) => {
    setCustomFields(
      customFields.map((cf) => (cf.id === id ? { ...cf, [field]: value } : cf))
    );
  };

  const removeCustomField = (id: string) => {
    setCustomFields(customFields.filter((cf) => cf.id !== id));
  };

  const addAccused = () => {
    setAccused([
      ...accused,
      {
        name: '',
        fatherName: '',
        age: '',
        gender: '',
        address: '',
        mobile: '',
        status: '',
      },
    ]);
  };

  const updateAccused = (index: number, field: keyof AccusedInfo, value: string) => {
    const newAccused = [...accused];
    newAccused[index] = { ...newAccused[index], [field]: value };
    setAccused(newAccused);
  };

  const removeAccused = (index: number) => {
    if (accused.length > 1) {
      setAccused(accused.filter((_, i) => i !== index));
    }
  };

  const handleSubmit = () => {
    toast({
      title: 'Case Uploaded Successfully',
      description: 'The case has been registered and is now available in the system.',
    });
    onOpenChange(false);
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-4xl max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle className="font-display text-xl">Upload New Case</DialogTitle>
        </DialogHeader>

        <Tabs value={activeTab} onValueChange={setActiveTab} className="mt-4">
          <TabsList className="grid grid-cols-5 w-full">
            <TabsTrigger value="case-details" className="text-xs sm:text-sm">
              <FileText className="h-4 w-4 mr-1 hidden sm:block" />
              Case Details
            </TabsTrigger>
            <TabsTrigger value="contraband" className="text-xs sm:text-sm">
              <Package className="h-4 w-4 mr-1 hidden sm:block" />
              Contraband
            </TabsTrigger>
            <TabsTrigger value="accused" className="text-xs sm:text-sm">
              <User className="h-4 w-4 mr-1 hidden sm:block" />
              Accused
            </TabsTrigger>
            <TabsTrigger value="evidence" className="text-xs sm:text-sm">
              <Upload className="h-4 w-4 mr-1 hidden sm:block" />
              Evidence
            </TabsTrigger>
            <TabsTrigger value="public-alert" className="text-xs sm:text-sm">
              <MessageSquare className="h-4 w-4 mr-1 hidden sm:block" />
              Public Alert
            </TabsTrigger>
          </TabsList>

          <TabsContent value="case-details" className="space-y-4 mt-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="district">District/City *</Label>
                <Select>
                  <SelectTrigger>
                    <SelectValue placeholder="e.g., Central Delhi" />
                  </SelectTrigger>
                  <SelectContent>
                    {districts.map((d) => (
                      <SelectItem key={d} value={d}>
                        {d}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label htmlFor="unit">PEW/PS/NIBCID Unit *</Label>
                <Input id="unit" placeholder="e.g., Cyber Crime Unit" />
              </div>

              <div className="space-y-2 md:col-span-2">
                <Label>Law Sections *</Label>
                <div className="flex gap-2">
                  <Input
                    placeholder="e.g., IPC 420"
                    value={newLawSection}
                    onChange={(e) => setNewLawSection(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && addLawSection()}
                  />
                  <Button type="button" onClick={addLawSection} variant="secondary">
                    Add
                  </Button>
                </div>
                <div className="flex flex-wrap gap-2 mt-2">
                  {lawSections.map((section) => (
                    <Badge key={section} variant="secondary" className="pl-2">
                      {section}
                      <button
                        onClick={() => removeLawSection(section)}
                        className="ml-1 hover:text-destructive"
                      >
                        <X className="h-3 w-3" />
                      </button>
                    </Badge>
                  ))}
                </div>
              </div>

              <div className="space-y-2">
                <Label htmlFor="dateOfOffence">Date of Offence *</Label>
                <Input id="dateOfOffence" type="date" />
              </div>

              <div className="space-y-2">
                <Label htmlFor="dateOfReport">Date of Report *</Label>
                <Input id="dateOfReport" type="date" />
              </div>

              <div className="space-y-2 md:col-span-2">
                <Label htmlFor="sceneOfCrime">Scene of Crime *</Label>
                <Input id="sceneOfCrime" placeholder="e.g., Connaught Place, New Delhi" />
              </div>

              <div className="space-y-2">
                <Label htmlFor="latitude">Latitude *</Label>
                <Input id="latitude" type="number" step="any" placeholder="e.g., 28.6315" />
              </div>

              <div className="space-y-2">
                <Label htmlFor="longitude">Longitude *</Label>
                <Input id="longitude" type="number" step="any" placeholder="e.g., 77.2167" />
              </div>
            </div>

            <div className="space-y-3 pt-4 border-t border-border">
              <div className="flex items-center justify-between">
                <Label>Custom Fields</Label>
                <Button type="button" variant="outline" size="sm" onClick={addCustomField}>
                  <Plus className="h-4 w-4 mr-1" />
                  Add Field
                </Button>
              </div>
              {customFields.map((field) => (
                <div key={field.id} className="flex gap-2">
                  <Input
                    placeholder="Field Label"
                    value={field.label}
                    onChange={(e) => updateCustomField(field.id, 'label', e.target.value)}
                    className="w-1/3"
                  />
                  <Input
                    placeholder="Field Value"
                    value={field.value}
                    onChange={(e) => updateCustomField(field.id, 'value', e.target.value)}
                    className="flex-1"
                  />
                  <Button
                    type="button"
                    variant="ghost"
                    size="icon"
                    onClick={() => removeCustomField(field.id)}
                  >
                    <X className="h-4 w-4" />
                  </Button>
                </div>
              ))}
            </div>
          </TabsContent>

          <TabsContent value="contraband" className="space-y-4 mt-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="contrabandType">Contraband Type</Label>
                <Select>
                  <SelectTrigger>
                    <SelectValue placeholder="e.g., Narcotic Substances" />
                  </SelectTrigger>
                  <SelectContent>
                    {contrabandTypes.map((type) => (
                      <SelectItem key={type} value={type}>
                        {type}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label htmlFor="contrabandQuantity">Quantity</Label>
                <Input id="contrabandQuantity" placeholder="e.g., 500 grams" />
              </div>

              <div className="space-y-2 md:col-span-2">
                <Label htmlFor="vehicleDetails">Vehicle Details (if applicable)</Label>
                <Input
                  id="vehicleDetails"
                  placeholder="e.g., DL 4C AB 1234 - White Honda City"
                />
              </div>
            </div>
          </TabsContent>

          <TabsContent value="accused" className="space-y-4 mt-4">
            {accused.map((acc, index) => (
              <div
                key={index}
                className="p-4 border border-border rounded-lg space-y-4"
              >
                <div className="flex items-center justify-between">
                  <h4 className="font-medium">Accused #{index + 1}</h4>
                  {accused.length > 1 && (
                    <Button
                      type="button"
                      variant="ghost"
                      size="sm"
                      onClick={() => removeAccused(index)}
                    >
                      <X className="h-4 w-4" />
                    </Button>
                  )}
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label>Name *</Label>
                    <Input
                      placeholder="e.g., Rajesh Kumar"
                      value={acc.name}
                      onChange={(e) => updateAccused(index, 'name', e.target.value)}
                    />
                  </div>
                  <div className="space-y-2">
                    <Label>Father's Name</Label>
                    <Input
                      placeholder="e.g., Suresh Kumar"
                      value={acc.fatherName}
                      onChange={(e) => updateAccused(index, 'fatherName', e.target.value)}
                    />
                  </div>
                  <div className="space-y-2">
                    <Label>Age *</Label>
                    <Input
                      type="number"
                      placeholder="e.g., 32"
                      value={acc.age}
                      onChange={(e) => updateAccused(index, 'age', e.target.value)}
                    />
                  </div>
                  <div className="space-y-2">
                    <Label>Gender *</Label>
                    <Select
                      value={acc.gender}
                      onValueChange={(value) => updateAccused(index, 'gender', value)}
                    >
                      <SelectTrigger>
                        <SelectValue placeholder="Select gender" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="Male">Male</SelectItem>
                        <SelectItem value="Female">Female</SelectItem>
                        <SelectItem value="Other">Other</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                  <div className="space-y-2 md:col-span-2">
                    <Label>Address</Label>
                    <Input
                      placeholder="e.g., 45, Lajpat Nagar, New Delhi"
                      value={acc.address}
                      onChange={(e) => updateAccused(index, 'address', e.target.value)}
                    />
                  </div>
                  <div className="space-y-2">
                    <Label>Mobile</Label>
                    <Input
                      placeholder="e.g., 9876543210"
                      value={acc.mobile}
                      onChange={(e) => updateAccused(index, 'mobile', e.target.value)}
                    />
                  </div>
                  <div className="space-y-2">
                    <Label>Status *</Label>
                    <Select
                      value={acc.status}
                      onValueChange={(value) => updateAccused(index, 'status', value)}
                    >
                      <SelectTrigger>
                        <SelectValue placeholder="Select status" />
                      </SelectTrigger>
                      <SelectContent>
                        {accusedStatuses.map((status) => (
                          <SelectItem key={status} value={status}>
                            {status}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>
                </div>
              </div>
            ))}
            <Button type="button" variant="outline" onClick={addAccused} className="w-full">
              <Plus className="h-4 w-4 mr-2" />
              Add Another Accused
            </Button>
          </TabsContent>

          <TabsContent value="evidence" className="space-y-4 mt-4">
            <div className="border-2 border-dashed border-border rounded-lg p-8 text-center">
              <Upload className="h-12 w-12 mx-auto text-muted-foreground mb-4" />
              <h4 className="font-medium mb-2">Upload Evidence Files</h4>
              <p className="text-sm text-muted-foreground mb-4">
                Drag & drop files here, or click to browse
              </p>
              <p className="text-xs text-muted-foreground mb-4">
                Supported formats: Images (JPG, PNG), Documents (PDF, DOC), Videos (MP4), Audio (MP3)
              </p>
              <Button variant="secondary">
                <Upload className="h-4 w-4 mr-2" />
                Browse Files
              </Button>
            </div>
          </TabsContent>

          <TabsContent value="public-alert" className="space-y-4 mt-4">
            <div className="p-4 bg-warning/10 rounded-lg border border-warning/20">
              <h4 className="font-medium text-warning mb-2">Public Alert Feature</h4>
              <p className="text-sm text-muted-foreground">
                If you need public assistance in this case, you can send an alert message to the public.
                This message will be broadcast to the registered community members.
              </p>
            </div>

            <div className="space-y-4">
              <div className="flex items-center gap-2">
                <input
                  type="checkbox"
                  id="enablePublicAlert"
                  checked={publicAlertEnabled}
                  onChange={(e) => setPublicAlertEnabled(e.target.checked)}
                  className="rounded border-border"
                />
                <Label htmlFor="enablePublicAlert">Enable Public Alert</Label>
              </div>

              {publicAlertEnabled && (
                <>
                  <div className="space-y-2">
                    <Label htmlFor="alertMessage">Alert Message *</Label>
                    <Textarea
                      id="alertMessage"
                      placeholder="e.g., Public assistance needed for identifying suspect. Last seen wearing blue jacket near Central Park area..."
                      value={publicAlertMessage}
                      onChange={(e) => setPublicAlertMessage(e.target.value)}
                      rows={4}
                    />
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="alertMobile">Contact Mobile Number *</Label>
                    <div className="flex items-center gap-2">
                      <Phone className="h-4 w-4 text-muted-foreground" />
                      <Input
                        id="alertMobile"
                        placeholder="e.g., 9876543210"
                        value={publicAlertMobile}
                        onChange={(e) => setPublicAlertMobile(e.target.value)}
                      />
                    </div>
                    <p className="text-xs text-muted-foreground">
                      This number will be included in the alert for public to contact.
                    </p>
                  </div>
                </>
              )}
            </div>
          </TabsContent>
        </Tabs>

        <div className="flex justify-end gap-3 mt-6 pt-4 border-t border-border">
          <Button variant="outline" onClick={() => onOpenChange(false)}>
            Cancel
          </Button>
          <Button onClick={handleSubmit}>
            <Upload className="h-4 w-4 mr-2" />
            Upload Case
          </Button>
        </div>
      </DialogContent>
    </Dialog>
  );
};