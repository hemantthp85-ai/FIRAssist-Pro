import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { Link, useNavigate } from 'react-router-dom'
import {
  User,
  Phone,
  MapPin,
  Calendar,
  Clock,
  AlertTriangle,
  FileText,
  ArrowRight,
  CheckCircle2,
  Sparkles,
  Shield
} from 'lucide-react'
import { Card, CardContent } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Progress } from '@/components/ui/progress'
import { cn } from '@/lib/utils'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'

interface ExtractedField {
  id: string
  label: string
  value: string
  icon: React.ElementType
  confidence: number
  isEditing: boolean
}



export default function InformationExtractionPage() {
  const navigate = useNavigate()
  const [isExtracting, setIsExtracting] = useState(true)
  const [fields, setFields] = useState<ExtractedField[]>([])
  const [extractionProgress, setExtractionProgress] = useState(0)

  const getValue = (...values: unknown[]) => {
    const value = values.find(item =>
      item !== undefined &&
      item !== null &&
      String(item).trim() !== ""
    )

    return value === undefined || value === null
      ? ""
      : String(value)
  }

  const getListValue = (...values: unknown[]) => {
    const value = values.find(item => {
      if (Array.isArray(item)) return item.length > 0

      return item !== undefined &&
        item !== null &&
        String(item).trim() !== ""
    })

    if (Array.isArray(value)) {
      return value
        .map(item =>
          typeof item === "string"
            ? item
            : item?.title || item?.section || ""
        )
        .filter(Boolean)
        .join(", ")
    }

    return value === undefined || value === null
      ? ""
      : String(value)
  }

useEffect(() => {

  const dashboardData = JSON.parse(
    localStorage.getItem("firDashboard") || "{}"
  )

  console.log("FULL API RESPONSE", dashboardData)
  console.log("DASHBOARD", dashboardData.dashboard)

  console.log(
    "DASHBOARD DATA:",
    dashboardData
  )
console.log(
  "CASE OVERVIEW:",
  dashboardData?.dashboard?.case_overview
)

console.log(
  "INCIDENT:",
  dashboardData?.dashboard?.case_overview?.incident
)

console.log(
  "COMPLAINANT:",
  dashboardData?.dashboard?.case_overview?.complainant
)

console.log(
  "ACCUSED:",
  dashboardData?.dashboard?.case_overview?.accused
)
  const dashboard =
    dashboardData?.dashboard || {}
  const caseData =
    dashboard?.case_overview ||
    {}
  const legalAnalysis =
    dashboard?.legal_analysis || {}
  const incident =
    caseData?.incident || {}

  const complainant =
    caseData?.complainant || {}

  const accused =
    caseData?.accused || {}
const incidentSummary =
  getValue(
    caseData?.incident_summary,
    caseData?.summary,
    incident.Summary,
    incident.summary
  )

const incidentDate =
  getValue(
    caseData?.incident_date,
    caseData?.date,
    incident.Date,
    incident.date
  )

const incidentTime =
  getValue(
    caseData?.incident_time,
    caseData?.time,
    incident.Time,
    incident.time
  )

const incidentLocation =
  getValue(
    caseData?.location,
    caseData?.incident_location,
    incident.Location,
    incident.location
  )

const complainantName =
  getValue(
    caseData?.victim_name,
    caseData?.complainant_name,
    complainant.Name,
    complainant.name
  )

const complainantPhone =
  getValue(
    caseData?.victim_phone,
    caseData?.complainant_phone,
    complainant.Phone,
    complainant.phone
  )

const accusedName =
  getValue(
    caseData?.accused_name,
    accused.Name,
    accused.name
  )

const crimeType =
  getListValue(
    caseData?.possible_offences,
    caseData?.crime_type,
    incident.offence,
    legalAnalysis?.recommended_sections
  )
  const extractedFields: ExtractedField[] = [
  {
    id: "summary",
    label: "Incident Summary",
    value: incidentSummary,
    icon: FileText,
    confidence: 100,
    isEditing: false
  },

  {
    id: "name",
    label: "Complainant Name",
    value: complainantName,
    icon: User,
    confidence: 100,
    isEditing: false
  },

  {
    id: "fatherName",
    label: "Father / Husband Name",
    value: getValue(
      caseData?.victim_father_name,
      complainant.Father_Name,
      complainant.father_name
    ),
    icon: User,
    confidence: 90,
    isEditing: false
  },

  {
    id: "age",
    label: "Age",
    value: getValue(
      caseData?.victim_age,
      complainant.Age,
      complainant.age
    ),
    icon: User,
    confidence: 90,
    isEditing: false
  },

  {
    id: "gender",
    label: "Gender",
    value: getValue(
      caseData?.victim_gender,
      complainant.Gender,
      complainant.gender
    ),
    icon: User,
    confidence: 90,
    isEditing: false
  },

  {
    id: "address",
    label: "Address",
    value: getValue(
      caseData?.victim_address,
      complainant.Address,
      complainant.address
    ),
    icon: MapPin,
    confidence: 90,
    isEditing: false
  },

  {
    id: "mobile",
    label: "Mobile Number",
    value: complainantPhone,
    icon: Phone,
    confidence: 100,
    isEditing: false
  },

  {
    id: "location",
    label: "Place of Occurrence",
    value: incidentLocation,
    icon: MapPin,
    confidence: 100,
    isEditing: false
  },

  {
    id: "date",
    label: "Occurrence Date",
    value: incidentDate,
    icon: Calendar,
    confidence: 100,
    isEditing: false
  },

  {
    id: "time",
    label: "Occurrence Time",
    value: incidentTime,
    icon: Clock,
    confidence: 100,
    isEditing: false
  },

  {
    id: "suspect",
    label: "Accused Name",
    value: accusedName,
    icon: AlertTriangle,
    confidence: 100,
    isEditing: false
  },

  {
    id: "crimeType",
    label: "Crime Type",
    value:
      crimeType ||
      caseData?.possible_offences?.[0] ||
      "",
    icon: Shield,
    confidence: 100,
    isEditing: false
  },

  {
    id: "propertyType",
    label: "Property Type",
    value: getValue(
      caseData?.property_type,
      caseData?.property?.Type,
      caseData?.property?.type
    ),
    icon: FileText,
    confidence: 90,
    isEditing: false
  },

  {
    id: "propertyValue",
    label: "Property Value",
    value: getValue(
      caseData?.property_value,
      caseData?.property?.Value,
      caseData?.property?.value
    ),
    icon: FileText,
    confidence: 90,
    isEditing: false
  },

  {
    id: "bns",
    label: "Recommended BNS Sections",
    value: getListValue(
      legalAnalysis?.recommended_sections
    ),
    icon: Shield,
    confidence: 95,
    isEditing: false
  }
]

  setFields(
    extractedFields
  )

  setExtractionProgress(
    100
  )

  setIsExtracting(
    false
  )

}, [])

  const toggleEdit = (id: string) => {
    setFields(prev => prev.map(f =>
      f.id === id ? { ...f, isEditing: !f.isEditing } : f
    ))
  }

  const updateFieldValue = (id: string, value: string) => {
    setFields(prev => prev.map(f =>
      f.id === id ? { ...f, value } : f
    ))
  }



  const handleContinue = () => {
    const fieldValue = (id: string) =>
      fields.find(field => field.id === id)?.value || ""

    const dashboardData = JSON.parse(
      localStorage.getItem("firDashboard") || "{}"
    )

    const overview =
      dashboardData?.dashboard?.case_overview || {}

    const complainant =
      overview?.complainant || {}

    const incident =
      overview?.incident || {}

    const property =
      overview?.property || {}

    const cyber =
      overview?.cyber || {}

    const legalAnalysis =
      dashboardData?.dashboard?.legal_analysis || {}

    const originalSections = legalAnalysis?.recommended_sections || []
    const bnsValue = fieldValue("bns")
    const newSections = bnsValue
      ? bnsValue.split(',').map((s: string) => s.trim()).filter(Boolean).map((itemStr: string) => {
          const found = originalSections.find((s: any) => s.title === itemStr || s.section === itemStr)
          if (found) return found
          const numMatch = itemStr.match(/\d+/)
          const sectionNum = numMatch ? numMatch[0] : itemStr
          return {
            section: sectionNum,
            title: itemStr,
            reason: "Manually edited"
          }
        })
      : []

    const updatedLegalAnalysis = {
      ...legalAnalysis,
      recommended_sections: newSections
    }

    const possibleOffences =
      Array.isArray(overview?.possible_offences) && overview.possible_offences.length
        ? overview.possible_offences
        : updatedLegalAnalysis.recommended_sections
          ?.map((section: any) => section.title)
          ?.filter(Boolean) || []

    const caseData = {
      id: dashboardData?.complaint_id || overview?.id,
      incident_summary: fieldValue("summary"),
      victim_name: fieldValue("name"),
      victim_phone: fieldValue("mobile"),
      victim_father_name: getValue(
        overview?.victim_father_name,
        complainant.Father_Name,
        complainant.father_name
      ),
      victim_age: getValue(
        overview?.victim_age,
        complainant.Age,
        complainant.age
      ),
      victim_gender: getValue(
        overview?.victim_gender,
        complainant.Gender,
        complainant.gender
      ),
      victim_address: getValue(
        overview?.victim_address,
        complainant.Address,
        complainant.address
      ),
      location: fieldValue("location"),
      incident_date: fieldValue("date"),
      incident_time: fieldValue("time"),
      accused_name: fieldValue("suspect"),
      crime_type: fieldValue("crimeType"),
      property_type: fieldValue("propertyType"),
      property_value: fieldValue("propertyValue"),
      vehicle_number: getValue(
        overview?.vehicle_number,
        property.Registration_Number,
        property.vehicle_number
      ),
      vehicle_model: getValue(
        overview?.vehicle_model,
        property.Vehicle_Model,
        property.vehicle_model
      ),
      vehicle_color: getValue(
        overview?.vehicle_color,
        property.Vehicle_Color,
        property.vehicle_color
      ),
      bank_name: getValue(
        overview?.bank_name,
        cyber.Bank_Name,
        cyber.bank_name
      ),
      transaction_id: getValue(
        overview?.transaction_id,
        cyber.Transaction_ID,
        cyber.transaction_id
      ),
      amount_lost: getValue(
        overview?.amount_lost,
        cyber.Amount_Lost,
        cyber.amount_lost
      ),
      possible_offences: possibleOffences.length
        ? possibleOffences
        : fieldValue("crimeType")
          ? [fieldValue("crimeType")]
          : [],
      offence: getValue(
        overview?.offence,
        incident.offence
      ),
      legal_analysis: updatedLegalAnalysis
    }

    localStorage.setItem(
      "caseData",
      JSON.stringify(caseData)
    )

    navigate(`/complaint/${caseData.id || 'new'}/evidence`)
  }

  return (
    <div className="space-y-6 max-w-6xl mx-auto">
      {/* Page Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">FIR Information Review</h1>
          <p className="text-muted-foreground mt-1">
            Review extracted FIR fields before generating the final FIR
          </p>
        </div>
        <div className="text-right">
          <p className="text-sm text-muted-foreground">FIR Completeness</p>
          <p className="text-2xl font-bold text-gradient">{extractionProgress}%</p>
        </div>
      </div>

      {/* Extraction Animation */}
      {isExtracting && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="glass-dark rounded-xl p-6 text-center"
        >
          <div className="flex items-center justify-center gap-3 mb-4">
            <Sparkles className="w-8 h-8 text-accent animate-pulse" />
            <span className="text-lg font-medium">AI is extracting information...</span>
          </div>
          <div className="max-w-md mx-auto">
            <Progress value={extractionProgress} className="h-3" />
          </div>
          <p className="text-sm text-muted-foreground mt-3">
            Analyzing complaint text and identifying key details
          </p>
        </motion.div>
      )}

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
              i === 1 ? 'bg-accent text-white' : i < 1 ? 'bg-success text-white' : 'bg-secondary text-muted-foreground'
            )}>
              {i < 1 ? <CheckCircle2 className="w-4 h-4" /> : i + 1}
            </div>
            <span className={cn(
              'text-sm hidden sm:block',
              i === 1 ? 'text-foreground' : 'text-muted-foreground'
            )}>
              {step}
            </span>
            {i < 4 && (
              <ArrowRight className="w-4 h-4 text-muted-foreground hidden sm:block" />
            )}
          </div>
        ))}
      </div>
