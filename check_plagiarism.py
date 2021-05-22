import os
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from collections import Counter


# Dictionary to store the Submissions
submissions={}


def format_code(code):

    '''
    
    Converts the submitted code from Hackerrank to desired format
    
    Parameters:
    code (String) : Submitted code
    
    Returns:
    new_code (String) : Formatted code with spaces and line number removed
    code_words (List) : List of words in the code
    
    '''
    
    code_lines=code.splitlines()
    new_code=""
    
    for i in range(len(code_lines)):
        line=code_lines[i]
        line=line.strip()
        if line.isnumeric():
            continue
        new_code=" ".join((new_code, line))
       
    new_code.strip()
    code_words=new_code.split(" ")
    new_code=new_code.replace(" ","")
   
    return new_code, code_words


def process_submission(browser, submission):

    '''
    
    Extracts necessary information from a submission tile and adds that as a list to submissions dictionary with key equal to the problem name
    
    Parameters:
    browser (WebDriver) : WebDriver Instance
    submission (WebElement) : Submission to process 
    
    '''
    
    foo=submission.find_elements_by_css_selector("p.small")
    
    # Score got for the solution
    score=float(foo[3].text)
    print(score)

    # Flag to check whether the submission was during the contest
    within_contest=foo[4].text
    
    if within_contest=="No":
        return
    
    bar=submission.find_elements_by_css_selector("a.challenge-slug.backbone")
    
    # Name of the problem
    problem_name=bar[0].text

    # Username of the submitter
    submitted_by=bar[1].text
    
    view=submission.find_element_by_css_selector("a.view-results").get_attribute("href")
    
    # Link of the solution
    solution_link=view

    browser.get(view)
    
    time.sleep(4)
    
    code=browser.find_element_by_css_selector("div.CodeMirror-lines")
    code=code.text
    new_code, code_words=format_code(code)
    
    entry=[submitted_by, new_code,solution_link, code_words]
    
    if problem_name not in submissions:
        submissions[problem_name]=[]
    
    submissions[problem_name].append(entry)
    
    browser.execute_script("window.history.go(-1)")


def view_submissions(browser, submission_link, page_num):

    '''
    
    Downloads submissions for a given page
    
    Parameters:
    browser (WebDriver) : WebDriver Instance
    submission_link (String) : Root link of the submission pages
    page_num (String) : Page Number
    
    Returns:
    boolean: True if page is not empty else False
    
    '''
    
    # Link of the submission page
    page_link=os.path.join(submission_link,page_num)
    browser.get(page_link)
    
    time.sleep(2)
    
    class_name="judge-submissions-list-view"
    
    # List of the submissions in the page
    submission_list=browser.find_elements_by_class_name(class_name)
    
    length=len(submission_list)
    
    if not length:
        return False
    
    for i in range(length):
        
        try:
            process_submission(browser, submission_list[i])
            time.sleep(2)
            submission_list=browser.find_elements_by_class_name(class_name)
        except Exception as e:
            print(e)
            continue
            
    return True


def download_submissions(browser, submission_link):

    '''
    
    Goes through the different submission pages
    
    Parameters:
    browser (WebDriver) : WebDriver Instance
    submission_link (String) : Root link of the submission pages
    
    '''
    
    # Submission page number
    page_num=1
    
    should_continue=True
    
    while should_continue: 
        
        try:
            should_continue=view_submissions(browser, submission_link, str(page_num))
        except Exception as e:
            print(e)
            continue
          
        page_num+=1


def hackerrank_contest(chrome_webdriver, submission_link, username, password):

    '''
    
    Function to download the submissions from hackerrank
    
    Parameters:
    chrome_webdriver (String) : Path of the Chrome Webdriver executable
    submission_link (String) : Root link of the submission pages
    username (String) : Hackerrank account username
    password (String) : Hackerrank account password
    
    '''
    
    try:

        browser=webdriver.Chrome(chrome_webdriver)
    
        # Login to Hackerrank
        browser.get("https://www.hackerrank.com/login")
        time.sleep(1)
        browser.find_element_by_name("username").send_keys(username)
        time.sleep(2)
        browser.find_element_by_name("password").send_keys(password,Keys.ENTER)
        
        print("Downloading submissions....")
        download_submissions(browser, submission_link)
    
    except Exception as e:
        print(e)


def compute_cosine_similarity(words1,words2):

    """
    
    Computes the cosine similarity between two codes
    
    Parameters:
    words1 (List) : List of words for the first code 
    words2 (List) : List of words for the second code
    
    Returns:
    cosine (Float) : Cosine similarity of the two codes
    
    """
    
    # Dictionaries with the words of the code
    val1=Counter(words1)
    val2=Counter(words2)
    
    # List of all the words in the two codes
    words = list(val1.keys() | val2.keys())
    
    # Vectors corresponding to the two codes
    vect1 = [val1.get(word, 0) for word in words]
    vect2 = [val2.get(word, 0) for word in words]

    len1 = sum(v*v for v in vect1) ** 0.5
    len2 = sum(v*v for v in vect2) ** 0.5
    dot = sum(v1*v2 for v1,v2 in zip(vect1, vect2))
    cosine = dot/(len1 * len2)
    
    return cosine


def check_plagiarism(disqualify, cosine_similarity=False, thresh=0.95):

    """
    
    Checks for plagiarism between two codes by either using cosine similarity of code equality
    
    Parameters:
    disqualify (List) : List to which items to be appended
    cosine_similarity (Boolean) : Boolean value to decide if cosine similarity is to be used
    thresh (Float) : threshold value for cosine similarity
    
    """
    
    for key in submissions:
        length=len(submissions[key])
        
        for i in range(length):
            username1=submissions[key][i][0]
            code1=submissions[key][i][1]
            solution_link1=submissions[key][i][2]
            code_words1=submissions[key][i][3]
            
            for j in range(i+1,length):
                username2=submissions[key][j][0]
                code2=submissions[key][j][1]
                solution_link2=submissions[key][j][2]
                code_words2=submissions[key][j][3]
                
                if username1==username2:
                    continue
                
                entry=[username1, solution_link1, username2, solution_link2, key]
                
                if cosine_similarity:
                    cosine=compute_cosine_similarity(code_words1,code_words2)
                    if cosine>=thresh:
                        disqualify.append(entry)
                    
                else:
                    if code2==code1:
                        disqualify.append(entry)


#check_plagiarism(disqualify,True)


def get_output(disqualify)->str:

    """
    
    Converts the list of disqualified candidates to a string output
    
    Parameters:
    disqualify (List) : List of candidates who have been detected for plagiarism
    
    Returns:
    output (String) : String representation to be presented on the GUI

    """

    
    output=""
    
    for row in disqualify:
        s=" ".join(map(str,row))
        output="\n".join((output,s))
        
    return output


# List of candidates caught doing plagiarism
disqualify=[]


def driver_function(chrome_webdriver, submission_link, username, password):

    '''
    
    Driver function
    
    Parameters:
    chrome_webdriver (String) : Path of the Chrome Webdriver executable
    submission_link (String) : Root link of the submission pages
    username (String) : Hackerrank account username
    password (String) : Hackerrank account password

    Returns:
    output (String) : String containing all list of candidates doing plagiarism
    
    '''

    hackerrank_contest(chrome_webdriver, submission_link,username,password)
    check_plagiarism(disqualify,True)
    output=get_output(disqualify)
    return output