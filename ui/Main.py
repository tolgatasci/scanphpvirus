from tkinter import Tk, Frame, BOTH

from tkinter import ttk, filedialog
import tkinter as tk
from helper.Global import *
from models.Arg import Arg


class Main(Tk):
    row_list = {}
    wordpress = False
    data = []

    def __init__(self, *arg, **kwargs):
        super().__init__()
        self.form()

    def form(self):
        self.title("Scan PHP files")
        self.geometry('600x800+800+100')
        self.w, self.h = self.winfo_screenwidth(), self.winfo_screenheight()
        self.resizable(False, False)
        self.configure(background="white")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=0)
        center_container = Frame(self, bg='brown')
        center_container.grid(row=0, column=0)

        ttk.Button(center_container, text="Select Directory", width=25, command=self.directory_select).grid(row=0,
                                                                                                            column=0,
                                                                                                            pady=10,
                                                                                                            padx=20)
        ttk.Button(center_container, text="Selet Zip File", width=25, command=self.zip_select).grid(row=0, column=1,
                                                                                                    pady=10,
                                                                                                    padx=20)
        self.wordpress = tk.IntVar()
        c2 = tk.Checkbutton(center_container, text='Wordpress', variable=self.wordpress, onvalue=1, offvalue=0)
        c2.grid(row=0, column=2, pady=10, padx=20)

        info_frame = Frame(self, bg='white')
        info_frame.grid(row=1, column=0, pady=10, padx=20, sticky='nsew')
        self.total_search = tk.Label(info_frame, text="Total Searched Files : 0", bg='White', fg='black')
        self.total_found = tk.Label(info_frame, text="Total Found danger  : 0", bg='White', fg='black')
        self.total_search.grid(row=0, column=0, pady=10, padx=20)
        self.total_found.grid(row=0, column=1, pady=10, padx=20)
        columns = ('code', 'line', 'file', '_id')

        self.tree = ttk.Treeview(self, columns=columns, show='headings', height=28,
                                 padding=(2, 2, 2, 2),
                                 selectmode="extended")
        self.tree.grid(row=2, column=0, pady=10, padx=20, sticky='nsew')
        # define headings
        self.tree.heading('code', text='Code')
        self.tree.heading('line', text='line')
        self.tree.heading('file', text='File', anchor='se')
        self.tree.heading('_id', text='_id')

        self.tree.column('code', width=300)
        self.tree.column('line', width=50)
        self.tree.column('file', width=75)

        self.tree.column('_id', width=0)

        self.tree["displaycolumns"] = ('code', 'line', 'file')
        self.code_info = None
        self.tree.bind('<<TreeviewSelect>>', self.item_selected)

        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)

        scrollbar.grid(row=2, column=1, sticky='ns')

    def item_selected(self, event):

        for selected_item in self.tree.selection():
            item = self.tree.item(selected_item)
            record = item['values']
            data_check = record[3]
            if data_check != "":
                if self.row_list.get(data_check) == None:
                    return False
            if self.code_info != None:
                self.code_info.destroy()

            get_data = self.row_list.get(data_check)

            self.code_info = tk.Toplevel(self)
            self.code_info.title(get_data[1].name)
            self.code_info.geometry("900x800+800+100")

            TextArea = tk.Text(self.code_info, font="ubuntu 12")

            TextArea.pack(expand=True, fill=BOTH)

            TextArea.insert(1.0, get_data[1].content)

            TextArea.focus()

            TextArea.mark_set("insert", "%d.%d" % (get_data[0].line, 0))

            TextArea.tag_configure("red", foreground="red")

            TextArea.tag_add("red", "{}.0".format(get_data[0].line), "{}.0 lineend".format(get_data[0].line))
            TextArea.see('{}.0'.format((int(get_data[0].line) - (1 if int(get_data[0].line) < 10 else 10))))
            TextArea.config(state="disabled")
            tk.Label(self.code_info,
                     text=get_data[2].name + "/" + get_data[1].name).pack()

    def zip_select(self):
        self.tree.delete(*self.tree.get_children())
        file = filedialog.askopenfilename(filetypes=[("Zip File", "*.zip")], title="Select a zip file")

        self.data = zip_run(Arg(zip=file, wordpress=True if self.wordpress.get() == 1 else False), self.data)
        self.run()

    def directory_select(self):
        self.tree.delete(*self.tree.get_children())
        folder = filedialog.askdirectory()
        self.data = directory_run(Arg(directory=folder, wordpress=True if self.wordpress.get() == 1 else False),
                                  self.data)
        self.run()

    def run(self):
        total_files = 0
        found_danger = 0
        index = 0
        for item in self.data.directory:

            for file_ in item.files:
                total_files += 1
                if file_.results:
                    found_danger += 1
                    print(Fore.GREEN + "File: " + Style.RESET_ALL + item.name + "/" + file_.name)

                    for rulex in file_.results:
                        self.row_list[index] = [rulex, file_, item]

                        self.tree.insert('', tk.END, values=(rulex.found, rulex.line, file_.name, index))
                        index += 1
                        print(
                            Fore.RED + "Rule: " + Style.RESET_ALL + rulex.name + Fore.RED + " found: " + Style.RESET_ALL + rulex.found + Fore.RED + " on line: " + Style.RESET_ALL + str(
                                rulex.line))
        print(Fore.GREEN + "Total files: " + Style.RESET_ALL + str(total_files))
        print(Fore.RED + "Total found risk: " + Style.RESET_ALL + str(found_danger))
        self.total_search.config(text='Total Searched Files : {}'.format(total_files))
        self.total_found.config(text='Total found files : {}'.format(found_danger))
