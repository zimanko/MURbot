import tkinter as TK
import tkinter.messagebox as TK_MSG

title_font = ('Helvetica', 18, 'normal')
button_font = ('Helvetica', 10, 'normal')
button_config = {'fg' : 'grey',
                 'bg' : 'white',
                 'font' : button_font,
                 'height' : 2,
                 'width' : 12,
                 'relief' : 'raised',
                 'activebackground' : 'white',
                 'activeforeground' : 'green',
                 'bd' : 1}

def callback():
    if TK_MSG.askyesno('Verify', 'Really Quit?'):
        TK_MSG.showwarning('Yes', 'not yet')
    else:
        TK_MSG.showinfo('No', 'Quit cancelled')


root = TK.Tk()

main_wnd = TK.Frame(root)
main_wnd.pack(expand=1, fill='both')

TK.Label(main_wnd,
         text='MURbot',
         bg='white',
         fg='grey',
         font=title_font).pack(expand=1, fill='both', side='left', padx=20)

TK.Button(main_wnd,
          text='Setup',
          **button_config,
          command=callback).pack(expand=1, fill='both', side='top', anchor='e', padx=5, pady=3)

TK.Button(main_wnd,
          text='Start',
          **button_config).pack(expand=1, fill='both', side='top', anchor='e', padx=5, pady=3)

TK.Button(main_wnd,
          text='Stop',
          **button_config).pack(expand=1, fill='both', side='top', anchor='e', padx=5, pady=3)

root.title('MURbot')
root.mainloop()
