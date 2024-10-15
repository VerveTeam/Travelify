DESCRIPTION_PROMPT = """
You will receive names of famous tourist attractions and nearby restaurants. It would be in form of an array, your job should 
be to iterate throught the entire array and write a short description about the place and the best time of the day to visit 
that particular place. You also need to give an description about the restaurant as well.

The output should be a python dictionary with keys as "Places" and "Restaurants".

### Output format
{
    "Places": ['<Description for Place at index 0>', '<Description for Place at index 1>'],
    "Restaurants": ['<Description for Restaurant at index 0>','<Description for Restaurant at index 1>']
}


"""