<div className="space-y-6">

  {/* COMPLAINANT DETAILS */}
  <Card className="bg-card/50 backdrop-blur border-white/10">
    <CardContent className="p-6">
      <h2 className="text-xl font-bold mb-4 text-accent">
        Complainant Details
      </h2>

      <div className="grid md:grid-cols-2 gap-4">
        {fields
          .filter(field =>
            [
              "name",
              "fatherName",
              "age",
              "gender",
              "mobile",
              "address"
            ].includes(field.id)
          )
          .map(field => (
            <div key={field.id}>
              <p className="text-xs text-muted-foreground">
                {field.label}
              </p>

              {field.isEditing ? (
  field.id === "gender" ? (
    <Select
      value={field.value}
      onValueChange={(value) =>
        updateFieldValue(field.id, value)
      }
    >
      <SelectTrigger>
        <SelectValue placeholder="Select Gender" />
      </SelectTrigger>

      <SelectContent>
        <SelectItem value="Male">Male</SelectItem>
        <SelectItem value="Female">Female</SelectItem>
        <SelectItem value="Other">Other</SelectItem>
      </SelectContent>
    </Select>
  ) : (
    <Input
      value={field.value}
      onChange={(e) =>
        updateFieldValue(
          field.id,
          e.target.value
        )
      }
    />
  )
) : (
  <div>
    <p className="font-medium">
      {field.value || "Not Available"}
    </p>

    <Button
      variant="ghost"
      size="sm"
      onClick={() =>
        toggleEdit(field.id)
      }
      className="mt-1 p-0 h-auto"
    >
      Edit
    </Button>
  </div>
)}
            </div>
          ))}
      </div>
    </CardContent>
  </Card>

  {/* INCIDENT DETAILS */}
  <Card className="bg-card/50 backdrop-blur border-white/10">
    <CardContent className="p-6">
      <h2 className="text-xl font-bold mb-4 text-accent">
        Incident Details
      </h2>

      <div className="grid md:grid-cols-2 gap-4">
        {fields
          .filter(field =>
            [
              "summary",
              "location",
              "date",
              "time",
              "crimeType"
            ].includes(field.id)
          )
          .map(field => (
            <div key={field.id}>
              <p className="text-xs text-muted-foreground">
                {field.label}
              </p>

              <p className="font-medium">
                {field.value || "Not Available"}
              </p>
            </div>
          ))}
      </div>
    </CardContent>
  </Card>

  {/* ACCUSED DETAILS */}
  <Card className="bg-card/50 backdrop-blur border-white/10">
    <CardContent className="p-6">
      <h2 className="text-xl font-bold mb-4 text-accent">
        Accused Details
      </h2>

      {fields
        .filter(field =>
          ["suspect"].includes(field.id)
        )
        .map(field => (
          <div key={field.id}>
            <p className="text-xs text-muted-foreground">
              {field.label}
            </p>

            {field.isEditing ? (
              <Input
                value={field.value}
                onChange={(e) =>
                  updateFieldValue(
                    field.id,
                    e.target.value
                  )
                }
              />
            ) : (
              <div>
                <p className="font-medium">
                  {field.value || "Unknown"}
                </p>

                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() =>
                    toggleEdit(field.id)
                  }
                  className="mt-1 p-0 h-auto"
                >
                  Edit
                </Button>
              </div>
            )}
          </div>
        ))}
    </CardContent>
  </Card>

  {/* PROPERTY DETAILS */}
  <Card className="bg-card/50 backdrop-blur border-white/10">
    <CardContent className="p-6">
      <h2 className="text-xl font-bold mb-4 text-accent">
        Property Details
      </h2>

      <div className="grid md:grid-cols-2 gap-4">
        {fields
          .filter(field =>
            [
              "propertyType",
              "propertyValue"
            ].includes(field.id)
          )
          .map(field => (
            <div key={field.id}>
              <p className="text-xs text-muted-foreground">
                {field.label}
              </p>

              {field.isEditing ? (
                <Input
                  value={field.value}
                  onChange={(e) =>
                    updateFieldValue(
                      field.id,
                      e.target.value
                    )
                  }
                />
              ) : (
                <div>
                  <p className="font-medium">
                    {field.value || "Not Available"}
                  </p>

                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() =>
                      toggleEdit(field.id)
                    }
                    className="mt-1 p-0 h-auto"
                  >
                    Edit
                  </Button>
                </div>
              )}
            </div>
          ))}
      </div>
    </CardContent>
  </Card>

  {/* LEGAL ANALYSIS */}
  <Card className="bg-card/50 backdrop-blur border-white/10">
    <CardContent className="p-6">
      <h2 className="text-xl font-bold mb-4 text-accent">
        Legal Analysis
      </h2>

      {fields
        .filter(field =>
          ["bns"].includes(field.id)
        )
        .map(field => (
          <div key={field.id}>
            <p className="text-xs text-muted-foreground">
              {field.label}
            </p>

            {field.isEditing ? (
              <Input
                value={field.value}
                onChange={(e) =>
                  updateFieldValue(
                    field.id,
                    e.target.value
                  )
                }
              />
            ) : (
              <div>
                <p className="font-medium">
                  {field.value || "Not Available"}
                </p>

                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() =>
                    toggleEdit(field.id)
                  }
                  className="mt-1 p-0 h-auto"
                >
                  Edit
                </Button>
              </div>
            )}
          </div>
        ))}
    </CardContent>
  </Card>

</div>

      {/* Action Buttons */}
      <div className="flex justify-between items-center pt-4">
        <Link to="/complaint/new">
          <Button variant="outline">
            Back
          </Button>
        </Link>
        <Button
          size="lg"
          onClick={handleContinue}
          disabled={isExtracting}
          className="min-w-[200px]"
        >
          Continue
          <ArrowRight className="w-5 h-5 ml-2" />
        </Button>
      </div>
    </div>
  )
}
