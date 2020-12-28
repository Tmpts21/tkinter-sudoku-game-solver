import random
import numpy 
import tkinter as tk
from tkinter import *
from tkinter import messagebox



#sudoku class
class sudoku :
    
    def __init__ (self) :
        
        self.board = []
        
        self.results = []
        
        
    def generate_new_board(self) :
        ''' generate a random board from a solved board . '''
        original_board =[[7,8,5,4,3,9,1,2,6],
                    [6,1,2,8,7,5,3,4,9],
                    [4,9,3,6,2,1,5,7,8],
                    [8,5,7,9,4,3,2,6,1],
                    [2,6,1,7,5,8,9,3,4],
                    [9,3,4,1,6,2,7,8,5],
                    [5,7,8,3,9,4,6,1,2],
                    [1,2,6,5,8,7,4,9,3],
                    [3,4,9,2,1,6,8,5,7]]
        
        ''' generate a new board \n explanation : the first set of loops will randomly select a number in the original board and
            make it 0 the 2nd set of loop will select a random increment and increment those remaining numbers that is not 0 by the random in
            crement value if the increment is greater than 9 we apply these formula (a-b) - 9 '''
        test = original_board
        random_increment = random.randint(0,8)
        index = 0
        for i in range(len(test)) :
            for j in range (3,len(test[i])-1) :
                index = random.randint(0 , len(test[i])-1 )
                test[i][index] = 0
        for x in range (len(test)) :
            for y in range (len(test[x])) :
                if test[x][y] != 0 :
                    if test[x][y] + random_increment > 9 :
                        test[x][y] = (test[x][y] + random_increment)-9
                    else :
                        test[x][y]+= random_increment
                        
        self.board = test
        
        return self.board
    
    def print_board(self) :
        ''' print the board in the console''' 
        counter = 0
        print('   ' , end = '')
        print('a','b','c','d','e','f','g','h','i')
        for i in numpy.array(self.board) :
            print(counter , i)
            counter += 1

    #solver
    def checkPossible(self , row,col,n) :
        ''' check horizontal and verticals if its existing in the two return false otherwise true'''
        horizontal = [] 
        vertical= [] 
        for i  in range(9) :
            if self.board[i][col] == n or self.board[row][i] == n:
                return False
        if self.check_subgrid(row , col , n) == False:
            return False 
        return True 
    
    def check_subgrid(self , row , col , n) :
        ''' check the current 3x3 ('subgrid') if the number to be put is existing if so return false otherwise true '''
        subgrid_x = (col // 3 ) * 3
        subgrid_y = (row // 3 ) * 3
        for i in range(0,3) :
            for j in range (0,3) :
                #print(subgrid_y + i ,subgrid_x + j)
                if self.board[subgrid_y + i][subgrid_x + j] == n :
                    return False
        return True

    def satisfied(self) :
        ''' check the board if it is done or filled entirely'''
        for i in self.board :
            if 0 not in i :
                continue
            else:
                return False
        return True 

    def solve(self) :
        ''' function that solves the board using backtracking algorithm '''
        if self.satisfied() :
            self.results.append(numpy.array(self.board))
            return self.results
        else :       
            for i in range (0,9) :
                for j in range (0,9) :
                    if self.board[i][j] == 0  :
                        for x in range (1 , 10) :
                            if self.checkPossible( i , j , x) :
                                self.board[i][j] = x
                                self.solve() 
                                self.board[i][j] = 0
                        return

    
#gui class
                   
class GUI(sudoku):
    def __init__(self):
        self.root = tk.Tk()
        self.sudoku= sudoku()
        #screen size ( full screen)
        w, h = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        self.root.geometry("%dx%d+0+0" % (w, h))
        #coordinates of the button user clicked 
        self.current_coordinates = []
        # sudoku board intialization 
        self.board = self.sudoku.generate_new_board()
        self.sudoku.board = self.board
        #info and entry label
        self.info_label = tk.Label(self.root,font=("Helvetica" ,31,'bold'), text='Sudoku with python',fg= 'blue',relief =RIDGE)
        self.info_label.grid(row=0, column=10)

        self.buttons = []
        self.draw_board()
        self.a = tk.Button(self.root, text= 'Restart Sudoku', font=("Helvetica" ,31,'bold') ,command = lambda: self.random_board() )
        self.a.grid(row=1, column=10, sticky="nsew", padx=1, pady=1)
        self.b = tk.Button(self.root, text= 'Solve Sudoku', font=("Helvetica" ,31,'bold') , command = lambda: self.solve() )
        self.b.grid(row=2, column=10, sticky="nsew", padx=1, pady=1)

        
    def draw_board (self) :
        ''' draw the board '''
        temp = []
        self.buttons = []

        for row in range(9):
            for col in range(9):
                if self.board[row][col] == 0 : 
                    temp.append(tk.Button(self.root, text= self.board[row][col] , bg = 'white',fg='red',font=("Helvetica", 28,'bold') , relief=RIDGE  ,height = 1, width = 3, command=lambda x=row, y=col: self.user_entry(x, y) ))
                else :                        
                    temp.append(tk.Button(self.root, text= self.board[row][col],font=("Helvetica" ,28,'bold') , bg ='white' ,relief=RIDGE , height = 1, width = 3, command=lambda x=row, y=col: self.user_entry(x, y) ))
                         
            self.buttons.append(temp)
            temp = []
        for i in range(len(self.buttons)) :
            for j in range(len(self.buttons[i])) :
                self.buttons[i][j].grid(row=i, column=j, sticky="nsew", padx=2, pady=2)

     
        
    def solve(self) :
        '''Solve the current board using the method solve() in the sudoku class'''
        self.sudoku.solve()
        self.board = self.sudoku.results[-1]
        self.draw_board()
        self.game_finished()

        

    def random_board(self) :
        '''Generate a random board using the generate_new_board() method from the sudoku class and redraw the board'''
        self.board = self.sudoku.generate_new_board()
        self.draw_board()
        return self.board
    def user_entry(self , row , col ) :
        '''After the user clicked the a button it will show an entry to user and user will type the value he want to add to the board'''
        if len(self.current_coordinates) > 0 :
            self.buttons[self.current_coordinates[0]][self.current_coordinates[1]].configure(bg='white', fg='black')
        self.buttons[row][col].configure(bg='black', fg = 'white')
        ''' label for the entry '''
        self.entry_label = tk.Label(self.root,font=("Helvetica" ,31,'bold'),text='Enter Value',fg= 'blue',relief =RIDGE )
        self.entry_label.grid(row=3, column=10)
        self.current_coordinates =[row,col]
        '''The entry widget for the user to input'''
        #user entry widget 
        user_entry = tk.Entry(self.root,font=("Helvetica" ,16,'bold'  ), justify='center')
        user_entry.grid(row=4, column=10, padx=1 , pady=1,ipady = 25 , ipadx=5 )
        user_entry.bind("<Return>" , self.get_entry_value)

    def get_entry_value(self,event):
        ''' get the user input and check if the value he put is possible to be put in the board  using the method checkPossible in sudoku class
        if so put it to the board and redraw board otherwise dont and display a label that says his input is invalid '''
        row , col  = self.current_coordinates[0] , self.current_coordinates[1]
        value = int(event.widget.get())
        if value > 9 :
            self.entry_label.configure(text=None , fg = 'white')
            self.entry_label.configure(text='Invalid' , fg = 'red')
            self.buttons[row][col].configure(bg='white', fg = 'blue')
            return 
        if ( self.sudoku.checkPossible(row , col , value) ) :
            self.buttons[row][col].configure(text=value,fg='blue')
            self.board[row][col] = value
            self.entry_label.configure(text=None , fg = 'white')
            self.entry_label.configure(text='Valid' , fg = 'green')
            self.buttons[row][col].configure(bg='white', fg = 'blue')
            if self.sudoku.satisfied() :
                self.game_finished()

        else :
            self.entry_label.configure(text=None , fg = 'white')
            self.entry_label.configure(text='Invalid' , fg = 'red')
            self.buttons[row][col].configure(bg='white', fg = 'blue')
    def game_finished(self) :
        ''' Message box if the game is finished ''' 
        messagebox.showinfo("Congratulation", "Sudoku game has been finished")



#main 

test = GUI()








        
