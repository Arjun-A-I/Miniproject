
# Import Module  
import tabula 
  
# Read PDF File 
# this contain a list 
df = tabula.read_pdf(r"C:\Users\arjun\Code\miniproj\Miniproject\ktu_calender.pdf", pages = 1)[0] 
  
# Convert into Excel File 
df.to_excel('./ktu_calender.xlsx', index = False) 