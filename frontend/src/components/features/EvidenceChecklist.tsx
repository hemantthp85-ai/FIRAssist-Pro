import { FileText, Check } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'

interface EvidenceChecklistProps {
  documents: string[]
  uploadedFiles: any[]
  onUploadClick: (docName: string) => void
  onVerifyToggle: (docName: string, currentStatus: string) => void
}

export default function EvidenceChecklist({
  documents,
  uploadedFiles,
  onUploadClick,
  onVerifyToggle
}: EvidenceChecklistProps) {
  
  const getDocumentStatus = (docName: string) => {
    const file = uploadedFiles.find(f => f.doc_name === docName)
    if (!file) return { label: 'Pending', variant: 'secondary' as const, file: null }
    if (file.status === 'Verified') return { label: 'Verified', variant: 'default' as const, file }
    return { label: 'Uploaded', variant: 'outline' as const, file }
  }

  return (
    <div className="space-y-3">
      {documents.map((docName) => {
        const { label, variant, file } = getDocumentStatus(docName)
        const isUploaded = !!file
        const isVerified = file?.status === 'Verified'

        return (
          <div
            key={docName}
            className="flex flex-col sm:flex-row items-start sm:items-center justify-between p-4 rounded-xl border border-white/5 bg-secondary/15 hover:bg-secondary/20 transition-all gap-4"
          >
            <div className="flex items-center gap-3">
              <div className={`w-8 h-8 rounded-lg flex items-center justify-center ${
                isVerified ? 'bg-success/20 text-success' : isUploaded ? 'bg-accent/20 text-accent' : 'bg-white/5 text-muted-foreground'
              }`}>
                <FileText className="w-4 h-4" />
              </div>
              <div>
                <p className="text-sm font-medium leading-none">{docName}</p>
                {file && (
                  <p className="text-[11px] text-muted-foreground mt-1.5 truncate max-w-[200px] sm:max-w-xs">
                    File: {file.filename}
                  </p>
                )}
              </div>
            </div>

            <div className="flex items-center gap-3 w-full sm:w-auto justify-between sm:justify-end">
              <Badge
                variant={variant}
                className={
                  isVerified
                    ? 'bg-success/20 text-success border-success/30'
                    : isUploaded
                    ? 'bg-accent/20 text-accent border-accent/30'
                    : 'bg-white/5 text-muted-foreground border-white/10'
                }
              >
                {label}
              </Badge>

              <div className="flex items-center gap-2">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => onUploadClick(docName)}
                  className="h-8 text-xs"
                >
                  {isUploaded ? 'Re-upload' : 'Upload'}
                </Button>

                {isUploaded && (
                  <Button
                    variant={isVerified ? 'default' : 'outline'}
                    size="sm"
                    onClick={() => onVerifyToggle(docName, file.status)}
                    className={`h-8 w-8 p-0 flex items-center justify-center ${
                      isVerified
                        ? 'bg-success text-white hover:bg-success/80'
                        : 'border-white/10 text-muted-foreground hover:text-foreground'
                    }`}
                    title={isVerified ? 'Mark as Unverified' : 'Mark as Verified'}
                  >
                    <Check className="w-4 h-4" />
                  </Button>
                )}
              </div>
            </div>
          </div>
        )
      })}
    </div>
  )
}
