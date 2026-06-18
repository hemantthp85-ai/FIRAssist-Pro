import type { Complaint, BNSSection, Officer, DashboardStats, Notification, CrimeType } from '@/types'

export const mockOfficer: Officer = {
  id: 'OFF-2024-001',
  name: 'Rajesh Kumar',
  rank: 'Sub-Inspector',
  station: 'Chennai Central Police Station',
  badge: 'TN-SI-4521',
  email: 'rajesh.kumar@tnpolice.gov.in'
}

export const mockNotifications: Notification[] = [
  {
    id: '1',
    title: 'New Complaint Assigned',
    message: 'A new theft complaint has been assigned to you.',
    type: 'info',
    read: false,
    createdAt: new Date().toISOString()
  },
  {
    id: '2',
    title: 'FIR Review Required',
    message: 'FIR #2024-0892 requires your review.',
    type: 'warning',
    read: false,
    createdAt: new Date(Date.now() - 3600000).toISOString()
  },
  {
    id: '3',
    title: 'FIR Submitted Successfully',
    message: 'FIR #2024-0891 has been submitted to the court.',
    type: 'success',
    read: true,
    createdAt: new Date(Date.now() - 7200000).toISOString()
  }
]

export const mockDashboardStats: DashboardStats = {
  totalComplaints: 1247,
  firGenerated: 1089,
  pendingReviews: 158,
  highPriorityCases: 42,
  weeklyTrend: [45, 52, 38, 61, 55, 48, 63],
  crimeDistribution: {
    'Theft': 412,
    'Assault': 287,
    'Cyber Crime': 156,
    'Fraud': 198,
    'Missing Person': 89,
    'Murder': 23,
    'Robbery': 45,
    'Domestic Violence': 123,
    'Property Dispute': 67,
    'Other': 47
  }
}

export const mockBNSSections: BNSSection[] = [
  {
    sectionNumber: 'BNS 303',
    title: 'Theft',
    description: 'Whoever, intending to take dishonestly any movable property out of the possession of any person without that person\'s consent, moves such property in order to such taking, is said to commit theft.',
    punishment: 'Imprisonment for up to 3 years, or fine, or both.',
    relatedCrimes: ['Theft', 'Robbery']
  },
  {
    sectionNumber: 'BNS 305',
    title: 'House-breaking',
    description: 'House-breaking means committing theft or other offense after entering a building used as a human dwelling.',
    punishment: 'Imprisonment for up to 10 years and fine.',
    relatedCrimes: ['Theft', 'Robbery']
  },
  {
    sectionNumber: 'BNS 307',
    title: 'Robbery',
    description: 'Robbery is theft where violence or force is used to take property from a person.',
    punishment: 'Imprisonment for up to 14 years and fine.',
    relatedCrimes: ['Robbery', 'Theft']
  },
  {
    sectionNumber: 'BNS 324',
    title: 'Cheating',
    description: 'Whoever, by deceiving any person, fraudulently or dishonestly induces them to deliver property or consent to its retention.',
    punishment: 'Imprisonment for up to 7 years and fine.',
    relatedCrimes: ['Fraud', 'Cyber Crime']
  },
  {
    sectionNumber: 'BNS 100',
    title: 'Murder',
    description: 'Whoever causes death by doing an act with the intention of causing death, or with the intention of causing such bodily injury as is likely to cause death.',
    punishment: 'Death penalty or imprisonment for life, and fine.',
    relatedCrimes: ['Murder', 'Assault']
  },
  {
    sectionNumber: 'BNS 115',
    title: 'Voluntary causing hurt',
    description: 'Whoever, except in the case provided for by section 114, voluntarily causes hurt, shall be punished.',
    punishment: 'Imprisonment for up to 7 years and fine.',
    relatedCrimes: ['Assault', 'Domestic Violence']
  },
  {
    sectionNumber: 'BNS 354',
    title: 'Assault on woman with intent to outrage modesty',
    description: 'Whoever assaults or uses criminal force to any woman, intending to outrage or knowing it to be likely that he will thereby outrage the modesty of such woman.',
    punishment: 'Imprisonment for up to 5 years and fine.',
    relatedCrimes: ['Assault', 'Domestic Violence']
  },
  {
    sectionNumber: 'BNS 351',
    title: 'Criminal intimidation',
    description: 'Whoever threatens another with any injury to his person, reputation or property, or to the person or reputation of any one in whom that person is interested.',
    punishment: 'Imprisonment for up to 7 years and fine.',
    relatedCrimes: ['Assault', 'Domestic Violence', 'Property Dispute']
  },
  {
    sectionNumber: 'BNS 370',
    title: 'Trafficking of person',
    description: 'Whoever, for the purpose of exploitation, recruits, transports, harbours or receives a person.',
    punishment: 'Imprisonment for up to 10 years and fine.',
    relatedCrimes: ['Missing Person']
  },
  {
    sectionNumber: 'BNS 362',
    title: 'Kidnapping',
    description: 'Whoever takes or entices any minor under sixteen years of age if a male, or under eighteen years of age if a female, out of the keeping of lawful guardian.',
    punishment: 'Imprisonment for up to 7 years and fine.',
    relatedCrimes: ['Missing Person', 'Murder']
  }
]

