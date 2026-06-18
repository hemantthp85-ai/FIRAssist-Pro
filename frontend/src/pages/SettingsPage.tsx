import { useState } from 'react'
import {
  Moon,
  Sun,
  Globe,
  Bell,
  User,
  Shield,
  Download,
  Trash2,
  Save
} from 'lucide-react'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Switch } from '@/components/ui/switch'
import { Badge } from '@/components/ui/badge'
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { useToast, useTheme } from '@/hooks'
import { mockOfficer } from '@/data/mockData'

export default function SettingsPage() {
  const { theme, toggleTheme } = useTheme()
  const { toast } = useToast()
  const [language, setLanguage] = useState('english')
  const [notifications, setNotifications] = useState({
    email: true,
    push: true,
    sms: false
  })
  const [autoSave, setAutoSave] = useState(true)
  const [soundEffects, setSoundEffects] = useState(true)

  const handleSave = () => {
    toast('Settings saved successfully', 'success')
  }

  const handleExportData = () => {
    toast('Data export started', 'info')
  }

  return (
    <div className="space-y-6 max-w-4xl mx-auto">
      {/* Page Header */}
      <div>
        <h1 className="text-3xl font-bold">Settings</h1>
        <p className="text-muted-foreground mt-1">
          Manage your account and application preferences
        </p>
      </div>

      {/* Profile Section */}
      <Card className="bg-card/50 backdrop-blur border-white/10">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <User className="w-5 h-5 text-accent" />
            Officer Profile
          </CardTitle>
          <CardDescription>
            Your official profile information
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          <div className="flex items-center gap-6">
            <Avatar className="w-20 h-20 border-4 border-accent/30">
              <AvatarImage src="" />
              <AvatarFallback className="bg-gradient-to-br from-accent to-success text-white font-bold text-2xl">
                {mockOfficer.name.split(' ').map(n => n[0]).join('')}
              </AvatarFallback>
            </Avatar>
            <div className="flex-1">
              <h3 className="text-xl font-semibold">{mockOfficer.name}</h3>
              <p className="text-muted-foreground">{mockOfficer.rank}</p>
              <div className="flex items-center gap-4 mt-2">
                <Badge variant="secondary">{mockOfficer.badge}</Badge>
                <Badge variant="outline">{mockOfficer.station}</Badge>
              </div>
            </div>
          </div>

          <div className="grid md:grid-cols-2 gap-4">
            <div className="space-y-2">
              <label className="text-sm font-medium">Officer ID</label>
              <Input value={mockOfficer.id} disabled />
            </div>
            <div className="space-y-2">
              <label className="text-sm font-medium">Email</label>
              <Input value={mockOfficer.email} disabled />
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Appearance */}
      <Card className="bg-card/50 backdrop-blur border-white/10">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            {theme === 'dark' ? <Moon className="w-5 h-5 text-accent" /> : <Sun className="w-5 h-5 text-warning" />}
            Appearance
          </CardTitle>
          <CardDescription>
            Customize the look and feel of the application
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex items-center justify-between p-4 bg-secondary/30 rounded-lg">
            <div>
              <p className="font-medium">Dark Mode</p>
              <p className="text-sm text-muted-foreground">Use dark theme for better visibility in low light</p>
            </div>
            <Switch
              checked={theme === 'dark'}
              onCheckedChange={toggleTheme}
            />
          </div>

          <div className="flex items-center justify-between p-4 bg-secondary/30 rounded-lg">
            <div>
              <p className="font-medium">Sound Effects</p>
              <p className="text-sm text-muted-foreground">Play sounds for notifications and actions</p>
            </div>
            <Switch
              checked={soundEffects}
              onCheckedChange={setSoundEffects}
            />
          </div>
        </CardContent>
      </Card>

      {/* Language */}
      <Card className="bg-card/50 backdrop-blur border-white/10">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Globe className="w-5 h-5 text-accent" />
            Language & Region
          </CardTitle>
          <CardDescription>
            Set your preferred language for the interface
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex items-center justify-between p-4 bg-secondary/30 rounded-lg">
            <div>
              <p className="font-medium">Interface Language</p>
              <p className="text-sm text-muted-foreground">Choose your preferred language</p>
            </div>
            <Select value={language} onValueChange={setLanguage}>
              <SelectTrigger className="w-[180px]">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="english">English</SelectItem>
                <SelectItem value="tamil">Tamil</SelectItem>
                <SelectItem value="hindi">Hindi</SelectItem>
              </SelectContent>
            </Select>
          </div>
        </CardContent>
      </Card>

      {/* Notifications */}
      <Card className="bg-card/50 backdrop-blur border-white/10">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Bell className="w-5 h-5 text-accent" />
            Notifications
          </CardTitle>
          <CardDescription>
            Configure how you receive notifications
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex items-center justify-between p-4 bg-secondary/30 rounded-lg">
            <div>
              <p className="font-medium">Email Notifications</p>
              <p className="text-sm text-muted-foreground">Receive updates via email</p>
            </div>
            <Switch
              checked={notifications.email}
              onCheckedChange={(checked) => setNotifications(prev => ({ ...prev, email: checked }))}
            />
          </div>

          <div className="flex items-center justify-between p-4 bg-secondary/30 rounded-lg">
            <div>
              <p className="font-medium">Push Notifications</p>
              <p className="text-sm text-muted-foreground">Get in-app notifications</p>
            </div>
            <Switch
              checked={notifications.push}
              onCheckedChange={(checked) => setNotifications(prev => ({ ...prev, push: checked }))}
            />
          </div>

          <div className="flex items-center justify-between p-4 bg-secondary/30 rounded-lg">
            <div>
              <p className="font-medium">SMS Alerts</p>
              <p className="text-sm text-muted-foreground">Receive critical alerts via SMS</p>
            </div>
            <Switch
              checked={notifications.sms}
              onCheckedChange={(checked) => setNotifications(prev => ({ ...prev, sms: checked }))}
            />
          </div>
        </CardContent>
      </Card>

      {/* Editor Settings */}
      <Card className="bg-card/50 backdrop-blur border-white/10">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Shield className="w-5 h-5 text-accent" />
            Editor Settings
          </CardTitle>
          <CardDescription>
            Configure auto-save and editor behavior
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex items-center justify-between p-4 bg-secondary/30 rounded-lg">
            <div>
              <p className="font-medium">Auto-Save Drafts</p>
              <p className="text-sm text-muted-foreground">Automatically save FIR drafts every 30 seconds</p>
            </div>
            <Switch
              checked={autoSave}
              onCheckedChange={setAutoSave}
            />
          </div>
        </CardContent>
      </Card>

      {/* Data Management */}
      <Card className="bg-card/50 backdrop-blur border-white/10">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Download className="w-5 h-5 text-accent" />
            Data Management
          </CardTitle>
          <CardDescription>
            Export or manage your stored data
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <Button variant="outline" className="w-full justify-start" onClick={handleExportData}>
            <Download className="w-4 h-4 mr-2" />
            Export All My Data
          </Button>
          <Button variant="outline" className="w-full justify-start text-danger hover:bg-danger/10">
            <Trash2 className="w-4 h-4 mr-2" />
            Delete Local Data
          </Button>
        </CardContent>
      </Card>

      {/* Save Button */}
      <div className="flex justify-end">
        <Button size="lg" onClick={handleSave} className="min-w-[200px]">
          <Save className="w-4 h-4 mr-2" />
          Save Settings
        </Button>
      </div>
    </div>
  )
}
