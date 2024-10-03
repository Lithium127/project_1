"""
---------------------------------------------------------------- 
Name:       Liam Wagner
Course:     CS1430, Section X, Fall 2024 
Assignment: Assignment 1 - Cost of College 
Purpose:    This program calculates the cost of college per 
            semester, week , day and even hour of class 
Input:      User the cost per year. The user also requests the 
            type of report and might be asked for the current 
            number of credits they are taking 
Output:     The output of this program is a report of costs based 
            on what the user has requested, it might be cost per 
            hour, per credit, per week or per semester 
----------------------------------------------------------------
"""
import sys
import os
import typing as t

from asciimatics.exceptions import ResizeScreenError
from asciimatics.screen import Screen
from asciimatics.scene import Scene
from asciimatics.widgets import Frame, Text, Layout, Label, VerticalDivider, Divider, ListBox, Widget

#################### 
# CONSTANTS 
################### 
_SEMESTERS_PER_YEAR = 2 
_WEEKS_PER_SEMESTER = 18 
_DAYS_PER_SEMESTER  = 90
_BREAK              = "-" * 35
_HOURS_PER_DAY      = 24

_REFERENCE_PRICE_LIST = [ # Must be reverse sorted to function
    ("Airplane", 359000),
    ("New Car", 48000),
    ("Used Car", 26000),
    ("Raising a Child (yr)", 20130),
    ("Billboard Ad", 7000),
    ("Average Mortgage", 2200),
    ("SCUBA Gear", 2000),
    ("Average Rent", 1400),
    ("Personal Computer", 1200),
    ("iPhone", 900),
    ("Television", 500),
    ("iPad", 350),
    ("Textbook", 200),
    ("15 Gallons of gas", 57.75),
    ("Steam Game", 40),
    ("Minecraft", 27),
    ("500 sheets of paper", 9),
    ("Hamburger", 5),
    ("A penny", 0.25),
]


class GradeCalculatorView(Frame):
    
    def __init__(self, screen: Screen) -> None:
        """Frane for calculating grades

        Args:
            screen (Screen): Screen select for 
        """
        super(GradeCalculatorView, self).__init__(
            screen,
            screen.height * 2 // 3, # height
            screen.width * 2 // 3, # width
            on_load=self.on_load, # The function called when the system loads
            hover_focus=True # weather to allow the [tab] key to focus on objects
        )
    
        # Create and add a layout for calculation outputs
        calculation_layout = Layout([58, 2, 40], fill_frame=True)
        self.add_layout(calculation_layout)

        self._cost_per_year_input = Text(
            label = "Cost / Year:    $",
            name = "cost",
            on_change = self.update_costs,
            on_focus = lambda: self.update_reference_list(self.text_to_float(self._cost_per_year_input.value))
        )
        calculation_layout.add_widget(Label("Input", align=">"))
        calculation_layout.add_widget(Label("---"))
        calculation_layout.add_widget(self._cost_per_year_input)
        
        calculation_layout.add_widget(Divider(), 0)        
        
        self.c_semester = Text(
            "Semester: $", 
            readonly=True, 
            # This function updates the reference list when this object is hovered over
            on_focus = lambda: self.update_reference_list(
                self.text_to_float(self.c_semester.value)
            )
        )
        self.c_month    = Text("Month     $", readonly=True, on_focus = lambda: self.update_reference_list(self.text_to_float(self.c_month.value)))
        self.c_week     = Text("Week:     $", readonly=True, on_focus = lambda: self.update_reference_list(self.text_to_float(self.c_week.value)))
        self.c_day      = Text("Day:      $", readonly=True, on_focus = lambda: self.update_reference_list(self.text_to_float(self.c_day.value)))
        self.c_hour     = Text("Hour      $", readonly=True, on_focus = lambda: self.update_reference_list(self.text_to_float(self.c_hour.value)))
        
        calculation_layout.add_widget(Label("General Breakdown", align=">"))
        calculation_layout.add_widget(self.c_semester)
        calculation_layout.add_widget(self.c_month)
        calculation_layout.add_widget(self.c_week)
        calculation_layout.add_widget(self.c_day)
        calculation_layout.add_widget(self.c_hour)
        
        calculation_layout.add_widget(Divider())
        
        self._credit_input = Text(
            "Credits / Semester",
            "credits",
            on_change = self.update_costs
        )
        self.c_credit   = Text("Credit:   $", readonly=True, on_focus = lambda: self.update_reference_list(self.text_to_float(self.c_credit.value)))
        self.c_class    = Text("Class:    $", readonly=True, on_focus = lambda: self.update_reference_list(self.text_to_float(self.c_class.value)))
        
        calculation_layout.add_widget(Label("Credit Beakdown", align=">"))
        calculation_layout.add_widget(self._credit_input)
        calculation_layout.add_widget(self.c_credit)
        calculation_layout.add_widget(self.c_class)
        
        calculation_layout.add_widget(Divider())
        
        
        
        calculation_layout.add_widget(VerticalDivider(), 1)
        
        self._reference_prices = _REFERENCE_PRICE_LIST
        
        self._reference_list = ListBox(
            Widget.FILL_FRAME,
            self.get_sorted_reference_list(0.0)
        )
        
        calculation_layout.add_widget(self._reference_list, 2)
        
        # Updates this instance with all current widgets
        self.fix()
    
    def on_load(self) -> None:
        """Updates internal widgets, called when the instance is loaded"""
        self.update_costs()
        self.update_reference_list(0.0)
    
    def update_reference_list(self, number: float) -> None:
        """Updates the reference list to change the position of the current selector

        Args:
            number (float): The current selector
        """
        self._reference_list.options = self.get_sorted_reference_list(number)
    
    def get_sorted_reference_list(self, number: float) -> list:
        """Sorts the list of reference options around a specified number

        Args:
            number (float): The current selector

        Returns:
            list: Sorted reference options
        """
        less_list = []
        greater_list = []
        
        for item, price in self._reference_prices:
            if price > number:
                greater_list.append((f"${price}{' '*(8-len(str(price)))} - {item}", 0))
            else:
                less_list.append((f"${price}{' '*(8-len(str(price)))} - {item}", 0))
        return greater_list + [(f"-[${number}]----------", 0)] + less_list
        
    
    def update_costs(self) -> None:
        """Updates all read-only text on the GUI"""
        price = self.get_user_input()
        
        c_semester = price      / _SEMESTERS_PER_YEAR
        c_week     = c_semester / _WEEKS_PER_SEMESTER
        c_month    = c_week     * 4
        c_day      = c_semester / _DAYS_PER_SEMESTER
        c_hour     = c_day      / _HOURS_PER_DAY
        c_credit   = c_semester / self.get_credits()
        c_class    = c_credit   / _WEEKS_PER_SEMESTER
        
        self.c_semester.value = self.truncate_float(c_semester)
        self.c_month.value    = self.truncate_float(c_month)
        self.c_week.value     = self.truncate_float(c_week)
        self.c_day.value      = self.truncate_float(c_day)
        self.c_hour.value     = self.truncate_float(c_hour)
        self.c_credit.value   = self.truncate_float(c_credit)
        self.c_class.value    = self.truncate_float(c_class)
    
    def truncate_float(self, f: float) -> str:
        """Truncates float f to two decimal places as a string

        Args:
            f (float): float to truncate

        Returns:
            str: String representation, truncated to 2 decimal places
        """
        s = str(float(f)).split(".")
        if len(s) < 2: return f
        return ".".join([s[0], s[1][:2]])
    
    def text_to_float(self, text, default: float = 0.0) -> float:
        """Converts a text to a float, accounts for errors in casting and returns the default

        Args:
            text (str): Text to cast
            default (float, optional): Default value for error catching. Defaults to 0.0.

        Returns:
            float: Converted text or default value
        """
        value = text
        
        if not value:
            return default
        if  len(value) <= 0:
            return default
        
        try: value = float(value)
        except: return default
        return value
    
    def get_user_input(self) -> float:
        """Returns the value contained in _cost_per_year_input

        Returns:
            float: User input or 0.0
        """
        # Using the cost per year, assuming the other two options don't have anything in them
        return self.text_to_float(self._cost_per_year_input.value)
    
    def get_credits(self) -> float:
        """Returns the user-input number of credits

        Returns:
            float: User input or 1.0
        """
        return self.text_to_float(self._credit_input.value, 1.0)
    

