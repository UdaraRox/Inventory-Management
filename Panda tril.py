
import pandas as pd


name_01=input("Input name 1")
name_02=input("Input name 2")
name_03=input("Input name 3")
#name_04=input("Input name 4")




# Create the data
data = {
    "Student name": [name_01,name_02,name_03],
    "Student age": [10, 12, 10],
    "Student ID": ["001", "002", "003"]
}
#bhagyai

# Create DataFrame
df = pd.DataFrame(data)

# Display the table
print(df)
