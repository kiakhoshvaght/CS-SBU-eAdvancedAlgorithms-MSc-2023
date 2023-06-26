# Import all classes of PuLP module
from pulp import *
import pulp as pl
import warnings
warnings.simplefilter(action='ignore')
import pandas

userGender = 'm' #input('Are you male(m) or female(f)?')
userWeight = 80 #float(input('Please input your weight:'))
userActivity = '2' #input('Please input your daily activity from 1(office job or studying) to 3(labor or professional athlete)?')
userBodyFatPercentFactor = 0.95 #Average due to inability to measure
leanFactor = 0.9 #Average for the sake of simplicity
userGenderFactor = float(0.9 if userGender == 'f' else 1)
userActivityFactor = float(1.3 if userActivity == '1' else 1.65 if userActivity == '2' else 2)
userBMR = userWeight * userGenderFactor * 24 * userBodyFatPercentFactor 
userDailyCaloriesNeeded = userBMR * userActivityFactor
print(f'Your (Approximate) BMR is {userBMR} and you need {userDailyCaloriesNeeded} calories daily')
print(f'These are some foods you can take for today:')

problem = LpProblem('Diet Problem', LpMaximize)

x = [] #Initialize objective variables
xCoefficients = []

pandas.set_option('display.max_rows', None)
foods = pandas.read_csv('/home/mahsaa/Desktop/CS-SBU-eAdvancedAlgorithms-MSc-2023/Assignments/401422081/project/food.csv') #fdc_id, description, food_category_id 
category = pandas.read_csv('/home/mahsaa/Desktop/CS-SBU-eAdvancedAlgorithms-MSc-2023/Assignments/401422081/project/food_category.csv') #id, description
nutrient = pandas.read_csv('/home/mahsaa/Desktop/CS-SBU-eAdvancedAlgorithms-MSc-2023/Assignments/401422081/project/food_nutrient.csv') #fdc_id, nutrient_id
ingredients = pandas.read_csv('/home/mahsaa/Desktop/CS-SBU-eAdvancedAlgorithms-MSc-2023/Assignments/401422081/project/input_food.csv') #fdc_id, fdc_of_input_food
#nutrient ids -> 1003 protein, 1004 fat, 1005 carbo
totalCalories = 0

cleanedData = []
for i in range(0,int(len(foods)/10)):
    foodId = foods.iloc[i]['fdc_id']
    foodDescription = foods.iloc[i]['description']
    nutrientRows = nutrient.query(f'fdc_id == {foodId}')
    calories = 0
    calories += 0 if nutrientRows.query(f'nutrient_id == 1003')['amount'].size == 0 else nutrientRows.query(f'nutrient_id == 1003')['amount'].values[0] * 4
    calories += 0 if nutrientRows.query(f'nutrient_id == 1004')['amount'].size == 0 else nutrientRows.query(f'nutrient_id == 1004')['amount'].values[0] * 9
    calories += 0 if nutrientRows.query(f'nutrient_id == 1005')['amount'].size == 0 else nutrientRows.query(f'nutrient_id == 1005')['amount'].values[0] * 4
    # print(f'foodId: {foodId} - desc: {foodDescription} - calory: {calories}')
    if(calories != 0):
        cleanedData.append({'fdc_id': foodId, 'title':foodDescription, 'calories': calories})

print(len(cleanedData))
    

for i in range(0,len(cleanedData)):
    x.append(LpVariable(name= str(cleanedData[i]['fdc_id']), upBound=1, lowBound=0, cat=LpInteger))
    xCoefficients.append(cleanedData[i]['calories'])

problem += lpSum(x[i] * xCoefficients[i] for i in range(0, len(x)))
problem += lpSum(x[i] * xCoefficients[i] for i in range(0, len(x))) <= userDailyCaloriesNeeded
# problem += (lpSum(x.values()) <= 2000, 'calories_condition')

problem.solve()
# print("Current Status: ", LpStatus[problem.status]) 
# print("Problem: ", problem)
# print("Objective: ", problem.objective)

for v in problem.variables():
    if(v.varValue == 1):
        # print(f'{v.name}')
        food = foods.query(f'fdc_id == {v.name}')
        print(food['description'].values)