import { useState } from 'react'
import { motion } from 'framer-motion'
import { Link } from 'react-router-dom'
import { Shield, Eye, EyeOff, Lock, User, ArrowRight } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'

export default function LoginPage() {
  const [showPassword, setShowPassword] = useState(false)
  const [officerId, setOfficerId] = useState('')
  const [password, setPassword] = useState('')
  const [isLoading, setIsLoading] = useState(false)

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)
    // Simulate login
    setTimeout(() => {
      window.location.href = '/dashboard'
    }, 1500)
  }

  return (
    <div className="min-h-screen bg-background flex">
      {/* Left Section - Branding */}
      <div className="hidden lg:flex lg:w-1/2 relative overflow-hidden bg-gradient-to-br from-primary via-secondary to-primary">
        {/* Animated background */}
        <div className="absolute inset-0 overflow-hidden">
          <motion.div
            animate={{
              rotate: [0, 360],
            }}
            transition={{
              duration: 60,
              repeat: Infinity,
              ease: 'linear'
            }}
            className="absolute -top-1/4 -left-1/4 w-1/2 h-1/2 bg-accent/10 rounded-full blur-3xl"
          />
          <motion.div
            animate={{
              rotate: [360, 0],
            }}
            transition={{
              duration: 80,
              repeat: Infinity,
              ease: 'linear'
            }}
            className="absolute -bottom-1/4 -right-1/4 w-1/2 h-1/2 bg-success/10 rounded-full blur-3xl"
          />
        </div>

        <div className="relative z-10 flex flex-col justify-center px-12">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
          >
            <div className="flex items-center gap-4 mb-8">
              <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-accent to-success flex items-center justify-center shadow-xl shadow-accent/25">
                <Shield className="w-8 h-8 text-white" />
              </div>
              <div>
                <h1 className="text-3xl font-bold">FORTHRIGHT</h1>
                <p className="text-muted-foreground">AI-Powered FIR Platform</p>
              </div>
            </div>

            <h2 className="text-4xl font-bold mb-4">
              Transform FIR Generation with AI
            </h2>
            <p className="text-lg text-muted-foreground mb-8 max-w-lg">
              Voice-powered complaint intake, intelligent information extraction,
              and automated FIR drafting for Tamil Nadu Police.
            </p>

            <div className="flex items-center gap-8">
              <div>
                <div className="text-3xl font-bold text-gradient">50,000+</div>
                <div className="text-sm text-muted-foreground">FIRs Generated</div>
              </div>
              <div className="w-px h-12 bg-white/20" />
              <div>
                <div className="text-3xl font-bold text-gradient">15,000+</div>
                <div className="text-sm text-muted-foreground">Officers</div>
              </div>
              <div className="w-px h-12 bg-white/20" />
              <div>
                <div className="text-3xl font-bold text-gradient">99.2%</div>
                <div className="text-sm text-muted-foreground">Accuracy</div>
              </div>
            </div>
          </motion.div>
        </div>
      </div>

      {/* Right Section - Login Form */}
      <div className="w-full lg:w-1/2 flex items-center justify-center p-8">
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.6 }}
          className="w-full max-w-md"
        >
          {/* Mobile Logo */}
          <div className="lg:hidden flex items-center justify-center gap-3 mb-8">
            <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-accent to-success flex items-center justify-center">
              <Shield className="w-6 h-6 text-white" />
            </div>
            <div className="text-center">
              <h1 className="text-2xl font-bold">FORTHRIGHT</h1>
              <p className="text-xs text-muted-foreground">Tamil Nadu Police</p>
            </div>
          </div>

          <Card className="bg-card/50 backdrop-blur-xl border-white/10">
            <CardHeader className="text-center pb-2">
              <CardTitle className="text-2xl">Officer Login</CardTitle>
              <CardDescription>
                Access the FIR generation platform with your credentials
              </CardDescription>
            </CardHeader>
            <CardContent className="pt-4">
              <form onSubmit={handleSubmit} className="space-y-4">
                <div className="space-y-2">
                  <label className="text-sm font-medium">Officer ID</label>
                  <div className="relative">
                    <User className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                    <Input
                      value={officerId}
                      onChange={(e) => setOfficerId(e.target.value)}
                      placeholder="Enter your Officer ID"
                      className="pl-10"
                      required
                    />
                  </div>
                </div>

                <div className="space-y-2">
                  <label className="text-sm font-medium">Password</label>
                  <div className="relative">
                    <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                    <Input
                      type={showPassword ? 'text' : 'password'}
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
                      placeholder="Enter your password"
                      className="pl-10 pr-10"
                      required
                    />
                    <button
                      type="button"
                      onClick={() => setShowPassword(!showPassword)}
                      className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground transition-colors"
                    >
                      {showPassword ? (
                        <EyeOff className="w-4 h-4" />
                      ) : (
                        <Eye className="w-4 h-4" />
                      )}
                    </button>
                  </div>
                </div>

                <div className="flex items-center justify-between text-sm">
                  <label className="flex items-center gap-2 cursor-pointer">
                    <input
                      type="checkbox"
                      className="w-4 h-4 rounded border-border accent-accent"
                    />
                    Remember me
                  </label>
                  <Link
                    to="#"
                    className="text-accent hover:underline"
                  >
                    Forgot Password?
                  </Link>
                </div>

                <Button
                  type="submit"
                  size="lg"
                  className="w-full"
                  disabled={isLoading}
                >
                  {isLoading ? (
                    <motion.div
                      animate={{ rotate: 360 }}
                      transition={{ duration: 1, repeat: Infinity, ease: 'linear' }}
                      className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full"
                    />
                  ) : (
                    <>
                      Login to Dashboard
                      <ArrowRight className="w-4 h-4 ml-2" />
                    </>
                  )}
                </Button>
              </form>

              <div className="mt-6 pt-6 border-t border-border text-center">
                <p className="text-sm text-muted-foreground">
                  For login assistance, contact IT Helpdesk
                </p>
                <p className="text-xs text-muted-foreground mt-1">
                  helpdesk@tnpolice.gov.in | 044-2844-7777
                </p>
              </div>
            </CardContent>
          </Card>

          <p className="text-center text-xs text-muted-foreground mt-8">
            Government of Tamil Nadu | Police Department
          </p>
        </motion.div>
      </div>
    </div>
  )
}
