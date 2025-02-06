import fitz  # Import PyMuPDF (alias 'fitz')


# Open a PDF document

doc = fitz.open(input("PDF Location: "))

page = doc[0]  # Access the first page



# Define rectangle coordinates

topLeftX = input("TopLeftX: ")
topLeftY = input("TopLeftY: ")
bottomRightX = input("BottomRightX: ")
bottomRightY = input("BottomRightY: ")
rect = fitz.Rect(topLeftX, topLeftY, bottomRightX, bottomRightY)  # Top-left (100, 100), bottom-right (200, 200)



# Create a new shape and draw the rectangle

shape = page.new_shape()

shape.draw_rect(rect) 

page.draw_rect(rect, color=fitz.utils.getColor('pink'))

# Save the modified PDF

doc.save("modified_pdf.pdf")

