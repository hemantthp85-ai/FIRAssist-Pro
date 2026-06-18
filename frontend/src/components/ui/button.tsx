import * as React from "react"
import { Slot } from "@radix-ui/react-slot"
import { cva, type VariantProps } from "class-variance-authority"
import { cn } from "@/lib/utils"

const buttonVariants = cva(
  "inline-flex items-center justify-center whitespace-nowrap rounded-lg text-sm font-medium transition-all duration-200 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50",
  {
    variants: {
      variant: {
        default:
          "bg-accent text-white shadow-lg shadow-accent/25 hover:bg-accent/90 hover:shadow-accent/40 active:scale-[0.98]",
        destructive:
          "bg-danger text-white shadow-lg shadow-danger/25 hover:bg-danger/90 active:scale-[0.98]",
        outline:
          "border-2 border-accent/50 text-accent hover:bg-accent/10 hover:border-accent",
        secondary:
          "bg-secondary text-foreground shadow-lg hover:bg-secondary/80 active:scale-[0.98]",
        ghost:
          "text-foreground hover:bg-white/5 hover:text-accent",
        link: "text-accent underline-offset-4 hover:underline",
        success:
          "bg-success text-white shadow-lg shadow-success/25 hover:bg-success/90 active:scale-[0.98]",
      },
      size: {
        default: "h-10 px-4 py-2",
        sm: "h-8 rounded-md px-3 text-xs",
        lg: "h-12 rounded-lg px-8 text-base",
        xl: "h-14 rounded-xl px-10 text-lg",
        icon: "h-10 w-10",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  }
)

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  asChild?: boolean
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, asChild = false, ...props }, ref) => {
    const Comp = asChild ? Slot : "button"
    return (
      <Comp
        className={cn(buttonVariants({ variant, size, className }))}
        ref={ref}
        {...props}
      />
    )
  }
)
Button.displayName = "Button"

export { Button, buttonVariants }
