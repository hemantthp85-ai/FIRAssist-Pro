import { useState } from 'react'
import { motion } from 'framer-motion'
import {
  Search,
  Filter,
  BookOpen,
  Scale,
  AlertTriangle,
  ChevronDown,
  ChevronUp,
  Bookmark
} from 'lucide-react'
import { Card, CardContent } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Badge } from '@/components/ui/badge'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { mockBNSSections } from '@/data/mockData'
import type { CrimeType } from '@/types'

const crimeTypes: (CrimeType | 'All')[] = [
  'All', 'Theft', 'Assault', 'Cyber Crime', 'Fraud', 'Missing Person', 'Murder', 'Robbery'
]

export default function BNSKnowledgePage() {
  const [searchQuery, setSearchQuery] = useState('')
  const [categoryFilter, setCategoryFilter] = useState<string>('All')
  const [expandedSection, setExpandedSection] = useState<string | null>(null)

  const filteredSections = mockBNSSections.filter(section => {
    const matchesSearch = section.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         section.sectionNumber.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         section.description.toLowerCase().includes(searchQuery.toLowerCase())
    const matchesCategory = categoryFilter === 'All' || section.relatedCrimes.includes(categoryFilter as CrimeType)
    return matchesSearch && matchesCategory
  })

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div>
        <h1 className="text-3xl font-bold">BNS Knowledge Base</h1>
        <p className="text-muted-foreground mt-1">
          Search and explore Bharatiya Nyaya Sanhita (BNS) sections
        </p>
      </div>

      {/* Search and Filters */}
      <Card className="bg-card/50 backdrop-blur border-white/10">
        <CardContent className="p-4">
          <div className="flex flex-col md:flex-row gap-4">
            <div className="relative flex-1">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
              <Input
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search by section number, title, or keywords..."
                className="pl-10"
              />
            </div>
            <Select value={categoryFilter} onValueChange={setCategoryFilter}>
              <SelectTrigger className="w-full md:w-[200px]">
                <Filter className="w-4 h-4 mr-2" />
                <SelectValue placeholder="Filter by Crime Type" />
              </SelectTrigger>
              <SelectContent>
                {crimeTypes.map((type) => (
                  <SelectItem key={type} value={type}>{type}</SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
        </CardContent>
      </Card>

      {/* Results Count */}
      <div className="flex items-center justify-between">
        <p className="text-sm text-muted-foreground">
          Found {filteredSections.length} BNS sections
        </p>
      </div>

      {/* Section Cards */}
      <div className="space-y-4">
        {filteredSections.map((section, index) => (
          <motion.div
            key={section.sectionNumber}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.05 }}
          >
            <Card className="bg-card/50 backdrop-blur border-white/10">
              <CardContent className="p-5">
                {/* Header */}
                <div className="flex items-start justify-between mb-3">
                  <div className="flex items-start gap-4">
                    <div className="w-14 h-14 rounded-xl bg-accent/20 flex items-center justify-center">
                      <Scale className="w-6 h-6 text-accent" />
                    </div>
                    <div>
                      <div className="flex items-center gap-2 mb-1">
                        <Badge variant="default" className="text-sm">
                          {section.sectionNumber}
                        </Badge>
                        <Badge variant="secondary" className="text-xs">
                          BNS 2023
                        </Badge>
                      </div>
                      <h3 className="text-lg font-semibold">{section.title}</h3>
                    </div>
                  </div>
                  <Button variant="ghost" size="icon">
                    <Bookmark className="w-4 h-4" />
                  </Button>
                </div>

                {/* Description */}
                <p className="text-sm text-foreground/90 mb-3 px-[72px]">
                  {section.description}
                </p>

                {/* Related Crimes */}
                <div className="flex items-center gap-2 mb-3 px-[72px]">
                  <span className="text-xs text-muted-foreground">Related Crimes:</span>
                  <div className="flex flex-wrap gap-1">
                    {section.relatedCrimes.map(crime => (
                      <Badge key={crime} variant="outline" className="text-xs">
                        {crime}
                      </Badge>
                    ))}
                  </div>
                </div>

                {/* Expand/Collapse */}
                <button
                  onClick={() => setExpandedSection(
                    expandedSection === section.sectionNumber ? null : section.sectionNumber
                  )}
                  className="flex items-center gap-1 text-xs text-accent hover:underline ml-[72px]"
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
                    className="mt-4 ml-[72px] p-4 bg-secondary/30 rounded-lg space-y-3"
                  >
                    <div>
                      <div className="flex items-center gap-2 text-sm font-medium mb-1">
                        <AlertTriangle className="w-4 h-4 text-warning" />
                        Punishment
                      </div>
                      <p className="text-sm text-muted-foreground">
                        {section.punishment}
                      </p>
                    </div>
                  </motion.div>
                )}
              </CardContent>
            </Card>
          </motion.div>
        ))}
      </div>

      {filteredSections.length === 0 && (
        <div className="text-center py-12">
          <BookOpen className="w-12 h-12 text-muted-foreground mx-auto mb-4" />
          <h3 className="text-lg font-medium mb-2">No sections found</h3>
          <p className="text-sm text-muted-foreground">
            Try adjusting your search or filter criteria
          </p>
        </div>
      )}
    </div>
  )
}
