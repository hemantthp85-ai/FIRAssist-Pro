export interface Complaint {
  id: string
  firNumber: string
  complainantName: string
  mobileNumber: string
  address: string
  incidentDate: string
  incidentTime: string
  location: string
  suspectDetails?: string
  witnessDetails?: string
  crimeType: CrimeType
  propertyDetails?: string
  status: ComplaintStatus
  officerId: string
  officerName: string
  createdAt: string
  updatedAt: string
  bnsSections: string[]
  transcript?: string
  missingInfo?: MissingInfo[]
  completionPercentage: number
}

export type CrimeType =
  | 'Theft'
  | 'Assault'
  | 'Cyber Crime'
  | 'Fraud'
  | 'Missing Person'
  | 'Murder'
  | 'Robbery'
  | 'Domestic Violence'
  | 'Property Dispute'
  | 'Other'

export type ComplaintStatus =
  | 'Draft'
  | 'Pending Review'
  | 'Under Investigation'
  | 'FIR Filed'
  | 'Closed'
  | 'Rejected'

export interface MissingInfo {
  id: string
  field: string
  question: string
  answered: boolean
  answer?: string
}

export interface BNSSection {
  sectionNumber: string
  title: string
  description: string
  punishment: string
  relatedCrimes: CrimeType[]
  isSelected?: boolean
}

export interface Officer {
  id: string
  name: string
  rank: string
  station: string
  badge: string
  email: string
}

export interface DashboardStats {
  totalComplaints: number
  firGenerated: number
  pendingReviews: number
  highPriorityCases: number
  weeklyTrend: number[]
  crimeDistribution: Record<CrimeType, number>
}

export interface AIMessage {
  id: string
  role: 'user' | 'assistant'
  content: string
  timestamp: string
}

export interface Notification {
  id: string
  title: string
  message: string
  type: 'info' | 'warning' | 'success' | 'error'
  read: boolean
  createdAt: string
}

export interface Settings {
  darkMode: boolean
  language: string
  notifications: {
    email: boolean
    push: boolean
    sms: boolean
  }
  autoSave: boolean
}
