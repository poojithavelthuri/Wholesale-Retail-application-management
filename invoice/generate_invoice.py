#BIS698W1700_Group03_Wholesale/Retail application management
#Importing necessary libraries and functions
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from database.order_model import fetch_order_details

def generate_invoice(order_id):
    order_details = fetch_order_details(order_id)
    if order_details:
        order_id, customer_name, product_name, quantity, total_price, order_date = order_details

        # Create a PDF invoice
        file_name = f"Invoice_{order_id}_{customer_name.replace(' ', '_')}.pdf"
        pdf = canvas.Canvas(file_name, pagesize=letter)

        # Add title to the invoice
        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(200, 750, "Invoice")

        # Order information
        pdf.setFont("Helvetica", 12)
        pdf.drawString(50, 700, f"Order ID: {order_id}")
        pdf.drawString(50, 680, f"Order Date: {order_date}")
        pdf.drawString(50, 660, f"Customer Name: {customer_name}")
        pdf.drawString(50, 640, f"Product: {product_name}")
        pdf.drawString(50, 620, f"Quantity: {quantity}")
        pdf.drawString(50, 600, f"Total Price: ${total_price:.2f}")

        # Save the PDF
        pdf.save()
        print(f"Invoice saved as {file_name}")
    else:
        print("Order details not found.")
