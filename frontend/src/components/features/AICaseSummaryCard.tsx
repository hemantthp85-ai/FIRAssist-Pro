import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Sparkles, Calendar, MapPin, User, AlertCircle } from 'lucide-react'

interface AICaseSummaryCardProps {
  caseData: any
}

export default function AICaseSummaryCard({ caseData }: AICaseSummaryCardProps) {
  const victimName = caseData.victim_name || 'Not specified'
  const incidentDate = caseData.incident_date || 'Not specified'
  const location = caseData.location || 'Not specified'
  const crimeType = caseData.crime_type || (Array.isArray(caseData.possible_offences) && caseData.possible_offences[0]) || 'Unknown Offence'
  const accusedName = caseData.accused_name || 'Unknown suspects'
  const incidentSummary = caseData.incident_summary || 'No detailed incident summary extracted yet.'

  // Dynamic details highlight based on crime type
  const isCyber = crimeType.toLowerCase().includes('cyber') || crimeType.toLowerCase().includes('financial') || !!caseData.transaction_id
  const isTheft = crimeType.toLowerCase().includes('theft') || crimeType.toLowerCase().includes('robbery') || !!caseData.property_value

  return (
    <Card className="bg-card/50 backdrop-blur border-white/10 overflow-hidden">
      <div className="absolute top-0 right-0 w-32 h-32 bg-accent/5 rounded-full blur-2xl pointer-events-none" />
      <CardHeader className="pb-3 border-b border-white/5">
        <CardTitle className="text-lg flex items-center gap-2">
          <Sparkles className="w-5 h-5 text-accent animate-pulse" />
          AI Case Executive Summary
        </CardTitle>
        <CardDescription>
          Synthesized police synopsis of the incident details
        </CardDescription>
      </CardHeader>
      <CardContent className="p-5 space-y-4">
        {/* Core Case Synopsis */}
        <div className="p-4 rounded-xl bg-accent/5 border border-accent/10 relative">
          <p className="text-sm text-foreground/90 leading-relaxed italic">
            "{incidentSummary}"
          </p>
        </div>

        {/* Fact Sheet Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
          <div className="flex items-center gap-2.5 p-2.5 rounded-lg bg-secondary/10 border border-white/5">
            <User className="w-4 h-4 text-accent/80 shrink-0" />
            <div className="min-w-0">
              <p className="text-[10px] text-muted-foreground uppercase font-bold">Complainant / Victim</p>
              <p className="font-semibold text-foreground truncate">{victimName}</p>
            </div>
          </div>

          <div className="flex items-center gap-2.5 p-2.5 rounded-lg bg-secondary/10 border border-white/5">
            <Calendar className="w-4 h-4 text-accent/80 shrink-0" />
            <div className="min-w-0">
              <p className="text-[10px] text-muted-foreground uppercase font-bold">Occurrence Date & Time</p>
              <p className="font-semibold text-foreground truncate">
                {incidentDate} {caseData.incident_time ? `@ ${caseData.incident_time}` : ''}
              </p>
            </div>
          </div>

          <div className="flex items-center gap-2.5 p-2.5 rounded-lg bg-secondary/10 border border-white/5">
            <MapPin className="w-4 h-4 text-accent/80 shrink-0" />
            <div className="min-w-0">
              <p className="text-[10px] text-muted-foreground uppercase font-bold">Location of Incident</p>
              <p className="font-semibold text-foreground truncate">{location}</p>
            </div>
          </div>

          <div className="flex items-center gap-2.5 p-2.5 rounded-lg bg-secondary/10 border border-white/5">
            <AlertCircle className="w-4 h-4 text-accent/80 shrink-0" />
            <div className="min-w-0">
              <p className="text-[10px] text-muted-foreground uppercase font-bold">Accused / Suspects</p>
              <p className="font-semibold text-foreground truncate">{accusedName}</p>
            </div>
          </div>
        </div>

        {/* Extra specifics if present */}
        {(isCyber && (caseData.bank_name || caseData.transaction_id || caseData.amount_lost)) && (
          <div className="p-3 rounded-lg bg-indigo-500/5 border border-indigo-500/10 text-xs">
            <p className="font-bold text-[10px] text-indigo-400 uppercase tracking-wider mb-1.5">Cyber/Financial Details</p>
            <div className="grid grid-cols-3 gap-2">
              <div>
                <span className="text-muted-foreground block text-[9px] uppercase">Bank Name</span>
                <span className="font-medium text-foreground">{caseData.bank_name || 'N/A'}</span>
              </div>
              <div>
                <span className="text-muted-foreground block text-[9px] uppercase">Transaction ID</span>
                <span className="font-medium text-foreground truncate block">{caseData.transaction_id || 'N/A'}</span>
              </div>
              <div>
                <span className="text-muted-foreground block text-[9px] uppercase">Amount Lost</span>
                <span className="font-semibold text-accent">{caseData.amount_lost ? `₹${caseData.amount_lost}` : 'N/A'}</span>
              </div>
            </div>
          </div>
        )}

        {(isTheft && (caseData.property_type || caseData.property_value)) && (
          <div className="p-3 rounded-lg bg-amber-500/5 border border-amber-500/10 text-xs">
            <p className="font-bold text-[10px] text-amber-400 uppercase tracking-wider mb-1.5">Property Details</p>
            <div className="grid grid-cols-2 gap-2">
              <div>
                <span className="text-muted-foreground block text-[9px] uppercase">Property Type</span>
                <span className="font-medium text-foreground">{caseData.property_type || 'N/A'}</span>
              </div>
              <div>
                <span className="text-muted-foreground block text-[9px] uppercase">Property Value</span>
                <span className="font-semibold text-accent">{caseData.property_value ? `₹${caseData.property_value}` : 'N/A'}</span>
              </div>
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  )
}
