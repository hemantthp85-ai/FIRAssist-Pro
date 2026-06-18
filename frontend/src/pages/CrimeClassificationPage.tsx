import { useState } from 'react'
import { motion } from 'framer-motion'
import { Link, useNavigate } from 'react-router-dom'
import {
  ArrowRight,
  CheckCircle2,
  Shield,
  Lock,
  AlertTriangle,
  Monitor,
  BadgeAlert,
  UserX,
  Skull,
  Gem,
  HeartOff,
  Home,
  FileQuestion
} from 'lucide-react'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { cn } from '@/lib/utils'
import type { CrimeType } from '@/types'

interface CrimeCategory {
  type: CrimeType
  icon: React.ElementType
  description: string
  gradient: string
  cases: number
}

const crimeCategories: CrimeCategory[] = [
  {
    type: 'Theft',
    icon: Lock,
    description: 'Property theft without force',
    gradient: 'from-yellow-500 to-orange-500',
    cases: 412
  },
  {
    type: 'Assault',
    icon: AlertTriangle,
    description: 'Physical assault or violence',
    gradient: 'from-red-500 to-pink-500',
    cases: 287
  },
  {
    type: 'Cyber Crime',
    icon: Monitor,
    description: 'Online fraud, hacking, cyber threats',
    gradient: 'from-blue-500 to-cyan-500',
    cases: 156
  },
  {
    type: 'Fraud',
    icon: BadgeAlert,
    description: 'Financial fraud, scams, cheating',
    gradient: 'from-purple-500 to-indigo-500',
    cases: 198
  },
  {
    type: 'Missing Person',
    icon: UserX,
    description: 'Missing person reports',
    gradient: 'from-gray-500 to-slate-500',
    cases: 89
  },
  {
    type: 'Murder',
    icon: Skull,
    description: 'Homicide cases',
    gradient: 'from-red-600 to-red-800',
    cases: 23
  },
  {
    type: 'Robbery',
    icon: Gem,
    description: 'Theft with force or threat',
    gradient: 'from-amber-500 to-yellow-600',
    cases: 45
  },
  {
    type: 'Domestic Violence',
    icon: HeartOff,
    description: 'Domestic dispute and violence',
    gradient: 'from-pink-500 to-rose-500',
    cases: 123
  },
  {
    type: 'Property Dispute',
    icon: Home,
    description: 'Land and property disputes',
    gradient: 'from-emerald-500 to-teal-500',
    cases: 67
  },
  {
    type: 'Other',
    icon: FileQuestion,
    description: 'Other types of complaints',
    gradient: 'from-gray-400 to-gray-500',
    cases: 47
  }
]

export default function CrimeClassificationPage() {
  const navigate = useNavigate()
  const [selectedCategory, setSelectedCategory] = useState<CrimeType>('Theft')
  const [aiDetected] = useState(true)

  const handleContinue = () => {
    navigate('/complaint/new/bns')
  }

  return (
    <div className="space-y-6 max-w-6xl mx-auto">
      {/* Page Header */}
      <div>
        <h1 className="text-3xl font-bold">Crime Classification</h1>
        <p className="text-muted-foreground mt-1">
          Select or confirm the crime category for this complaint
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

      {/* AI Detection Banner */}
      {aiDetected && (
        <motion.div
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          className="glass-dark rounded-xl p-4 flex items-center justify-between"
        >
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-accent/20 flex items-center justify-center">
              <Shield className="w-5 h-5 text-accent" />
            </div>
            <div>
              <p className="font-medium">AI Detection: Theft</p>
              <p className="text-sm text-muted-foreground">
                Based on keywords: "stolen", "motorcycle", "parked"
              </p>
            </div>
          </div>
          <Badge variant="default" className="bg-success/20 text-success border-success/30">
            98% Confidence
          </Badge>
        </motion.div>
      )}

      {/* Crime Category Grid */}
      <div className="grid sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {crimeCategories.map((category, index) => {
          const isSelected = selectedCategory === category.type
          return (
            <motion.div
              key={category.type}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.05 }}
            >
              <Card
                className={cn(
                  "bg-card/50 backdrop-blur border-white/10 cursor-pointer transition-all duration-300 hover:scale-[1.02]",
                  isSelected && "border-accent shadow-lg shadow-accent/20 ring-2 ring-accent/50"
                )}
                onClick={() => setSelectedCategory(category.type)}
              >
                <CardContent className="p-5">
                  <div className="flex items-start justify-between mb-3">
                    <div className={cn(
                      "w-12 h-12 rounded-xl bg-gradient-to-br flex items-center justify-center",
                      category.gradient
                    )}>
                      <category.icon className="w-6 h-6 text-white" />
                    </div>
                    {isSelected && (
                      <motion.div
                        initial={{ scale: 0 }}
                        animate={{ scale: 1 }}
                        className="w-6 h-6 rounded-full bg-accent flex items-center justify-center"
                      >
                        <CheckCircle2 className="w-4 h-4 text-white" />
                      </motion.div>
                    )}
                  </div>
                  <h3 className="font-semibold mb-1">{category.type}</h3>
                  <p className="text-xs text-muted-foreground mb-2">
                    {category.description}
                  </p>
                  <div className="flex items-center justify-between">
                    <Badge variant="secondary" className="text-xs">
                      {category.cases} cases this month
                    </Badge>
                  </div>
                </CardContent>
              </Card>
            </motion.div>
          )
        })}
      </div>

      {/* Selected Category Details */}
      <Card className="bg-card/50 backdrop-blur border-white/10">
        <CardHeader>
          <CardTitle>Selected Crime Category</CardTitle>
          <CardDescription>
            Confirm this classification to proceed with BNS section recommendations
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex items-center gap-4">
            <div className={cn(
              "w-16 h-16 rounded-xl bg-gradient-to-br flex items-center justify-center",
              crimeCategories.find(c => c.type === selectedCategory)?.gradient
            )}>
              {(() => {
                const Icon = crimeCategories.find(c => c.type === selectedCategory)?.icon || Lock
                return <Icon className="w-8 h-8 text-white" />
              })()}
            </div>
            <div className="flex-1">
              <h3 className="text-xl font-bold">{selectedCategory}</h3>
              <p className="text-muted-foreground">
                {crimeCategories.find(c => c.type === selectedCategory)?.description}
              </p>
            </div>
            <Button
              variant="outline"
              onClick={() => setSelectedCategory('Theft')}
            >
              Change
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Action Buttons */}
      <div className="flex justify-between items-center pt-4">
        <Link to="/complaint/new/missing">
          <Button variant="outline">
            Back
          </Button>
        </Link>
        <Button
          size="lg"
          onClick={handleContinue}
          className="min-w-[200px]"
        >
          Get BNS Recommendations
          <ArrowRight className="w-5 h-5 ml-2" />
        </Button>
      </div>
    </div>
  )
}
