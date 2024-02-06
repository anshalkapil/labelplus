import tkinter as tk
from tkinter import filedialog
import pandas as pd

pd.options.display.max_colwidth = 10000

# Create and run the application
root = tk.Tk()
root.geometry("400x400")
root.title("LabelPlus")

def num_labels(df):
    upload_button.destroy()
    num_text = tk.Label(root, text="Enter the Number of Distinct Labels:")
    num_text.pack()
    num_input =tk.Scale(root, from_=0, to=10, orient="horizontal")
    
    num_input.pack()

    def label_names(df,num_submit):
        num_of_labels = num_input.get()
        num_text.destroy()
        num_input.destroy()
        num_submit.destroy()
        frame = tk.Frame(root, padx=20, pady=20)
        key_header = tk.Label(frame, text="Keyboard Shortcut")
        label_header = tk.Label(frame, text="Label Name")
        key_header.grid(row=0,column=0)
        label_header.grid(row=0,column=1)
        label_list =[]
        key_list =[]
        keys = ['a','s','d','f','g','h','j','k','l','p']
        for i in range(num_of_labels):
            key_list.append(tk.Label(frame, text=keys[i]))
            label_list.append(tk.Entry(frame))
            key_list[i].grid(row=i+1, column=0)
            label_list[i].grid(row=i+1, column=1) 
        label_rows = tk.Label(frame,text="Start from index:")
        starting_entry =tk.Entry(frame)
        label_rows.grid(row=i+2,column=0)
        starting_entry.grid(row=i+2,column=1) 
        frame.grid(row=0, column=0, sticky="n")
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)


        
        def labeling():
            labels = dict()
            start = int(starting_entry.get())
            for i in range(num_of_labels):
                labels[keys[i]] = label_list[i].get()
            print(labels)
            frame.destroy()
            
            row_var = tk.StringVar()  
            def finish():
                    df.to_excel('Labelled_database.xlsx', index=False)
            finish_button =tk.Button(root, text="Finish", command=finish)
            finish_button.pack()
            
            for i in range(start, df.shape[0]):
                row_var.set(str(i))  
                row = tk.Text(root, height=5, font=('TkDefaultFont', 10))
                row.insert('end', str(df.loc[i]))
                row.pack()
                
                
                def key_press(event, i=i):
                    key = event.keysym
                    if key in labels:
                        df.loc[i, "Label"] = labels[key]
                    row_var.set(str(i+1))  
                    row.destroy()
                    
                    
                
                root.bind("<Key>", key_press)
                root.wait_variable(row_var)  #
        
            

            

        label_submit = tk.Button(frame, text= "Submit", command=labeling)
        label_submit.grid(row=i+3,column=1)


        



    num_submit = tk.Button(root, text= "Submit", command=lambda:label_names(df,num_submit))
    num_submit.pack()

def upload_excel():
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    df = pd.read_csv(file_path)
    if "Label" not in df:
        df["Label"] = None
    print(df.head())
    num_labels(df)


upload_button = tk.Button(root, text="Upload CSV File", command=upload_excel)
upload_button.pack()

root.mainloop()