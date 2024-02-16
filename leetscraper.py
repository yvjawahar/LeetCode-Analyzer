import requests
from bs4 import BeautifulSoup
import re
import json
def get_contest_rating(contest_span):
    raw_text = contest_span.get_text(strip=True)
    numeric_part = ''.join(c for c in raw_text if c.isdigit() or c == ',')
    numeric_value = int(numeric_part.replace(',', ''))
    return numeric_value

def get_name(name_element):
    if name_element:
       name = name_element.get_text(strip=True)
       return name
    return "null"
def get_rank(rank_span):
    raw_text = rank_span.get_text(strip=True)
    numeric_part = ''.join(c for c in raw_text if c.isdigit() or c == ',')
    numeric_value = int(numeric_part.replace(',', ''))
    return numeric_value

def scrape_leetcode_profile(username):
    url = f'https://leetcode.com/{username}/'
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extracting details
        name_element = soup.find('div', class_='text-label-1 dark:text-dark-label-1 break-all text-base font-semibold')
        name=get_name(name_element)
        rank= soup.select_one('span.ttext-label-1.dark\\:text-dark-label-1.font-medium')
        rank=get_rank(rank)
        contest_rating = soup.find('div','text-label-1 dark:text-dark-label-1 flex items-center text-2xl')
        contest_rating=get_contest_rating(contest_rating)

        contest = soup.find_all(class_='text-label-1 dark:text-dark-label-1 font-medium leading-[22px]')
        global_rank=contest[0].get_text()
        number_of_contest=int(contest[1].get_text())
        
        
        easy=""
        easy_solved=0
        easy_total=0
        medium=""
        medium_solved=0
        medium_total=0
        hard=""
        hard_solved=0
        hard_total=0
        total_problems_solved=0
        total_problems=0
        data=[]
        problem_sections = soup.find_all('div', class_='space-y-2')
        for section in problem_sections:
            # Extract information from each section
            problem_type_element = section.find('div', class_='w-[53px] text-label-3 dark:text-dark-label-3')
            problem_solved_element = section.find('span', class_='mr-[5px] text-base font-medium leading-[20px] text-label-1 dark:text-dark-label-1')
            problem_total_element = section.find('span', class_='text-xs font-medium text-label-4 dark:text-dark-label-4')
            
            # Check if the elements are found before calling get_text()
            problem_type = problem_type_element.get_text(strip=True) if problem_type_element else None
            problem_solved = problem_solved_element.get_text(strip=True) if problem_solved_element else None
            problem_total = problem_total_element.get_text(strip=True) if problem_total_element else None

            # Append the extracted information to the data list
            data.append({
                'problem_type': problem_type,
                'problem_solved': problem_solved,
                'problem_total': problem_total
            })
        for index in range(len(data)):
            for key in data[index]:
                if index==0:
                    if key=='problem_type':
                        easy=data[index][key]
                    if key=='problem_solved':
                        easy_solved=int(data[index][key])
                        total_problems_solved+=easy_solved
                    if key=='problem_total':
                        easy_total=int(data[index][key][1:])
                        total_problems+=easy_total
                elif index==1:
                    if key=='problem_type':
                        medium=data[index][key]
                    if key=='problem_solved':
                        medium_solved=int(data[index][key])
                        total_problems_solved+=medium_solved
                    if key=='problem_total':
                        medium_total=int(data[index][key][1:])
                        total_problems+=medium_total
                elif index==2:
                    if key=='problem_type':
                        hard=data[index][key]
                    if key=='problem_solved':
                        hard_solved=int(data[index][key])
                        total_problems_solved+=hard_solved
                    if key=='problem_total':
                        hard_total=int(data[index][key][1:])
                        total_problems+=hard_total

        

        return {
            'name': name,
            'rank': rank,
            'contest_rating': contest_rating,
            #'contests_attended': number_of_contest,
            'easy': easy,
            'easy_solved':easy_solved,
            'easy_total':easy_total,
            'medium':medium,
            'medium_solved':medium_solved,
            'medium_total':medium_total,
            'hard':hard,
            'hard_solved':hard_solved,
            'hard_total':hard_total,
            'total_problems_solved':total_problems_solved,
            'total_problems':total_problems,
            'global_ranking':global_rank,
            'contest_attended':number_of_contest,
        }

    else:
        print(f"Failed to fetch data for {username}. Status code: {response.status_code}")
        return None

# profile_data = scrape_leetcode_profile()

# if profile_data:
#     json_data = json.dumps(profile_data, ensure_ascii=False).replace("'", '"')
#     print(profile_data)