export const mockComplaints: Complaint[] = [
  {
    id: 'CMP-2024-001',
    firNumber: 'FIR/TN-CHN-001/2024/0892',
    complainantName: 'Ramesh Pillai',
    mobileNumber: '9876543210',
    address: '45, Anna Nagar, Chennai',
    incidentDate: '2024-01-15',
    incidentTime: '14:30',
    location: 'Near Anna Nagar Bus Stand',
    suspectDetails: 'Unknown person, approx 30 years, wearing black shirt',
    witnessDetails: 'Autokaran Vela Murugan, nearby shop owner',
    crimeType: 'Theft',
    propertyDetails: 'Honda Activa 5G, Registration: TN-07-AB-1234, Blue color',
    status: 'Pending Review',
    officerId: 'OFF-2024-001',
    officerName: 'Rajesh Kumar',
    createdAt: '2024-01-15T15:00:00Z',
    updatedAt: '2024-01-16T10:30:00Z',
    bnsSections: ['BNS 303'],
    transcript: 'Yesterday my Activa scooter was stolen from outside my house. It happened around 2:30 in the afternoon. The bike is blue in color, Honda Activa 5G model. Registration number is TN-07-AB-1234.',
    completionPercentage: 95
  },
  {
    id: 'CMP-2024-002',
    firNumber: 'FIR/TN-CHN-001/2024/0891',
    complainantName: 'Lakshmi Devi',
    mobileNumber: '9876543211',
    address: '78, T. Nagar, Chennai',
    incidentDate: '2024-01-14',
    incidentTime: '20:00',
    location: 'T. Nagar Market Area',
    suspectDetails: 'Group of 3 men on bikes',
    witnessDetails: 'Street vendor nearby',
    crimeType: 'Robbery',
    propertyDetails: 'Gold chain (8 grams), Rs. 5000 cash',
    status: 'FIR Filed',
    officerId: 'OFF-2024-001',
    officerName: 'Rajesh Kumar',
    createdAt: '2024-01-14T21:00:00Z',
    updatedAt: '2024-01-15T09:00:00Z',
    bnsSections: ['BNS 307', 'BNS 303'],
    completionPercentage: 100
  },
  {
    id: 'CMP-2024-003',
    firNumber: 'Draft',
    complainantName: 'Venkat Rao',
    mobileNumber: '9876543212',
    address: '12, Adyar, Chennai',
    incidentDate: '2024-01-16',
    incidentTime: '10:00',
    location: 'Online Transaction',
    suspectDetails: 'Unknown online seller',
    witnessDetails: '',
    crimeType: 'Cyber Crime',
    propertyDetails: 'Rs. 25,000 lost in online fraud',
    status: 'Draft',
    officerId: 'OFF-2024-001',
    officerName: 'Rajesh Kumar',
    createdAt: '2024-01-16T11:00:00Z',
    updatedAt: '2024-01-16T11:00:00Z',
    bnsSections: ['BNS 324'],
    transcript: 'I found an online seller on Facebook selling electronics at cheap prices. I paid Rs. 25,000 through UPI but never received the product. Now they have blocked me.',
    completionPercentage: 72
  },
  {
    id: 'CMP-2024-004',
    firNumber: 'FIR/TN-CHN-001/2024/0890',
    complainantName: 'Meena Sundaram',
    mobileNumber: '9876543213',
    address: '34, Nungambakkam, Chennai',
    incidentDate: '2024-01-13',
    incidentTime: '22:00',
    location: 'Nungambakkam Railway Station',
    suspectDetails: 'Unknown male, approximately 25-30 years',
    witnessDetails: 'Platform ticket collector',
    crimeType: 'Assault',
    propertyDetails: 'Handbag with documents and phone',
    status: 'Under Investigation',
    officerId: 'OFF-2024-002',
    officerName: 'Kavitha R',
    createdAt: '2024-01-13T23:00:00Z',
    updatedAt: '2024-01-15T14:00:00Z',
    bnsSections: ['BNS 115', 'BNS 303'],
    completionPercentage: 85
  }
]

export const crimeCategories: { type: CrimeType; icon: string; color: string }[] = [
  { type: 'Theft', icon: 'Lock', color: 'from-yellow-500 to-orange-500' },
  { type: 'Assault', icon: 'AlertTriangle', color: 'from-red-500 to-pink-500' },
  { type: 'Cyber Crime', icon: 'Monitor', color: 'from-blue-500 to-cyan-500' },
  { type: 'Fraud', icon: 'BadgeAlert', color: 'from-purple-500 to-indigo-500' },
  { type: 'Missing Person', icon: 'UserX', color: 'from-gray-500 to-slate-500' },
  { type: 'Murder', icon: 'Skull', color: 'from-red-600 to-red-800' },
  { type: 'Robbery', icon: 'Gem', color: 'from-amber-500 to-yellow-600' },
  { type: 'Domestic Violence', icon: 'HeartOff', color: 'from-pink-500 to-rose-500' },
  { type: 'Property Dispute', icon: 'Home', color: 'from-emerald-500 to-teal-500' },
  { type: 'Other', icon: 'FileQuestion', color: 'from-gray-400 to-gray-500' }
]

export const mockAIResponses = [
  "Based on the complaint details, I would recommend BNS Section 303 for theft. Would you like me to add this to the FIR?",
  "I've detected some missing information: the vehicle registration number and exact location of the theft. Would you like me to generate follow-up questions?",
  "The incident appears to fall under the category of 'Property Theft'. I've extracted the following key details: Date: 15th January, Time: 2:30 PM, Location: Anna Nagar Bus Stand area.",
  "FIR Draft has been generated successfully. The document includes all extracted information and recommended BNS sections. You can review and edit before submission.",
  "Based on the BNS knowledge base, similar cases in the past year have had a conviction rate of 45%. Key evidence in successful prosecutions includes CCTV footage and witness statements."
]
