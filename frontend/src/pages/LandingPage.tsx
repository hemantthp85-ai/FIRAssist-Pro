import { motion } from 'framer-motion'
import { Link } from 'react-router-dom'
import {
  Mic,
  FileSearch,
  AlertCircle,
  BookOpen,
  FileText,
  Languages,
  Shield,
  ArrowRight,
  Users,
  FileCheck,
  Clock,
  TrendingUp,
  ChevronRight
} from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card, CardContent } from '@/components/ui/card'

const features = [
  {
    icon: Mic,
    title: 'Voice Complaint Intake',
    description: 'Record complaints via voice input with real-time speech-to-text conversion powered by AI.',
    gradient: 'from-blue-500 to-cyan-500'
  },
  {
    icon: FileSearch,
    title: 'AI Information Extraction',
    description: 'Automatically extract key details from complaints using intelligent NLP analysis.',
    gradient: 'from-purple-500 to-pink-500'
  },
  {
    icon: AlertCircle,
    title: 'Missing Detail Detection',
    description: 'Intelligently identify gaps in information and generate follow-up questions.',
    gradient: 'from-orange-500 to-red-500'
  },
  {
    icon: BookOpen,
    title: 'BNS Section Recommendation',
    description: 'Get AI-powered suggestions for relevant Bharatiya Nyaya Sanhita sections.',
    gradient: 'from-green-500 to-emerald-500'
  },
  {
    icon: FileText,
    title: 'FIR Draft Generation',
    description: 'Generate complete FIR drafts automatically from extracted information.',
    gradient: 'from-indigo-500 to-violet-500'
  },
  {
    icon: Languages,
    title: 'Multilingual Support',
    description: 'Support for Tamil, English, and other regional languages for citizen complaints.',
    gradient: 'from-teal-500 to-cyan-500'
  }
]

