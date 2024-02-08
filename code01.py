def BMI(weight, height):
    bmi = weight / float(height * height)
    result = ""
    if bmi < 18.5:
        result = "Underweight"
    elif bmi >= 18.5 and bmi < 25:
        result = "Normal"
    elif bmi >= 25 and bmi < 30:
        result = "Overweight"
    else:
        result = "Obesity"

    return result
