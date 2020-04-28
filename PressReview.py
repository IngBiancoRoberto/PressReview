import tkinter
from tkinter import messagebox
import os
import numpy as np
import backend

class PressReview:

    def __init__(self):
        # start backend
        self.be = backend.Backend()
        # make layout
        self.make_layout()
        # initialise empty selection
        self.selected_rows = []
        self.selected_date = []
        # populate date list from database
        self.populate_dates()
        # select first line
        self.dates_list.select_set(0)
        # show articles
        self.date_select([])
        #
        self.update_narticles_label()

        #
        # start app
        self.app.mainloop()



    def make_layout(self):
        
        # create window
        self.app =tkinter.Tk()
        self.app.configure(bg='white')
        self.app.title('Press Review')
        self.app.geometry('1200x500+200+100')

        # update button
        self.update_button_string = tkinter.StringVar()
        self.update_button_string.set('Update Articles')
        self.update_button = tkinter.Button(self.app, textvariable = self.update_button_string,
        command=self.update_articles)
        self.update_button.grid(row=0, column=0,columnspan=2, padx=10,pady=10)

        # label with number of articles
        self.narticles_label_string = tkinter.StringVar()
        self.narticles_label = tkinter.Label(self.app,text='Test label',textvariable = self.narticles_label_string,
        font=('bold',12),bg='white')
        self.narticles_label.grid(row=0,column=2,columnspan=2, pady=10)

        ## DATES LIST (listbox)
        self.dates_list = tkinter.Listbox(self.app,height=8,width=22,font=('bold',10),border=2,highlightcolor='blue',selectmode='SINGLE')
        self.dates_list.grid(row=1,column = 0, padx=10,pady=10)
        # dates scrollbar
        self.dates_scrollbar = tkinter.Scrollbar(self.app)
        self.dates_scrollbar.grid(row=1,column=1)
        # fix dates scrollbar
        self.dates_list.configure(yscrollcommand=self.dates_scrollbar.set)
        self.dates_scrollbar.configure(command=self.dates_list.yview)
        self.dates_list.bind('<<ListboxSelect>>',self.date_select)
        self.dates_list.bind('<Button-3>',self.date_delete)

        # ARTICLE LIST (Listbox)
        #self.article_frame = tkinter.Frame(self.app,bg='white',width=500,height=500,relief='sunken')
        #self.article_frame.grid(row=1,column=2,padx=10,pady=10,sticky='N')
        self.articles_list = tkinter.Listbox(self.app,height=22,width=120,border=2,font=('bold',11),highlightcolor='blue',selectmode='SINGLE')
        self.articles_list.grid(row=1,column = 3, padx=10,pady=10)
        # articles scrollbar
        self.articles_scrollbar = tkinter.Scrollbar(self.app)
        self.articles_scrollbar.grid(row=1,column=4)
        # fix articles scrollbar
        self.articles_list.configure(yscrollcommand=self.articles_scrollbar.set)
        self.articles_scrollbar.configure(command=self.articles_list.yview)
        self.articles_list.bind('<Double-Button-1>',self.article_select)

        # MENU
        menubar = tkinter.Menu(self.app)
        # data menu
        data_menu = tkinter.Menu(menubar, tearoff=0)
        data_menu.add_command(label='Delete all data...', command=self.delete_all)
        data_menu.add_separator()
        data_menu.add_command(label='Exit',command=self.app.quit)
        # add to menubar
        menubar.add_cascade(label='Data',menu=data_menu)

        # help menu
        help_menu = tkinter.Menu(menubar,tearoff=0)
        help_menu.add_command(label='About',command=self.about)
        menubar.add_cascade(label='Help',menu=help_menu)
        # add to app
        self.app.config(menu=menubar)

    def delete_all(self):
        if len(self.selected_rows)==0:
            tkinter.messagebox.showwarning('Delete data','No data to delete!')
            return

        answer = tkinter.messagebox.askyesno('Delete all data',
        'Are you sure you want to delete all data?',
        default=messagebox.NO)

        if answer==False:
            return
        
        # remove items in db
        self.be.db.removeAll()
        # set selection to empty
        self.selected_date = []
        self.selected_rows = []
        # update graphics
        self.populate_dates()
        self.update_narticles_label()
        # clear articles listbox
        self.articles_list.delete(0,'end')

    def about(self):
        tkinter.messagebox.showinfo('About','Press Review - R. Bianco Apr 2020')


    def update_narticles_label(self):
        if len(self.selected_rows) ==0:
            self.narticles_label_string.set('')
        else:
            self.narticles_label_string.set('{:d} articles found'.format(len(self.selected_rows)))
    
    def update_articles(self):
        # callback to button press

        # change text in button to checking
        self.update_button_string.set('Checking...')
        
        #
        status = self.be.update_db()

        if status == 'no_data':
            messagebox.showwarning('No data','No data')
        elif status == 'same_data':
            messagebox.showwarning('No data change','The articles have not changed since last check')
        else: # if data have changed
            # update list of dates
            self.populate_dates()
            # select first date
            self.dates_list.select_set(0)
            # show last articles
            self.date_select([])

        #revert button string
        self.update_button_string.set('Update articles')
      
    def populate_dates(self):
        "ADDS DATES TO Listbox"
        dates_values = self.be.db.readUniqueTimes()
        # clear list first
        self.dates_list.delete(0, 'end')
        # add values
        for date_value in dates_values:
            self.dates_list.insert('end', date_value)
        

    def date_select(self, event):
        # get chosen date
        curselect = self.dates_list.curselection()
        if len(curselect)==0:
            return

        self.selected_date = self.dates_list.get( curselect[0] ) 
        # find corresponding rows in database
        self.selected_rows = self.be.db.readByTime(self.selected_date)
        # clean up article listbox
        self.articles_list.delete(0, 'end')
        # populate listbox
        for row in self.selected_rows:
            #self.articles_list.insert('end','['+row[2]+']')
            #self.articles_list.insert('end',row[3])
            self.articles_list.insert('end','')
            self.articles_list.insert('end','['+row[2]+'] '+row[3])       
        # update number of articles label
        self.update_narticles_label()

    def date_delete(self,event):
        # clear selection
        self.dates_list.selection_clear(0,tkinter.END)
        # set selection on clicked item
        self.dates_list.selection_set(self.dates_list.nearest(event.y))
        self.dates_list.activate(self.dates_list.nearest(event.y))
        # show articles
        self.date_select([])
        # question
        answer = messagebox.askyesno('Delete item','Do you want to delete all articles for the selected date?',
        default=messagebox.NO)
        # if false return
        if answer==False:
            return
        
        # get chosen date
        curselect = self.dates_list.curselection()
        if len(curselect)==0:
            return
        #
        self.selected_date = self.dates_list.get( curselect[0] ) 
        # delete records by date
        self.be.db.removeByTime(self.selected_date)
        # update dates list
        self.populate_dates()
        # select date before
        new_curselect = max(0,curselect[0]-1)
        self.dates_list.selection_set( new_curselect )
        # show articles as if selecting date
        self.date_select([])
  
    def article_select(self,event):
        # selected cursor
        curselect = self.articles_list.curselection() # tuple
        if len(curselect)==0 or np.mod(curselect[0],2)==0:
            return
        actual_select = int((curselect[0]-1)/2)
        os.startfile( self.selected_rows[actual_select][4] )
        

PressReview()



