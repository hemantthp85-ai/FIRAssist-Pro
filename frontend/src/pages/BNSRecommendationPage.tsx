import { useState } from 'react'
import { motion } from 'framer-motion'
import { Link, useNavigate } from 'react-router-dom'
import {
  ArrowRight,
  BookOpen,
  CheckCircle2,
  X,
  Scale,
  AlertTriangle,
  Info,
  ChevronDown,
  ChevronUp,
  Gavel
} from 'lucide-react'
import { Card, CardContent } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { useToast } from '@/hooks'
import { cn } from '@/lib/utils'
import { mockBNSSections } from '@/data/mockData'
import type { BNSSection } from '@/types'

export default function BNSRecommendationPage() {
  const navigate = useNavigate()
  const { toast } = useToast()
  const [sections, setSections] = useState<BNSSection[]>(
    mockBNSSections.slice(0, 5).map(s => ({ ...s, isSelected: ['BNS 303', 'BNS 305'].includes(s.sectionNumber) }))
  )
  const [expandedSection, setExpandedSection] = useState<string | null>(null)

  const handleAccept = (sectionNumber: string) => {
    setSections(prev => prev.map(s =>
      s.sectionNumber === sectionNumber ? { ...s, isSelected: true } : s
    ))
    toast('BNS section accepted', 'success')
  }

  const handleReject = (sectionNumber: string) => {
    setSections(prev => prev.map(s =>
      s.sectionNumber === sectionNumber ? { ...s, isSelected: false } : s
    ))
    toast('BNS section rejected', 'info')
  }

  const selectedCount = sections.filter(s => s.isSelected).length
  const handleContinue = () => {
    navigate('/complaint/new/fir')
  }

  return (
    <div className="space-y-6 max-w-5xl mx-auto">
      {/* Page Header */}
      <div>
        <h1 className="text-3xl font-bold">BNS Section Recommendation</h1>
        <p className="text-muted-foreground mt-1">
          Review AI-suggested Bharatiya Nyaya Sanhita sections for this case
        </p>
      </div>

      {/* Steps Indicator */}
      <div className="flex items-center gap-4">
        {[
          'Complaint Intake',
          'Information Extraction',
          'Evidence & Documents',
          'Review & Confirm',
          'FIR Generation'
        ].map((step, i) => (
          <div key={step} className="flex items-center gap-2">
            <div className={cn(
              'w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium transition-colors',
              i === 3 ? 'bg-accent text-white' : i < 3 ? 'bg-success text-white' : 'bg-secondary text-muted-foreground'
            )}>
              {i < 3 ? <CheckCircle2 className="w-4 h-4" /> : i + 1}
            </div>
            <span className={cn(
              'text-sm hidden sm:block',
              i === 3 ? 'text-foreground' : 'text-muted-foreground'
            )}>
              {step}
            </span>
            {i < 4 && (
              <ArrowRight className="w-4 h-4 text-muted-foreground hidden sm:block" />
            )}
          </div>
        ))}
      </div>

      {/* Selection Summary */}
      <Card className="bg-card/50 backdrop-blur border-white/10">
        <CardContent className="p-5">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 rounded-xl bg-accent/20 flex items-center justify-center">
                <Scale className="w-6 h-6 text-accent" />
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Selected BNS Sections</p>
                <p className="text-2xl font-bold">{selectedCount} of {sections.length}</p>
              </div>
            </div>
            <div className="flex items-center gap-2">
              {sections.map(section => (
                <Badge
                  key={section.sectionNumber}
                  variant={section.isSelected ? 'default' : 'secondary'}
                  className="text-xs"
                >
                  {section.sectionNumber}
                </Badge>
              ))}
            </div>
          </div>
        </CardContent>
      </Card>

      {/* BNS Section Cards */}
      <div className="space-y-4">
        <h2 className="text-xl font-semibold flex items-center gap-2">
          <BookOpen className="w-5 h-5 text-accent" />
          Suggested BNS Sections
        </h2>

        {sections.map((section, index) => (
          <motion.div
            key={section.sectionNumber}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
          >
            <Card className={cn(
              "bg-card/50 backdrop-blur border-white/10 transition-all duration-300",
              section.isSelected && "border-success/30"
            )}>
              <CardContent className="p-5">
                {/* Header */}
                <div className="flex items-start justify-between mb-3">
                  <div className="flex items-center gap-3">
                    <div className={cn(
                      "w-12 h-12 rounded-xl flex items-center justify-center font-bold text-sm",
                      section.isSelected
                        ? "bg-success/20 text-success"
                        : "bg-secondary text-muted-foreground"
                    )}>
                      {section.sectionNumber}
                    </div>
                    <div>
                      <h3 className="font-semibold">{section.title}</h3>
                      <p className="text-xs text-muted-foreground">
                        {section.relatedCrimes.join(', ')}
                      </p>
                    </div>
                  </div>
                  <div className="flex items-center gap-2">
                    {section.isSelected ? (
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => handleReject(section.sectionNumber)}
                      >
                        <X className="w-4 h-4 mr-1" />
                        Reject
                      </Button>
                    ) : (
                      <Button
                        size="sm"
                        onClick={() => handleAccept(section.sectionNumber)}
                      >
                        <CheckCircle2 className="w-4 h-4 mr-1" />
                        Accept
                      </Button>
                    )}
                  </div>
                </div>

                {/* Description */}
                <p className="text-sm text-foreground/90 mb-3">
                  {section.description}
                </p>

                {/* Expand/Collapse */}
                <button
                  onClick={() => setExpandedSection(
                    expandedSection === section.sectionNumber ? null : section.sectionNumber
                  )}
                  className="flex items-center gap-1 text-xs text-accent hover:underline"
                >
                  {expandedSection === section.sectionNumber ? (
                    <>
                      <ChevronUp className="w-3 h-3" />
                      Show less
                    </>
                  ) : (
                    <>
                      <ChevronDown className="w-3 h-3" />
                      Show punishment details
                    </>
                  )}
                </button>

                {/* Expanded Content */}
                {expandedSection === section.sectionNumber && (
                  <motion.div
                    initial={{ opacity: 0, height: 0 }}
                    animate={{ opacity: 1, height: 'auto' }}
                    className="mt-4 p-4 bg-secondary/30 rounded-lg space-y-3"
                  >
                    <div>
                      <div className="flex items-center gap-2 text-sm font-medium mb-1">
                        <Gavel className="w-4 h-4 text-warning" />
                        Punishment
                      </div>
                      <p className="text-sm text-muted-foreground">
                        {section.punishment}
                      </p>
                    </div>
                    <div>
                      <div className="flex items-center gap-2 text-sm font-medium mb-1">
                        <Info className="w-4 h-4 text-accent" />
                        Why Recommended
                      </div>
                      <p className="text-sm text-muted-foreground">
                        This section is recommended because the complaint involves {section.title.toLowerCase()} activities
                        which fall under this legal framework. The AI detected keywords matching this section's criteria.
                      </p>
                    </div>
                    <div>
                      <div className="flex items-center gap-2 text-sm font-medium mb-1">
                        <AlertTriangle className="w-4 h-4 text-danger" />
                        Related Crimes
                      </div>
                      <div className="flex flex-wrap gap-2">
                        {section.relatedCrimes.map(crime => (
                          <Badge key={crime} variant="secondary" className="text-xs">
                            {crime}
                          </Badge>
                        ))}
                      </div>
                    </div>
                  </motion.div>
                )}
              </CardContent>
            </Card>
          </motion.div>
        ))}
      </div>

      {/* Action Buttons */}
      <div className="flex justify-between items-center pt-4">
        <Link to="/complaint/new/classification">
          <Button variant="outline">
            Back
          </Button>
        </Link>
        <Button
          size="lg"
          onClick={handleContinue}
          disabled={selectedCount === 0}
          className="min-w-[200px]"
        >
          Generate FIR Draft
          <ArrowRight className="w-5 h-5 ml-2" />
        </Button>
      </div>
    </div>
  )
}
