import os
from tabulate import tabulate
import time
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
path = os.getcwd()

def setting_up():
    os.system("pip3 install -r requirements.txt")
    os.chdir(path + "/src")
    os.system("python3 download_model.py 124M")

def auth_drive():
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)
    file_id = [
        "1w90gcY_DzPyGKHc3wX-vwejuNrnxGo0J",
        "1fRKWHCAI0BHp9ufts3zkawTClYWuY_Xn",
        "1ypk3UGzbzo6YbOnw_GrAIT_L8f9zQ5sa"
    ]
    names = ["action", "crime", "comedy"]
    for i in range(len(file_id)):
        os.mkdir(names[i])
        os.chdir(path + "/src/" + names[i])
        file_list = drive.ListFile({'q': "'%s' in parents and trashed=false" % file_id[i]}).GetList()
        for file1 in file_list:
            print('title: %s, id: %s' % (file1['title'], file1['id']))
            file1.GetContentFile(file1['title'])
        os.chdir("../GPT2-WriteEmUp")

def run_gen():
    os.chdir(path + "/src")
    gen_sel_table = [["Num.", "Contents"],[1, "Generate Unconditional Samples"], [2, "Generate Interactive Conditional Samples"]]
    print(tabulate(gen_sel_table, headers="firstrow", tablefmt="fancy_grid"))
    gen_sel = int(input("\nPlease input your choice: "))

    genre_sel_table = [["Num.", "Contents"],[1, "Action"], [2, "Crime"], [3, "Comedy"]]
    print(tabulate(genre_sel_table, headers="firstrow", tablefmt="fancy_grid"))
    genre_sel = input("\nPlease input the name of the category: ")
    genre = ["action", "crime", "comedy"]

    def unconditional_parameters(top_k = 0, temperature = 1, category = genre_sel):
        a = 0
        print("\n\n-------PARAMETERS---------")
        top_k = int(input("\nPlease input the top_k value for your sample(A good value is 40. Inputs are from 0- 100): "))
        if 0 >= top_k >= 100:
            print("Input parameter wrong.")
            unconditional_parameters()
        temperature = float(input("\nPlease input the custom words for your sample(The best is 0.8. Inputs are from 0 - 1): "))
        if 0 >= temperature >= 1:
            print("Input parameter wrong.")
            unconditional_parameters()
        category = category.lower()
        for i in genre:
            if i != category:
                print(f"\n{category}: not found. Checking the next category")
                a += 1
                if a >= len(genre):
                    print("Your input is wrong.")
                    unconditional_parameters()
                else:
                    pass
            
        param_data_unconditional = [["Param.", "Values"], ["top_k", f"{top_k}"], ["temperature", f"{temperature}"], ["category", f"{category}"]]
        print("\n")
        print(tabulate(param_data_unconditional, headers="firstrow", tablefmt="fancy_grid"))
        time.sleep(1)
        print("\n\nGenerating uncondtional samples...")
        os.chdir(path + "/src")
        os.system(f"python3 generate_unconditional_samples.py --top_k {top_k} --temperature {temperature} --model_name {category}")

    def interactive_conditional_parameters(top_k = 0, temperature = 1, nsamples = 1, category = genre_sel):
        b = 0
        print("\n\n-------PARAMETERS---------")
        top_k = int(input("\nPlease input the top_k value for your sample(A good value is 40. Inputs are from 0- 100): "))
        if 0 > top_k > 100:
            print("Input parameter wrong.")
            interactive_conditional_parameters()
        temperature = float(input("\nPlease input the custom words for your sample(The best is 0.8. Inputs are from 0 - 1): "))
        if 0 > temperature > 1:
            print("Input parameter wrong.")
            interactive_conditional_parameters()
        nsamples = int(input("\nPlease input the number of samples that you want.(Default val. is 1): "))
        if nsamples <= 0:
            print("Input parameter wrong.")
            interactive_conditional_parameters()
        category = category.lower()
        for i in genre:
            if i == category:
                break
            else:
                print("Category not found. Checking the next category")
            b += 1
            if b < len(genre):
                print("Your input is wrong.")
                interactive_conditional_parameters()
            
        param_data_conditional = [["Param.", "Values"], ["top_k", f"{top_k}"], ["temperature", f"{temperature}"], ["nsamples", f"{nsamples}"],["category", f"{category}"]]
        print("\n")
        print(tabulate(param_data_conditional, headers="firstrow", tablefmt="fancy_grid"))
        time.sleep(1)
        print("\n\nGenerating interactive condtional samples...")
        os.chdir(path + "/src")
        os.system(f"python3 interactive_conditional_samples.py --top_k {top_k} --temperature {temperature} --nsamples {nsamples} --model_name {category}")

    if gen_sel == 1:
        unconditional_parameters()
    elif gen_sel == 2:
        interactive_conditional_parameters()

setting_up()
auth_drive()
def main():
    head = [["Num.", "Contents"], [1, "Generate Text"], [2, "Exit"]]
    print(tabulate(head, headers = "firstrow", tablefmt="fancy_grid"))
    inp = int(input("Please input your choice: "))
    if inp == 1:
        run_gen()
    else:
        exit()

main()
