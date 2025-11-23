
export enum UserRole {
  Customer = 'customer',
  Bank = 'bank',
}

export interface Receipt {
  id: string;
  vendor: string;
  amount: number;
  date: string;
  category: string;
  icon: React.ComponentType<{ className?: string }>;
}

export enum ModelStatus {
    Active = 'Active',
    Inactive = 'Inactive',
    Training = 'Training',
    Error = 'Error'
}

export interface AIModel {
    id: string;
    name: string;
    version: string;
    status: ModelStatus;
    accuracy: number;
    lastUpdated: string;
}

export enum IncidentSeverity {
    Low = 'Low',
    Medium = 'Medium',
    High = 'High',
    Critical = 'Critical'
}

export interface AuditIncident {
    id: string;
    timestamp: string;
    modelId: string;
    description: string;
    severity: IncidentSeverity;
    resolved: boolean;
}

export interface NavItem {
    label: string;
    screen: string;
    icon: React.ComponentType<{ className?: string }>;
}