def create_screen(screen, scene) -> None:
    """Creates scenes and effects and plays the screen

    Args:
        screen (Screen): The screen on which to run the scenes
        scene (Scene): The scene to start on
    """
    # Define your Scenes here
    scenes = [
        Scene([GradeCalculatorView(screen)], -1)
    ]

    # Run your program
    screen.play(scenes, stop_on_resize=True, start_scene=scene)

def start_gui() -> None:
    """Starts the cost of college calculator in a text-based GUI mode"""
    last_scene = None
    while True:
        try:
            Screen.wrapper(create_screen, arguments=[last_scene])
            sys.exit(0)
        except ResizeScreenError as e:
            last_scene = e.scene

def no_gui() -> None:
    """Starts the cost of college calculator in a terminal-based, no GUI mode"""
    os.system("clear") # Clear console
    print("-->  COST OF COLLEGE ESTIMATOR  <--")
    print(_BREAK)
    while True:
        try:
            cost_year = float(input("Please enter the cost of college per year --> \n"))
            break
        except: pass
    print(_BREAK)
    print("Select from the following:")
    print(_BREAK)
    print("\n".join([
        "A -> cost per SEMESTER",
        "B -> cost per WEEK",
        "C -> cost per DAY",
        "D -> cost per CREDIT",
        "E -> cost per 50 minute class PERIOD"
    ]))
    print(_BREAK)
    choice = input("Please enter A - E--> \n")
    if   choice == "A":
        amount = cost_year / _SEMESTERS_PER_YEAR
        print(f"Cost per semester is ${amount:.2f}")
    elif choice == "B":
        amount = (cost_year / _SEMESTERS_PER_YEAR) / _WEEKS_PER_SEMESTER
        print(f"Cost per week is ${amount:.2f}")
    elif choice == "C":
        amount = (cost_year / _SEMESTERS_PER_YEAR) / _DAYS_PER_SEMESTER
        print(f"Cost per day is ${amount:.2f}")
    elif choice == "D":
        credits = int(input("How many credits are you taking this semester --> \n"))
        amount = (cost_year / _SEMESTERS_PER_YEAR) / credits
        print(f"Cost per credit is ${amount:.2f} ")
    elif choice == "E":
        credits = int(input("How many credits are you taking this semester --> \n"))
        amount = ((cost_year / _SEMESTERS_PER_YEAR) / credits) / _WEEKS_PER_SEMESTER
        print(f"Cost per 50 minute class period is ${amount:.2f} ")
    else:
        print("Invalid selection, must be A-E!")
    
    
    
start_gui()