const stats = [
  { icon: FileCheck, value: '50,000+', label: 'FIRs Generated' },
  { icon: Users, value: '15,000+', label: 'Officers Onboarded' },
  { icon: Clock, value: '85%', label: 'Time Saved' },
  { icon: TrendingUp, value: '99.2%', label: 'Accuracy Rate' }
]

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-background">
      {/* Navigation */}
      <nav className="fixed top-0 left-0 right-0 z-50 bg-primary/80 backdrop-blur-xl border-b border-white/10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-accent to-success flex items-center justify-center">
                <Shield className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="font-bold text-lg tracking-tight">FORTHRIGHT AI</h1>
              </div>
            </div>
            <div className="flex items-center gap-4">
              <Link to="/login">
                <Button variant="ghost">Login</Button>
              </Link>
              <Link to="/login">
                <Button>
                  Get Started
                  <ArrowRight className="w-4 h-4 ml-2" />
                </Button>
              </Link>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="pt-32 pb-20 px-4 relative overflow-hidden">
        {/* Background elements */}
        <div className="absolute inset-0 overflow-hidden">
          <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-accent/20 rounded-full blur-3xl" />
          <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-success/20 rounded-full blur-3xl" />
          <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-accent/5 rounded-full blur-3xl" />
        </div>

        <div className="max-w-7xl mx-auto relative z-10">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="text-center"
          >
            <motion.div
              initial={{ scale: 0.9, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              transition={{ delay: 0.2, duration: 0.5 }}
              className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-accent/10 border border-accent/20 text-accent text-sm font-medium mb-8"
            >
              <Shield className="w-4 h-4" />
              Tamil Nadu Police Department
            </motion.div>

            <h1 className="text-5xl md:text-7xl font-extrabold tracking-tight mb-6">
              <span className="bg-gradient-to-r from-white via-gray-100 to-gray-300 bg-clip-text text-transparent">
                FORTHRIGHT
              </span>
              <span className="text-gradient ml-3">AI</span>
            </h1>

            <p className="text-xl md:text-2xl text-muted-foreground max-w-3xl mx-auto mb-4 font-light">
              Agentic AI-Based FIR Generation and Legal Assistance Platform
            </p>

            <p className="text-muted-foreground max-w-2xl mx-auto mb-12">
              Transform the way complaints are processed with AI-powered voice intake,
              automatic information extraction, and intelligent FIR generation.
            </p>

            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link to="/login">
                <Button size="xl" className="min-w-[200px]">
                  Start Filing FIR
                  <ArrowRight className="w-5 h-5 ml-2" />
                </Button>
              </Link>
              <Button size="xl" variant="outline" className="min-w-[200px]">
                Watch Demo
              </Button>
            </div>
          </motion.div>

          {/* Hero Image/Preview */}
          <motion.div
            initial={{ opacity: 0, y: 50 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.5, duration: 0.8 }}
            className="mt-20 relative"
          >
            <div className="absolute inset-0 bg-gradient-to-t from-background via-transparent to-transparent z-10" />
            <div className="rounded-2xl overflow-hidden border border-white/10 shadow-2xl shadow-accent/10">
              <div className="bg-secondary/50 backdrop-blur-xl p-1">
                <div className="flex items-center gap-2 px-4 py-2 border-b border-white/10">
                  <div className="flex gap-1.5">
                    <div className="w-3 h-3 rounded-full bg-red-500" />
                    <div className="w-3 h-3 rounded-full bg-yellow-500" />
                    <div className="w-3 h-3 rounded-full bg-green-500" />
                  </div>
                  <div className="flex-1 text-center text-xs text-muted-foreground">
                    forthright-ai.tnpolice.gov.in
                  </div>
                </div>
                <div className="aspect-[16/9] bg-gradient-to-br from-secondary to-primary relative overflow-hidden">
                  {/* Mock Dashboard Preview */}
                  <div className="absolute inset-4 rounded-xl bg-card/50 backdrop-blur border border-white/10 p-4">
                    <div className="flex gap-4 h-full">
                      <div className="w-48 rounded-lg bg-secondary/50 p-3 hidden md:block">
                        <div className="space-y-2">
                          {[1,2,3,4,5].map(i => (
                            <div key={i} className={`h-8 rounded ${i === 1 ? 'bg-accent/20' : 'bg-white/5'}`} />
                          ))}
                        </div>
                      </div>
                      <div className="flex-1 space-y-4">
                        <div className="grid grid-cols-4 gap-4">
                          {[1,2,3,4].map(i => (
                            <div key={i} className="h-24 rounded-lg bg-white/5 animate-pulse" />
                          ))}
                        </div>
                        <div className="grid grid-cols-2 gap-4">
                          <div className="h-48 rounded-lg bg-white/5" />
                          <div className="h-48 rounded-lg bg-white/5" />
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-24 px-4 relative">
        <div className="max-w-7xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-3xl md:text-4xl font-bold mb-4">
              Powerful AI-Driven Features
            </h2>
            <p className="text-muted-foreground max-w-2xl mx-auto">
              Streamline your complaint handling process with our comprehensive AI toolkit
            </p>
          </motion.div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {features.map((feature, index) => (
              <motion.div
                key={feature.title}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.1 }}
              >
                <Card className="group h-full bg-card/50 backdrop-blur border-white/10 hover:border-accent/50 transition-all duration-300 hover:shadow-lg hover:shadow-accent/5">
                  <CardContent className="p-6">
                    <div className={`w-12 h-12 rounded-xl bg-gradient-to-br ${feature.gradient} flex items-center justify-center mb-4 group-hover:scale-110 transition-transform duration-300`}>
                      <feature.icon className="w-6 h-6 text-white" />
                    </div>
                    <h3 className="text-lg font-semibold mb-2">{feature.title}</h3>
                    <p className="text-sm text-muted-foreground">{feature.description}</p>
                  </CardContent>
                </Card>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Statistics Section */}
      <section className="py-24 px-4 bg-gradient-to-b from-transparent via-accent/5 to-transparent">
        <div className="max-w-7xl mx-auto">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
            {stats.map((stat, index) => (
              <motion.div
                key={stat.label}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.1 }}
                className="text-center"
              >
                <div className="inline-flex items-center justify-center w-14 h-14 rounded-full bg-accent/10 mb-4">
                  <stat.icon className="w-6 h-6 text-accent" />
                </div>
                <div className="text-4xl font-bold text-gradient mb-1">{stat.value}</div>
                <div className="text-sm text-muted-foreground">{stat.label}</div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-24 px-4">
        <div className="max-w-4xl mx-auto">
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            whileInView={{ opacity: 1, scale: 1 }}
            viewport={{ once: true }}
            className="glass-dark rounded-2xl p-8 md:p-12 text-center"
          >
            <Shield className="w-12 h-12 text-accent mx-auto mb-6" />
            <h2 className="text-3xl font-bold mb-4">
              Ready to Transform Your FIR Process?
            </h2>
            <p className="text-muted-foreground mb-8 max-w-xl mx-auto">
              Join thousands of officers across Tamil Nadu using FORTHRIGHT AI to
              streamline complaint handling and FIR generation.
            </p>
            <Link to="/login">
              <Button size="lg" className="min-w-[200px]">
                Access Platform
                <ChevronRight className="w-4 h-4 ml-2" />
              </Button>
            </Link>
          </motion.div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-white/10 py-12 px-4">
        <div className="max-w-7xl mx-auto">
          <div className="flex flex-col md:flex-row justify-between items-center gap-6">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-accent to-success flex items-center justify-center">
                <Shield className="w-5 h-5 text-white" />
              </div>
              <div>
                <p className="font-bold">FORTHRIGHT AI</p>
                <p className="text-xs text-muted-foreground">Tamil Nadu Police Department</p>
              </div>
            </div>
            <div className="flex gap-8 text-sm text-muted-foreground">
              <a href="#" className="hover:text-foreground transition-colors">Privacy Policy</a>
              <a href="#" className="hover:text-foreground transition-colors">Terms of Service</a>
              <a href="#" className="hover:text-foreground transition-colors">Support</a>
            </div>
            <p className="text-xs text-muted-foreground">
              2024 Tamil Nadu Police. All rights reserved.
            </p>
          </div>
        </div>
      </footer>
    </div>
  )
}
