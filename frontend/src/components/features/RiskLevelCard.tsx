import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { ShieldAlert, AlertOctagon, Clock, ShieldCheck } from 'lucide-react'

interface RiskLevelCardProps {
  caseData: any
}

export default function RiskLevelCard({ caseData }: RiskLevelCardProps) {
  // Try retrieving risk data from multiple sources
  const getRiskData = () => {
    if (caseData?.risk_assessment && typeof caseData.risk_assessment === 'object') {
      return caseData.risk_assessment
    }
    
    try {
      const dashboardStr = localStorage.getItem('firDashboard')
      if (dashboardStr) {
        const parsed = JSON.parse(dashboardStr)
        const risk = parsed?.dashboard?.risk_assessment || parsed?.risk_assessment
        if (risk) {
          if (typeof risk === 'string') return JSON.parse(risk)
          return risk
        }
      }
    } catch (e) {
      console.error('Error parsing firDashboard for risk assessment:', e)
    }

    try {
      const caseStr = localStorage.getItem('caseData')
      if (caseStr) {
        const parsed = JSON.parse(caseStr)
        const risk = parsed?.risk_assessment
        if (risk) {
          if (typeof risk === 'string') return JSON.parse(risk)
          return risk
        }
      }
    } catch (e) {
      console.error('Error parsing caseData for risk assessment:', e)
    }

    return null
  }

  const risk = getRiskData()

  // Fallback default if risk data is not generated yet
  const threatLevel = (risk?.threat_level || risk?.risk_assessment || 'LOW').toUpperCase()
  const victimRisk = risk?.victim_risk || 'LOW'
  const publicSafety = risk?.public_safety_risk || 'LOW'
  const suspectFlight = risk?.suspect_flight_risk || 'LOW'
  const evidenceLoss = risk?.evidence_loss_risk || 'LOW'
  const priority = risk?.investigation_priority || 'MEDIUM'
  const responseTime = risk?.recommended_response_time || '24 Hours'
  const immediateActions = Array.isArray(risk?.immediate_actions) ? risk.immediate_actions : []

  // Determine styles based on threat level
  let levelColor = 'text-success border-success/20 bg-success/5'
  let levelIcon = <ShieldCheck className="w-5 h-5 text-success animate-pulse" />
  let levelText = 'LOW THREAT'

  if (threatLevel === 'HIGH' || threatLevel === 'CRITICAL') {
    levelColor = 'text-danger border-danger/30 bg-danger/5'
    levelIcon = <AlertOctagon className="w-5 h-5 text-danger animate-bounce" />
    levelText = 'HIGH THREAT'
  } else if (threatLevel === 'MEDIUM') {
    levelColor = 'text-warning border-warning/20 bg-warning/5'
    levelIcon = <ShieldAlert className="w-5 h-5 text-warning animate-pulse" />
    levelText = 'MEDIUM THREAT'
  }

  // Mini badge helpers
  const getBadgeColor = (val: string) => {
    const v = String(val).toUpperCase()
    if (v === 'HIGH' || v === 'CRITICAL') return 'text-danger bg-danger/10 border-danger/20'
    if (v === 'MEDIUM') return 'text-warning bg-warning/10 border-warning/20'
    return 'text-success bg-success/10 border-success/20'
  }

  return (
    <Card className="bg-card/50 backdrop-blur border-white/10">
      <CardHeader className="pb-3 border-b border-white/5">
        <CardTitle className="text-lg flex items-center gap-2">
          <ShieldAlert className="w-5 h-5 text-accent" />
          Threat & Risk Assessment
        </CardTitle>
        <CardDescription>
          AI-evaluated safety risk matrix and response priorities
        </CardDescription>
      </CardHeader>
      <CardContent className="p-5 space-y-4">
        {/* Main Threat Badge */}
        <div className={`flex items-center justify-between p-4 rounded-xl border ${levelColor}`}>
          <div className="flex items-center gap-3">
            {levelIcon}
            <div>
              <p className="text-[10px] text-muted-foreground uppercase font-bold">Overall Case Threat Level</p>
              <p className="text-base font-black tracking-wide">{levelText}</p>
            </div>
          </div>
          <div className="text-right">
            <p className="text-[10px] text-muted-foreground uppercase font-bold flex items-center gap-1 justify-end">
              <Clock className="w-3 h-3 text-muted-foreground" />
              Response Time
            </p>
            <p className="text-sm font-extrabold text-foreground">{responseTime}</p>
          </div>
        </div>

        {/* Risk Grid */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-2 text-xs">
          <div className="p-2.5 rounded-lg bg-secondary/10 border border-white/5">
            <span className="text-muted-foreground block text-[9px] uppercase font-bold">Victim Risk</span>
            <span className={`inline-block mt-1.5 px-2 py-0.5 rounded-full border text-[10px] font-bold ${getBadgeColor(victimRisk)}`}>
              {victimRisk}
            </span>
          </div>

          <div className="p-2.5 rounded-lg bg-secondary/10 border border-white/5">
            <span className="text-muted-foreground block text-[9px] uppercase font-bold">Public Safety</span>
            <span className={`inline-block mt-1.5 px-2 py-0.5 rounded-full border text-[10px] font-bold ${getBadgeColor(publicSafety)}`}>
              {publicSafety}
            </span>
          </div>

          <div className="p-2.5 rounded-lg bg-secondary/10 border border-white/5">
            <span className="text-muted-foreground block text-[9px] uppercase font-bold">Suspect Flight</span>
            <span className={`inline-block mt-1.5 px-2 py-0.5 rounded-full border text-[10px] font-bold ${getBadgeColor(suspectFlight)}`}>
              {suspectFlight}
            </span>
          </div>

          <div className="p-2.5 rounded-lg bg-secondary/10 border border-white/5">
            <span className="text-muted-foreground block text-[9px] uppercase font-bold">Evidence Loss</span>
            <span className={`inline-block mt-1.5 px-2 py-0.5 rounded-full border text-[10px] font-bold ${getBadgeColor(evidenceLoss)}`}>
              {evidenceLoss}
            </span>
          </div>
        </div>

        {/* Details and Actions */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
          <div className="p-3.5 rounded-xl bg-secondary/10 border border-white/5">
            <p className="text-[10px] text-muted-foreground uppercase font-bold tracking-wider mb-1.5">Priority Classification</p>
            <div className="flex justify-between items-center bg-card/60 p-2 rounded-lg border border-white/5">
              <span className="text-muted-foreground">Investigation Priority:</span>
              <span className={`px-2.5 py-0.5 rounded-full border text-[10px] font-bold ${getBadgeColor(priority)}`}>
                {priority}
              </span>
            </div>
          </div>

          {immediateActions.length > 0 && (
            <div className="p-3.5 rounded-xl bg-secondary/10 border border-white/5">
              <p className="text-[10px] text-muted-foreground uppercase font-bold tracking-wider mb-1.5">Immediate Response Actions</p>
              <ul className="space-y-1 bg-card/60 p-2 rounded-lg border border-white/5">
                {immediateActions.slice(0, 3).map((act: string, idx: number) => (
                  <li key={idx} className="text-[11px] text-foreground/90 flex items-start gap-1">
                    <span className="text-accent">•</span>
                    <span className="truncate">{act}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  )
}
