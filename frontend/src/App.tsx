import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { ThemeProvider, ToastProvider } from '@/hooks'
import { DashboardLayout } from '@/components/layout/DashboardLayout'

// Pages
import LandingPage from '@/pages/LandingPage'
import LoginPage from '@/pages/LoginPage'
import DashboardPage from '@/pages/DashboardPage'
import NewComplaintPage from '@/pages/NewComplaintPage'
import ActiveCasesPage from '@/pages/ActiveCasesPage'
import InformationExtractionPage from '@/pages/InformationExtractionPage'
import EvidenceDocumentsPage from '@/pages/EvidenceDocumentsPage'
import MissingInfoPage from '@/pages/MissingInfoPage'
import CrimeClassificationPage from '@/pages/CrimeClassificationPage'
import BNSRecommendationPage from '@/pages/BNSRecommendationPage'
import FIRGeneratorPage from '@/pages/FIRGeneratorPage'
import FIRHistoryPage from '@/pages/FIRHistoryPage'
import AnalyticsPage from '@/pages/AnalyticsPage'
import BNSKnowledgePage from '@/pages/BNSKnowledgePage'
import SettingsPage from '@/pages/SettingsPage'

function App() {
  return (
    <ThemeProvider>
      <ToastProvider>
        <BrowserRouter>
          <Routes>
            {/* Public routes */}
            <Route path="/" element={<LandingPage />} />
            <Route path="/login" element={<LoginPage />} />

            {/* Protected dashboard routes */}
            <Route element={<DashboardLayout />}>
              <Route path="/dashboard" element={<DashboardPage />} />
              <Route path="/complaint/new" element={<NewComplaintPage />} />
              <Route path="/complaint/:id" element={<NewComplaintPage />} />
              <Route path="/complaint/:id/extraction" element={<InformationExtractionPage />} />
              <Route path="/complaint/:id/evidence" element={<EvidenceDocumentsPage />} />
              <Route path="/complaint/:id/missing" element={<MissingInfoPage />} />
              <Route path="/complaint/:id/classification" element={<CrimeClassificationPage />} />
              <Route path="/complaint/:id/bns" element={<BNSRecommendationPage />} />
              <Route path="/complaint/:id/fir" element={<FIRGeneratorPage />} />
              <Route path="/cases" element={<ActiveCasesPage />} />
              <Route path="/history" element={<FIRHistoryPage />} />
              <Route path="/analytics" element={<AnalyticsPage />} />
              <Route path="/bns" element={<BNSKnowledgePage />} />
              <Route path="/settings" element={<SettingsPage />} />
            </Route>
          </Routes>
        </BrowserRouter>
      </ToastProvider>
    </ThemeProvider>
  )
}

export default App
