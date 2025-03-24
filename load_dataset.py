from bs4 import BeautifulSoup, SoupStrainer, PageElement
import builtins
import os
from langchain_community.document_loaders import RecursiveUrlLoader
from bs4 import BeautifulSoup, XMLParsedAsHTMLWarning
import warnings



loader = RecursiveUrlLoader('https://webgpufundamentals.org/', max_depth=2)
docs = loader.load()

# print(len(docs))
for doc in docs:
    if doc.metadata['content_type']=="application/xml":
        # print("xml")
        continue
    
    soup = BeautifulSoup(doc.page_content)
    lesson_main = soup.find('div', attrs={"class":"lesson-main"})
    title_elem = soup.find('div', attrs={"class":"lesson-title"})
    if title_elem ==  None or lesson_main == None:
        # print(doc.page_content)
        continue
    
    extracted_content = []
    for element in lesson_main.descendants:
        if element.name == 'p':
            extracted_content.append(element.get_text(strip=True))
        elif element.name == 'pre':
            # Get the class name if it starts with 'lang-'
            class_attr = element.get("class", [])
            lang_class = next((cls for cls in class_attr if cls.startswith("lang-")), None)
            
            # Format the code block with backticks and language
            if lang_class:
                extracted_content.append(f"```{lang_class[5:]}\n{element.get_text(strip=True)}\n```")
            else:
                extracted_content.append(f"```\n{element.get_text(strip=True)}\n```")    
        elif element.name == 'div':
            # Get the class name if it starts with 'lang-'
            class_attr = element.get("class", [])
            is_bottom_bar_class = next((cls for cls in class_attr if cls.startswith("webgpu_bottombar")), None) != None 
            is_warn_class = next((cls for cls in class_attr if cls.startswith("warn")), None) != None 
            if is_bottom_bar_class or is_warn_class:
                extracted_content.append(element.get_text(strip=True))
        elif element.name == 'section':
            # Get the class name if it starts with 'lang-'
            extracted_content.append(element.get_text(strip=True))
            

    # for content in extracted_content:
    #     print(content)
    curr_path = os.path.abspath(os.curdir)
    page_title = title_elem.get_text(strip=True)
    dest_file_name = "_".join(page_title.split(' '))
    dest_file_name_full = f"{dest_file_name}.txt"
    dest_path = os.path.join(curr_path,'docs','webgpu',dest_file_name_full)
    print(dest_path)
    with builtins.open(dest_path,"w") as f:
        page = "\n\n".join(extracted_content)
        f.write(page)