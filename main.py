import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from pypdf import PdfWriter
import os


class PDFMergerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Merger")
        self.root.geometry("600x500")
        self.root.configure(bg="#f0f0f0")
        
        self.pdf_list = []
        
        # Title
        title_label = tk.Label(
            root, 
            text="PDF Merger Tool", 
            font=("Arial", 16, "bold"),
            bg="#f0f0f0"
        )
        title_label.pack(pady=10)
        
        # Frame for buttons
        button_frame = tk.Frame(root, bg="#f0f0f0")
        button_frame.pack(pady=10)
        
        # Add PDF button
        add_btn = tk.Button(
            button_frame,
            text="Add PDF Files",
            command=self.add_pdfs,
            bg="#4CAF50",
            fg="white",
            padx=10,
            pady=5,
            font=("Arial", 10)
        )
        add_btn.pack(side=tk.LEFT, padx=5)
        
        # Clear button
        clear_btn = tk.Button(
            button_frame,
            text="Clear List",
            command=self.clear_list,
            bg="#FF9800",
            fg="white",
            padx=10,
            pady=5,
            font=("Arial", 10)
        )
        clear_btn.pack(side=tk.LEFT, padx=5)
        
        # File list display
        list_label = tk.Label(root, text="PDF Files to Merge:", font=("Arial", 10, "bold"), bg="#f0f0f0")
        list_label.pack(anchor="w", padx=20, pady=(10, 5))
        
        self.file_listbox = scrolledtext.ScrolledText(
            root,
            height=8,
            width=70,
            state=tk.DISABLED,
            font=("Arial", 9)
        )
        self.file_listbox.pack(padx=20, pady=5)
        
        # Output filename
        output_frame = tk.Frame(root, bg="#f0f0f0")
        output_frame.pack(pady=10, padx=20, fill=tk.X)
        
        output_label = tk.Label(output_frame, text="Output Filename:", font=("Arial", 10), bg="#f0f0f0")
        output_label.pack(side=tk.LEFT)
        
        self.output_entry = tk.Entry(output_frame, font=("Arial", 10))
        self.output_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 0))
        self.output_entry.insert(0, "merged.pdf")
        
        # Merge button
        merge_btn = tk.Button(
            root,
            text="Merge PDFs",
            command=self.merge_pdfs,
            bg="#2196F3",
            fg="white",
            padx=20,
            pady=10,
            font=("Arial", 11, "bold")
        )
        merge_btn.pack(pady=15)
        
        # Status label
        self.status_label = tk.Label(
            root,
            text="Ready",
            font=("Arial", 10),
            fg="green",
            bg="#f0f0f0"
        )
        self.status_label.pack(pady=10)
    
    def add_pdfs(self):
        files = filedialog.askopenfilenames(
            title="Select PDF files",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        if files:
            self.pdf_list.extend(files)
            self.update_file_display()
            self.update_status(f"Added {len(files)} file(s). Total: {len(self.pdf_list)}", "blue")
    
    def clear_list(self):
        self.pdf_list = []
        self.update_file_display()
        self.update_status("List cleared", "orange")
    
    def update_file_display(self):
        self.file_listbox.config(state=tk.NORMAL)
        self.file_listbox.delete(1.0, tk.END)
        for i, pdf in enumerate(self.pdf_list, 1):
            self.file_listbox.insert(tk.END, f"{i}. {os.path.basename(pdf)}\n")
        self.file_listbox.config(state=tk.DISABLED)
    
    def merge_pdfs(self):
        if not self.pdf_list:
            messagebox.showwarning("Warning", "Please add PDF files first")
            return
        
        output_filename = self.output_entry.get().strip()
        if not output_filename:
            messagebox.showwarning("Warning", "Please enter an output filename")
            return
        
        try:
            self.update_status("Merging PDFs...", "blue")
            self.root.update()
            
            merger = PdfWriter()
            for pdf in self.pdf_list:
                merger.append(pdf)
            
            merger.write(output_filename)
            
            self.update_status(f"✓ Successfully merged to {output_filename}", "green")
            messagebox.showinfo("Success", f"PDFs merged successfully!\nOutput: {output_filename}")
            
        except Exception as e:
            self.update_status(f"✗ Error: {str(e)}", "red")
            messagebox.showerror("Error", f"Failed to merge PDFs:\n{str(e)}")
    
    def update_status(self, message, color="black"):
        self.status_label.config(text=message, fg=color)


if __name__ == "__main__":
    root = tk.Tk()
    app = PDFMergerGUI(root)
    root.mainloop()